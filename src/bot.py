from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import traceback
import yaml

with open(r'config.yml') as file:
    account = yaml.full_load(file)

class InstagramBot():
    def __init__(self, account):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(5)

        self.username = account['username']
        self.password = account['password']
    
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
        import pdb;pdb.set_trace()
        self.driver.find_element_by_xpath("//input[@name='username']").send_keys(self.username)
        time.sleep(1)
        self.driver.find_element_by_xpath("//input[@name='password']").send_keys(self.password)
        time.sleep(2)
        self.driver.find_element_by_xpath("//button[contains(.,'Log In')]").click()
        time.sleep(3)

if __name__ == "__main__":
    ib = InstagramBot(account)
    ib.signIn()
