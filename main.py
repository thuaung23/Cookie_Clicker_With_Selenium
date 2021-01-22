from selenium import webdriver
import time

URL = "http://orteil.dashnet.org/experiments/cookie/"
chrome_path = "YOUR_CHROME_DRIVER_PATH"

driver = webdriver.Chrome(chrome_path)
driver.get(URL)
# Get cookie to click on.
cookie = driver.find_element_by_css_selector("#cookie")
# Get a list of upgradable items.
items = [item.get_attribute("id") for item in driver.find_elements_by_css_selector("#store div")]

time_out = time.time() + 5  # 5s
game_over = time.time() + 60 * 5  # 5 mins

while True:
    cookie.click()

    # Check if time is at 5s.
    if time.time() > time_out:
        # Get all tag to get prices.
        all_prices = driver.find_elements_by_css_selector("#store b")
        item_prices = []
        # Change all prices into int and add to item_prices list.
        for price in all_prices:
            element_text = price.text
            if element_text != "":
                cost = int(element_text.split("-")[1].strip().replace(",", ""))
                item_prices.append(cost)

        # Create dict to store items and their prices.
        cookies_upgrade = {}
        for n in range(len(item_prices)):
            cookies_upgrade[item_prices[n]] = items[n]

        # Get the cookie count under id="money".
        money_element = driver.find_element_by_id("money").text
        # Strip any commas if there are any and change the count into an int.
        if "," in money_element:
            money_element = money_element.replace(",", "")
        cookie_count = int(money_element)

        # Get an affordable item that can be currently purchase with available cookie count.
        affordable_upgrades = {}
        for cost, _id in cookies_upgrade.items():
            if cookie_count > cost:
                affordable_upgrades[cost] = _id

        # Buy the most affordable item.
        highest_price_affordable_upgrade = max(affordable_upgrades)
        print(highest_price_affordable_upgrade)
        to_purchase_id = affordable_upgrades[highest_price_affordable_upgrade]
        driver.find_element_by_id(to_purchase_id).click()
        # Add 5s until next check.
        time_out = time.time() + 5

    # Check if time passes 5 mins.
    if time.time() > game_over:
        # Get cookie/s count and print it.
        score = driver.find_element_by_css_selector("#cps").text
        print(score)
        break
