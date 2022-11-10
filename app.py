from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager as CM

import os
import time


#fill these fields -------------------------------
USERNAME = '' #your IG username
PASSWORD = '' #your IG password

USR = '' #use to be scraped
PAGE = "" #scrape following or followers
#-------------------------------------------------

TIMEOUT = 10

options = Options()
# options.add_argument("--headless")
# options.add_argument('--no-sandbox')
options.add_argument("--log-level=3")
options.add_argument('--user-agent="Mozilla/5.0 (iPhone; CPU iPhone OS 13_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Mobile/15E148 Safari/604.1"')
""" prefs = {"profile.managed_default_content_settings.images":2,
         "profile.default_content_setting_values.notifications":2,
         "profile.managed_default_content_settings.stylesheets":2,
         "profile.managed_default_content_settings.javascript":1,
         "profile.managed_default_content_settings.plugins":1,
         "profile.managed_default_content_settings.popups":2,
         "profile.managed_default_content_settings.geolocation":2,
         "profile.managed_default_content_settings.media_stream":2,
}
options.add_experimental_option("prefs",prefs) """

driver = webdriver.Chrome(service=Service(CM().install()), options=options)
driver.set_window_size(428, 926)
driver.get('https://www.instagram.com/accounts/login/')

time.sleep(0.27)

#allow cookies
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Only allow essential cookies")]'))).click()

print("[Info] - Logging in...")

#input username
username = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
username.clear()
username.send_keys(USERNAME)

#input password
password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))
password.clear()
password.send_keys(PASSWORD)

#login
WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()

#dismiss pop-ups
WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not Now')]"))).click()
#WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Cancel')]"))).click()
#WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not Now')]"))).click()

print("[Info] - Searching for the user...")

time.sleep(0.8)

#go to user page
driver.get('https://www.instagram.com/{}/'.format(USR))

#time.sleep(4.65)

#WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//a[contains(@href, "%s")]' % PAGE))).click()

#followers = driver.find_element("xpath", '//div[contains(text(), "followers")]/span')
#following = driver.find_element("xpath", '//div[contains(text(), "following")]/span')

followers = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[contains(text(), "followers")]/span')))
following = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[contains(text(), "following")]/span')))

followers_count = int(followers.text)
following_count = int(following.text)

followers.click()
time.sleep(1.08)

print('[Info] - Scraping...')

print(followers_count)
print(following_count)

time.sleep(3)

for i in range(1, followers_count):
    #scr1 = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/section/main/div/div/div/div[%s]" % i)
    scr1 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/section/main/div/div/div/div[%s]' % i)))    
    driver.execute_script("arguments[0].scrollIntoView();", scr1)
    time.sleep(0.01)
    text = scr1.text
    #print(text)
    list = text.split()
    dirname = os.path.dirname(os.path.abspath(__file__))
    csvfilename = os.path.join(dirname, USR + "-" + PAGE + ".txt")
    file_exists = os.path.isfile(csvfilename)
    f = open(csvfilename,'a')
    f.write(str(list[0]) + "\n")
    f.close()
    print('{}, {}'.format(i, list[0]))


""" for i in range(1,500):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    list_of_followers = driver.find_elements(By.XPATH, "//a[role='link']/span")
    print(list_of_followers)

new_list_of_followers = []
for i in list_of_followers:
    new_list_of_followers.append(i.text.split()[0])

print(new_list_of_followers) """

#driver.quit()


""" 
/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/section/main/div/div/div/div[7]/div[2]/div/div/div/a/span
/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/section/main/div/div/div/div[33]/div[2]/div/div/div/a/span
/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/section/main/div/div/div/div[1]/div[2]/div/div/div/a/span
/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/section/main/div/div/div/div[%s]/div[2]/div/div/div/a/span 
"""