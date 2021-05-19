from typing import List

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

from src.profile import ins_profile

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
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(5)

        self.http_base = requests.Session()

        self.username = account['username']
        self.password = account['password']

        with open(r'filter.yml') as file:
            self.filter = yaml.full_load(file)
    
    def wait(self, mu = 2, sigma = 0.5):
        # random wait time to avoid being blocked
        t = random.normal(mu, sigma,1)[0]
        if t <= 0:
            return 0.1
        else:
            return t

    def check_availability(self, username) -> None:
        """
        Checking Status code, Taking number of posts, Privacy and followed by viewer
        Raise Error if the Profile is private and not following by viewer
        :return: None
        """
        search = self.http_base.get(f'https://www.instagram.com/{username}/', params={'__a': 1})
        search.raise_for_status()

        load_and_check = search.json()
        n_posts = load_and_check.get('graphql').get('user').get('edge_owner_to_timeline_media').get('count')
        n_followers = load_and_check.get('graphql').get('user').get('edge_followed_by').get('count')
        n_following = load_and_check.get('graphql').get('user').get('edge_follow').get('count')
        privacy = load_and_check.get('graphql').get('user').get('is_private')
        followed_by_viewer = load_and_check.get('graphql').get('user').get('followed_by_viewer')
        if privacy and not followed_by_viewer:
            raise PrivateException(f'[!] Account is private: {username}')
        return n_posts, n_followers, n_following
    
    def get_post_link(self, username) -> None:
        url = f'https://www.instagram.com/{username}/'
        self.driver.get(url)
        action = ActionChains(self.driver)
        elements = self.driver.find_elements_by_xpath('//a[@href]')
        post_links = []
        n_likes = []
        n_comments = []
        for elem in elements:
            urls = elem.get_attribute('href')
            if 'p' in urls.split('/'):
                action.move_to_element(elem).perform()
                post_links.append(urls)
                temp_likes, temp_comments = elem.find_element_by_class_name('qn-0x').text.split('\n')
                n_likes.append(temp_likes)
                n_comments.append(temp_comments)
        return post_links, n_likes, n_comments

    def get_profile(self, username) -> None:
        """Taking hrefs while scrolling down"""
        n_posts, n_followers, n_following = self.check_availability(username)
        print(f"Analyzing account: {username} with {n_followers} followers")
        post_links, n_likes, n_comments = self.get_post_link(username)
        self.wait(1)
        self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        self.wait(1)
        print(f'[*] extracting {len(post_links)} posts jsons string, please wait...'.title())
        new_links = [urllib.parse.urljoin(link, '?__a=1') for link in post_links]
        post_jsons = [self.http_base.get(link.split()[0]).json() for link in new_links]
        return None

    def signIn(self):
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
        self.driver.find_element_by_xpath("//button[contains(.,'保存信息')]").click()
        time.sleep(self.wait())

        """Check For Invalid Credentials"""
        try:
            var_error = self.driver.find_element_by_class_name('eiCW-').text
            raise ValueError('[!] Invalid Credentials')
        except NoSuchElementException:
            pass

        """Taking cookies"""
        cookies = {
            cookie['name']: cookie['value']
            for cookie in self.driver.get_cookies()
        }
        self.http_base.cookies.update(cookies)

    def dive(self, username: str, depth=0, max_depth=0, max_width=500):
        if depth > max_depth:
            return 
        self.get_profile(username)
        followers = self.get_followers(username, max_width)
        for f in followers:
            try:
                self.dive(f, depth+1, max_depth)
            except PrivateException:
                print(PrivateException)

    def get_followers(self, username: str, max_width: int = 500):
        url = f'https://www.instagram.com/{username}/'
        self.driver.get(url)
        followersLink = self.driver.find_element_by_xpath("(//a[@class='-nal3 '])[2]")
        followersLink.click()
        self.wait()
        followersList = self.driver.find_element_by_xpath("//div[@role='dialog']")
        num = len(followersList.find_elements_by_css_selector('li'))

        followersList.click()
        actionChain = webdriver.ActionChains(self.driver)
        while (num < max_width):
            actionChain.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
            num += len(followersList.find_elements_by_css_selector('li'))
            print(num)
        
        followers = []
        for user in followersList.find_elements_by_css_selector('li'):
            userLink = user.find_element_by_css_selector('a').get_attribute('href')
            print(userLink)
            followers.append(userLink.split('/')[-2])
            if (len(followers) == max_width):
                break

        return followers


if __name__ == "__main__":
    root_username='nba'
    ib = InstagramBot(account)
    ib.signIn()
    ib.dive(root_username, 0, 2, 50)
    # ib.get_profile(root_username)
