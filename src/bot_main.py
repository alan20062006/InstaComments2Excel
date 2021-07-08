import itertools
from os import path
from pdb import set_trace
import pickle
from typing import Dict, List, Tuple

from explicit import waiter, XPATH
from selenium import webdriver
import selenium
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common import action_chains
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import traceback
import urllib.parse
import numpy.random as random
import requests
import yaml
import pandas as pd

from src.profile import AccountProfile, profile_parser, get_post_link

SAVE_FILE_NAME = 'influencer_info.csv'
COOKIES_PATH = './login.cache'

class PrivateException(Exception):
    pass

with open(r'config.yml') as file:
    account = yaml.full_load(file)

class InstagramBot():
    def __init__(self, account):
        options = Options()
        # options.add_argument('--headless')
        # options.add_argument('--no-sandbox')
        # options.add_argument('--disable-dev-shm-usage')
        options.add_argument("user-data-dir=selenium") 
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(5)

        self.http_base = requests.Session()

        self.username = account['username']
        self.password = account['password']
        self.info_list = []

        with open(r'filter.yml') as file:
            self.filter = yaml.full_load(file)
    '''
    Helper function
    '''
    def sleep(self, mu = 2, sigma = 0.5):
        time.sleep(self.wait(mu, sigma))
        return 
    
    def wait(self, mu = 2, sigma = 0.5):
        # random wait time to avoid being detected
        if sigma == 0:
            return mu
        else:
            t = random.normal(mu, sigma,1)[0]
            if t <= 0:
                return 0.1
            else:
                return t

    '''
    Low level API
    '''
    def check_availability(self, username: str):
        """
        Checking Status code, Taking number of posts, Privacy and followed by viewer
        Raise Error if the Profile is private and not following by viewer
        return: numbers of posts/followers/followings
        """
        search = self.http_base.get(f'https://www.instagram.com/{username}/', params={'__a': 1})
        search.raise_for_status()

        load_and_check = search.json()
        privacy = load_and_check.get('graphql').get('user').get('is_private')
        followed_by_viewer = load_and_check.get('graphql').get('user').get('followed_by_viewer')
        
        if privacy and not followed_by_viewer:
            raise PrivateException(f'[!] Account is private: {username}')
        return search.json()

    # def get_post_link(self, username: str) -> Tuple[List[str], List[str], List[str]]:
    #     '''
    #     Get the links of first 12 posts(I don't where where did I put this stupid hard coded number)
    #     that contains the detailed information of the posts. Also with the numbers of likes and comments
    #     of this post.
    #     The numbers of likes and comments will be rounded and formated in string.
    #     '''
    #     url = f'https://www.instagram.com/{username}/'
    #     self.driver.get(url)
    #     action = ActionChains(self.driver) # mouse pointer driver
    #     elements = self.driver.find_elements_by_xpath('//a[@href]')
    #     post_links = []
    #     n_likes = []
    #     n_comments = []
    #     for elem in elements:
    #         urls = elem.get_attribute('href')
    #         if 'p' in urls.split('/'):
    #             action.move_to_element(elem).perform() # move pointer to the post to get the likes and comments info
    #             post_links.append(urls)
    #             # get numbers of likes and comments
    #             temp_likes, temp_comments = elem.find_element_by_class_name('qn-0x').text.split('\n')
    #             n_likes.append(temp_likes)
    #             n_comments.append(temp_comments)
    #     return post_links, n_likes, n_comments

    def get_profile(self, username, keep_post_jsons=False) -> Dict:
        # Taking hrefs while scrolling down
        profile_graphql = self.check_availability(username)
        print(f"Analyzing account: {username}")
        user_profile = profile_parser(username, profile_graphql)
        
        self.sleep(0.5)
        self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        self.sleep(0.5)

        if keep_post_jsons:
            ''' TODO:
            post basic infos can be directly parsed from profile_graphql, instead of doing http requests again and again
            '''
            # post json string is stored in another link
            post_links, n_likes, n_comments = get_post_link(username)
            print(f'[*] extracting {len(post_links)} posts jsons string, please wait...'.title())
            user_profile.new_links = [urllib.parse.urljoin(link, '?__a=1') for link in post_links]
            user_profile.post_jsons = [self.http_base.get(link.split()[0]).json() for link in user_profile.new_links]
            # here you can do anything to parse the detailed info of a post

        return user_profile
    
    def get_followers(self, username: str, max_width: int = 500) -> List[str]:
        '''
        Get a bunch of follwers of an account
        '''
        url = f'https://www.instagram.com/{username}/'
        self.driver.get(url)
        # click on "followers" on main page
        followersLink = self.driver.find_element_by_xpath("(//a[@class='-nal3 '])[2]")
        followersLink.click()
        self.sleep(1)
        # find the popup follower tab
        followersList = self.driver.find_element_by_xpath("//div[@role='dialog']")
        num = len(followersList.find_elements_by_css_selector('li'))
        actionChain = webdriver.ActionChains(self.driver)
        while (num < max_width):
            # followersList.click() # trick
            self.sleep()
            actionChain.key_down(Keys.SPACE).pause(self.wait(0.1,0.01)).key_up(Keys.SPACE).perform()
            actionChain.reset_actions()
            num = len(followersList.find_elements_by_css_selector('li'))
        
        followers = []
        for user in followersList.find_elements_by_css_selector('li'):
            userLink = user.find_element_by_css_selector('a').get_attribute('href')
            followers.append(userLink.split('/')[-2])
            if (len(followers) >= max_width):
                break

        return followers
    def scrape_followers(self, username, max_width: int = 50):
        # Load account page
        self.driver.get("https://www.instagram.com/{0}/".format(username))

        # Click the 'Follower(s)' link
        # driver.find_element_by_partial_link_text("follower").click
        self.sleep(2)
        self.driver.find_element_by_xpath("(//a[@class='-nal3 '])[2]").click()

        # Wait for the followers modal to load
        waiter.find_element(self.driver, "//div[@role='dialog']", by=XPATH)
        # allfoll = int(self.driver.find_element_by_xpath("//li[2]/a/span").text)
        
        # At this point a Followers modal pops open. If you immediately scroll to the bottom,
        # you hit a stopping point and a "See All Suggestions" link. If you fiddle with the
        # model by scrolling up and down, you can force it to load additional followers for
        # that person.

        # Now the modal will begin loading followers every time you scroll to the bottom.
        # Keep scrolling in a loop until you've hit the desired number of followers.
        # In this instance, I'm using a generator to return followers one-by-one
        followers = []
        follower_css = "ul div li:nth-child({}) a.notranslate"  # Taking advange of CSS's nth-child functionality
        for group in itertools.count(start=1, step=12):
            for follower_index in range(group, group + 12):
                if follower_index > max_width:
                    return followers
                followers.append(waiter.find_element(self.driver, follower_css.format(follower_index)).text)

            # Instagram loads followers 12 at a time. Find the last follower element
            # and scroll it into view, forcing instagram to load another 12
            # Even though we just found this elem in the previous for loop, there can
            # potentially be large amount of time between that call and this one,
            # and the element might have gone stale. Lets just re-acquire it to avoid
            # tha
            last_follower = waiter.find_element(self.driver, follower_css.format(group+11))
            self.driver.execute_script("arguments[0].scrollIntoView();", last_follower)

    '''
    High level API
    '''
    def sign_in(self):
        if path.exists(COOKIES_PATH):
            print("Loading existing cookies")
            cookies = pickle.load(open(COOKIES_PATH, "rb"))
            # cookies = {
            #     cookie['name']: cookie['value']
            #     for cookie in get_cookies
            # }
            # for cookie in get_cookies:
            #     self.driver.add_cookie(cookie)


        else:
            self.driver.get('https://www.instagram.com/accounts/login/')
            try:
                WebDriverWait(self.driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "//input[@name='username']"))
                )
            except Exception as e:
                traceback.print_exc()
                print(e)
                return
            self.driver.find_element_by_xpath("//input[@name='username']").send_keys(self.username)
            time.sleep(self.wait())
            self.driver.find_element_by_xpath("//input[@name='password']").send_keys(self.password)
            time.sleep(self.wait(mu=0.6))
            self.driver.find_element_by_xpath("//input[@name='password']").send_keys(Keys.ENTER)
            time.sleep(self.wait())

            # Save Info or Not
            try:
                var_error = self.driver.find_element_by_xpath("//button[contains(.,'保存信息')]").click()
                time.sleep(self.wait())
            except NoSuchElementException:
                pass

            """Check For Invalid Credentials"""
            try:
                var_error = self.driver.find_element_by_class_name('eiCW-').text
                raise ValueError('[!] Invalid Credentials')
            except NoSuchElementException:
                pass

            """Taking cookies"""
            get_cookies = self.driver.get_cookies()
            cookies = {
                cookie['name']: cookie['value']
                for cookie in get_cookies
            }
            print(f"Generated new cookies and save it into {COOKIES_PATH}")
            pickle.dump(cookies, open(COOKIES_PATH,"wb"))

        self.http_base.cookies.update(cookies)

    def dive(self, username: str, max_depth=0, max_width=500, keep_post_jsons=False, depth=0):
        '''
        Browse the TREE of an account (BFS)
        '''
        if depth > max_depth:
            return 
        try:
            user_profile = self.get_profile(username, keep_post_jsons)
        except:
            traceback.print_exc()
            print(f"FAILED: got {username} profile")

        COND_FOLLOWERS = user_profile.n_followers > 2000 and user_profile.n_followers < 50000
        COND_LIKES = True
        COND_COMMENTS = True

        if COND_FOLLOWERS and COND_LIKES and COND_COMMENTS: 
            self.info_list.append(user_profile)
            info_df = pd.DataFrame([user_profile])
            info_df.to_csv(SAVE_FILE_NAME, mode='a', index=False)

            followers = self.scrape_followers(username, max_width)
            print(f"Got followers: \n{followers}")
            for f in followers:
                try:
                    self.dive(f, max_depth, depth = depth+1)
                except PrivateException:
                    print(PrivateException)
                except Exception as e:
                    print(e)


if __name__ == "__main__":
    # unit test
    root_username='beatrizcorbett'
    ib = InstagramBot(account)
    ib.sign_in()
    ib.dive(root_username, 2, 50, keep_post_jsons=False)
    
    # ib.get_profile(root_username)
