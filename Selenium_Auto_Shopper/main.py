from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
##############################################################################

s=Service("/Users/finnhewes/Developing/chromedriver")
browser = webdriver.Chrome(service=s)

# url's to be accessed
three_panel_light_set_withboom_url = "https://www.trendyol.com/deyatech/pro-530-led-video-surekli-isik-3-lu-panel-set-p-91149240?boutiqueId=61&merchantId=108280"
three_panel_light_set_noboom_url = "https://www.trendyol.com/deyatech/youtube-kit-pro-kit-fotograf-ve-video-530-led-surkeli-isik-p-35258545?boutiqueId=61&merchantId=108280"
conv_rate_url = "https://www.google.com/search?q=exchange+rate+usd+to+tl&oq=exchange+rate+&aqs=chrome.0.69i59j69i57j69i61.2515j0j7&sourceid=chrome&ie=UTF-8"
boom_arm_only_url = "https://www.trendyol.com/ada-greenbox/boom-arm-isik-light-stand-softbox-led-microfon-tutucu-p-34218485?boutiqueId=61&merchantId=124728"

# finds the current conversion rate from USD to TRY(Turkish Lira)
browser.get(conv_rate_url)
conversion_rate = float(browser.find_element(By.CLASS_NAME, "a61j6.vk_gy.vk_sh.Hg3mWc").get_attribute("value"))

# creating a dict of prices, so we can access this later
prices = {
    "withboom" : {
        "price": "",
        "price_dollar": "",
    },
    "noboom" : {
        "price": "",
        "price_dollar": "",
    },
    "boomonly": {
        "price": "",
        "price_dollar": "",
    },
}

# finds the price of the three-panel light set WITH the boom arm, and sets its value in the dictionary above
browser.get(three_panel_light_set_withboom_url)
withboom_price = browser.find_element(By.CLASS_NAME, "prc-dsc").text.split()[0]
prices["withboom"]["price"] = browser.find_element(By.CLASS_NAME, "prc-dsc").text.split()[0]
# finds the price of the three-panel light set WITHOUT the boom arm, and sets its value in the dictionary above
browser.get(three_panel_light_set_noboom_url)
noboom_price = browser.find_element(By.CLASS_NAME, "prc-dsc").text.split()[0]
prices["noboom"]["price"] = browser.find_element(By.CLASS_NAME, "prc-dsc").text.split()[0]
# finds the price of a stand-alone boom arm, and sets its value in the dictionary above
browser.get(boom_arm_only_url)
boom_only_price = browser.find_element(By.CLASS_NAME, "prc-dsc").text.split()[0]
prices["boomonly"]["price"] = browser.find_element(By.CLASS_NAME, "prc-dsc").text.split()[0]

# Prices are currently strings. I need to remove the periods the Turks use as place value separators, the way we 'Muricans
# use commas, if any are present (eg. the price is more than 999 lira), and convert the remaining string of digits into
# an int. I'm ignoring partial lira prices, as 1 kuruş (.00 decimal value) amounts to less than 1/10 of a penny.
for each in prices:
    #   catching any prices with periods
    if "." in prices[each]["price"]:
        prices[each]["price"] = int(prices[each]["price"].replace(".", ""))
    #   formatting any prices without periods
    else:
        prices[each]["price"] = int(prices[each]["price"])

    #   I'm now converting prices to USD and rounding to the nearest cent, as my bank accounts/credit cards are all USD
    prices[each]["price_dollar"] = round(prices[each]["price"]/conversion_rate, 2)

print(f"With boom:{prices['withboom']['price']}  ~  ${prices['withboom']['price_dollar']}")
print(f"With boom:{prices['noboom']['price']}  ~  ${prices['noboom']['price_dollar']}")
print(f"With boom:{prices['boomonly']['price']}  ~  ${prices['boomonly']['price_dollar']}")

difference = round(abs((prices['boomonly']['price_dollar'] + prices['noboom']['price_dollar'])-prices['withboom']['price_dollar']), 2)

if (prices['boomonly']['price_dollar'] + prices['noboom']['price_dollar']) < prices['withboom']['price_dollar']:
    print(f"Buy separately! Save yourself ${difference}")
else:
    print(f"Buy the package deal! Save yourself ${difference}")

browser.quit()
