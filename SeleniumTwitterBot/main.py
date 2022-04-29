from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
import datetime
CHROME_DRIVER_PATH = YOUR_DRIVER_PATH
TWITTER_EMAIL = YOUR_TWITTER_LOGIN
TWITTER_PASSWORD = YOUR_TWITTER_PASSWORD
TWITTER_URL = "https://twitter.com/i/flow/login"
# url to find the daily prayer times for istanbul below, as that's where I wrote this script. 
PT_URL = "https://www.google.com/search?q=PRAYER+TIMES+ISTANBUL&oq=PRAYER+TIMES+ISTANBUL&aqs=chrome..69i57j69i60.2572j0j4&sourceid=chrome&ie=UTF-8"
s = Service(CHROME_DRIVER_PATH)
browser = webdriver.Chrome(service=s)
###############################################################################################
    # Get Adhan Times from Google
browser.get(PT_URL)
adhan_times = {}
adhan_times["fajr"] = browser.find_element(By.XPATH, '//*[@id="rso"]/div[1]/block-component/div/div[1]/div/div/div/div[1]/div/div/div/div/div[2]/div[2]/div[2]/table/tbody/tr[2]/td[1]/div').text
adhan_times["sunrise"] = browser.find_element(By.XPATH, '//*[@id="rso"]/div[1]/block-component/div/div[1]/div/div/div/div[1]/div/div/div/div/div[2]/div[2]/div[2]/table/tbody/tr[2]/td[2]/div').text
adhan_times["dhuhr"] = browser.find_element(By.XPATH, '//*[@id="rso"]/div[1]/block-component/div/div[1]/div/div/div/div[1]/div/div/div/div/div[2]/div[2]/div[2]/table/tbody/tr[2]/td[3]/div').text
adhan_times["asr"] = browser.find_element(By.XPATH, '//*[@id="rso"]/div[1]/block-component/div/div[1]/div/div/div/div[1]/div/div/div/div/div[2]/div[2]/div[2]/table/tbody/tr[2]/td[4]/div').text
adhan_times["maghrib"] = browser.find_element(By.XPATH, '//*[@id="rso"]/div[1]/block-component/div/div[1]/div/div/div/div[1]/div/div/div/div/div[2]/div[2]/div[2]/table/tbody/tr[2]/td[5]/div').text
adhan_times["isha"] = browser.find_element(By.XPATH, '//*[@id="rso"]/div[1]/block-component/div/div[1]/div/div/div/div[1]/div/div/div/div/div[2]/div[2]/div[2]/table/tbody/tr[2]/td[6]/div').text
###############################################################################################
now = datetime.datetime.now().strftime(f"%H:%M")  # get/format the current time (hours:mins)

for key in adhan_times:   # loop through dictionary of adhan times
    if adhan_times[key] == now:   # if any of the values in the dict match the current time (eg. they're now doing the call to prayer):
            # Log in to Twitter
        browser.get(TWITTER_URL)  # open twitter
        time.sleep(2)  # quick pause to let things load
        # find email input
        email_input = browser.find_element(By.XPATH, '//input[@autocomplete="username"]')
        email_input.send_keys(TWITTER_EMAIL)  # input email address
        # find and click 'next' button
        browser.find_element(By.XPATH,'//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[6]/div').click()
        time.sleep(2)  # pause to let things load
        try:  # see if we need to further verify our identity...
            additional_input = browser.find_element(By.XPATH, '//input[@inputmode="text"]')
            additional_input.send_keys("disgruntledint2")  # additional username verification
            additional_input.send_keys(Keys.ENTER)  # bypass finding the "next" button to click on
            time.sleep(2)  # pause to let things load
        except NoSuchElementException:
            pass
        password_input = browser.find_element(By.XPATH, '//input[@name="password"]')  # find password input
        password_input.send_keys(TWITTER_PASSWORD)  # input password
        password_input.send_keys(Keys.ENTER)  # bypass finding the "login" button to click on
        time.sleep(2)  # pause to let things load up
        # Draft Tweet
        tweet_input_box = browser.find_element(By.XPATH, '//div[@data-block="true"]')
        tweet_input_box.click()
        tweet_input_box.send_keys("They're singing again...") # my disgruntled message re: the adhan
        # Send Tweet
        send_tweet_button = browser.find_element(By.XPATH, '//div[@data-testid="tweetButtonInline"]/div/span')
        send_tweet_button.click()
        print("Tweet sent.")  # print confirmation

browser.quit()
