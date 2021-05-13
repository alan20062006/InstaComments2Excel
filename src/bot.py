from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
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
        self.posts = load_and_check.get('graphql').get('user').get('edge_owner_to_timeline_media').get('count')
        privacy = load_and_check.get('graphql').get('user').get('is_private')
        followed_by_viewer = load_and_check.get('graphql').get('user').get('followed_by_viewer')
        if privacy and not followed_by_viewer:
            raise PrivateException(f'[!] Account is private: {username}')
    
    def scroll_down(self) -> None:
        """Taking hrefs while scrolling down"""
        while len(list(set(self.links))) < self.posts:
            self.get_href()
            self.wait(1)
            self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            self.wait(1)
        self.submit_links()
        return None

    def submit_links(self) -> None:
        """Gathering Images and Videos and pass to function <fetch_url> Using ThreadPoolExecutor"""
        self.control()
        links = list(set(self.links))

        print('[!] Ready for video - images'.title())
        print(f'[*] extracting {len(links)} posts , please wait...'.title())

        new_links = [urllib.parse.urljoin(link, '?__a=1') for link in links]
        [self.fetch_url(link) for link in new_links]

    def fetch_url(self, url: str) -> None:
        """
        This function extracts images and videos
        :param url: Taking the url
        :return None
        """

        logging_page_id = self.http_base.get(url.split()[0]).json()
        try:
            """Taking Gallery Photos or Videos"""
            for log_pages in logging_page_id['graphql']['shortcode_media']['edge_sidecar_to_children']['edges']:
                video = log_pages['node']['is_video']
                if video:
                    video_url = log_pages['node']['video_url']
                    self.videos.append(video_url)
                else:
                    image = log_pages['node']['display_url']
                    self.pictures.append(image)

        except KeyError:
            """Unique photo or Video"""
            image = logging_page_id['graphql']['shortcode_media']['display_url']
            self.pictures.append(image)

            if logging_page_id['graphql']['shortcode_media']['is_video']:
                videos = logging_page_id['graphql']['shortcode_media']['video_url']
                self.videos.append(videos)

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
        self.driver.find_element_by_xpath("//button[contains(.,'Save Info')]").click()
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
        self.check_availability(username)
        self.get_profile(username)
        followings = self.get_followings(username, max_width)
        for f in followings:
            try:
                self.dive(f"https://www.instagram.com/{f}/", depth+1, max_depth)
            except PrivateException:
                print(PrivateException)

    def filter_out(self):
        pass

    def get_profile(self, username: str):
        url = f'https://www.instagram.com/{username}/'
        self.driver.get(url)
        post=self.driver.find_element_by_xpath("(//li[@class='Y8-fY '])[1]").find_element_by_tag_name('span')
        followings=self.driver.find_element_by_xpath("(//a[@class='-nal3 '])[2]").find_element_by_tag_name('span').text
        followers=self.driver.find_element_by_xpath("(//a[@class='-nal3 '])[1]").find_element_by_tag_name('span').text
        import pdb;pdb.set_trace()


    def get_followings(self, username: str, max_width: int = 500):
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
    ib = InstagramBot(account)
    ib.signIn()
    ib.dive('wefluens', 0, 0, 50)
