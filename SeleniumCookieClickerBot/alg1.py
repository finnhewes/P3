#   Below is my first attempt at a cookie clicker algorithm. Seeing how many cookies per second we can reach in 5 mins!
#   This attempt buys the most expensive available upgrade after each 250 clicks... 
#   My C/S score for this attempt was 57.6... Mediocre at best!

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import selenium.common.exceptions
import time

###############################################################################################

s=Service("/Users/finnhewes/Developing/chromedriver")
browser = webdriver.Chrome(service=s)
browser.get("http://orteil.dashnet.org/experiments/cookie/")

###############################################################################################

cookie = browser.find_element(By.ID, "cookie")      # finds cookie item to click on
store_items = browser.find_elements(By.CSS_SELECTOR, "#store div")    #  a list of all upgrades in the store
item_ids = [item.get_attribute("id") for item in store_items]       #  a list of the upgrades' individual item ids

five_min = time.time() + 60*5 # AFTER this five minutes has elapsed, we will stop clicking and print out cookies/sec

# rather than timing my upgrade purchases based on time elapsed, I'm timing based on clicks, which should occur at a
# somewhat constant rate...
click_count = 0
keep_going = True
while keep_going:
    cookie.click()
    click_count += 1
    # every 250 clicks, we will buy all the upgrades we can afford, starting with the most expensive.
    if click_count%250 == 0:
        # getting our "cash", or cookies we can spend, and converting to an int
        cash = browser.find_element(By.ID, "money").text
        try:
            cash = int(cash)
        except ValueError:
            cash = int(cash.replace(",", ""))       # catches any values greater than 3 place values & removes commas

        bs = browser.find_elements(By.CSS_SELECTOR, "#store b")  # singles out all the B tags in the store first
        item_prices = []
        # Convert <b> text into an integer price.
        for those in bs:
            element_text = those.text
            # catching empty elements
            if element_text != "":
                # the line below removes the item name & any commas in its price, then converts num string to int
                price = int(element_text.split("-")[1].strip().replace(",", ""))
                # and saves to our item_prices list
                item_prices.append(price)

        # Create dictionary of store items and prices from previously created lists
        all_upgrades = {}
        for n in range(len(item_prices)):
            all_upgrades[item_prices[n]] = item_ids[n]

        available_upgrades = {}
        for cost, id in all_upgrades.items():
            if cost < cash:
                available_upgrades[cost] = id

        try:
            most_expensive_available = max(available_upgrades)
            id_to_buy = available_upgrades[most_expensive_available]
            browser.find_element(By.ID, id_to_buy).click()
        except ValueError:
            pass


    #After 5 minutes stop the bot and check the cookies per second count.
    if time.time() > five_min:
        cookie_per_s = browser.find_element(By.ID, "cps").text
        print(cookie_per_s)
        break
