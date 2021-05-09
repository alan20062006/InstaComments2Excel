from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import traceback
import yaml
import numpy.random as random

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

        self.username = account['username']
        self.password = account['password']
    
    def wait(self, mu = 2, sigma = 0.5):
        # random wait time to avoid being blocked
        t = random.normal(mu, sigma,1)[0]
        if t <= 0:
            return 0.1
        else:
            return t
    
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

    def dive(self, username: str, depth=0, max_depth=0, max_width=500):
        if depth > max_depth:
            return 
        self.get_profile(username)
        followings = self.get_followings(username, max_width)
        for f in followings:
            self.dive(f"https://www.instagram.com/{f}/", depth+1, max_depth)

    
    def get_profile(self, username: str):
        url = f'https://www.instagram.com/{username}/'
        return
        self.driver.get(root_url)


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
            import pdb;pdb.set_trace()
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
    ib.dive('jacqueline.xiaowang', 0, 0, 50)
