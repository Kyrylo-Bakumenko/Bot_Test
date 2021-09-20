from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import numpy as np

# hiding selenium: hiding driver ###
option = webdriver.ChromeOptions()

# Removes navigator.webdriver flag
# For ChromeDriver version 79.0.3945.16 or over
option.add_argument('--disable-blink-features=AutomationControlled')
# Add Proxy
# option.add_argument('proxy-server=216.21.18.193:80')

# Open Browser
PATH = "C:\Program Files (x86)\chromedriver_win32\chromedriver.exe"  # driver path
driver = webdriver.Chrome(executable_path=PATH, options=option)

# hiding selenium: hiding JavaScript ###
# done by renaming variable "$cdc_asdjflasutopfhvcZLmcfl_" in .exe driver file
# changed to variable of same length "$cdc_tlwcyetlnmhiyaovSEfvye_"

# Constants, censored for git
PERSONAL_INFO = ["Kyrylo", "Bakumenko", "## Example Ave", "City", "#####", "kyrylobakumenko@gmail.com", "###-###-####"]
ADDRESS_SUFFIXES = [".firstName", ".lastName", ".street", ".city", ".zipcode"]

# driver.delete_all_cookies()  # delete all cookies
# go to best buy cart (avoids pop-up at main site)
driver.get("https://www.bestbuy.com")
# driver.get("https://www.bestbuy.com/cart")
# find and save search bar into search
search = driver.find_element_by_id("gh-search-input")
# search for item
search.send_keys("dog")
search.send_keys(Keys.ENTER)
clickRandomDelay = 10

# test link clicking
try:
    # wait for item list to load
    item_list = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "sku-item"))
    )
    # save items into list
    items = item_list.find_elements_by_class_name("sku-item")
    # for every item in list find stock, product name, and price
    for item in items:
        stock = item.find_element_by_class_name("fulfillment-add-to-cart-button")
        header = item.find_element_by_class_name("sku-header")
        price = item.find_elements_by_class_name("sr-only")[-1]
        print("Card: ", header.text,
              "\nPrice: ", re.sub("[^(0-9.)]", '', price.text),
              "\nStock: ", stock.text)
        # if item is in stock, add to cart.
        # Otherwise continue
        if stock.text == "Add to Cart":
            button = stock.find_element_by_tag_name("button")
            time.sleep(clickRandomDelay*np.random.random())
            button.click()
            # exit to finalize purchase
            break
    # got to cart
    driver.get("https://www.bestbuy.com/cart")
    # click shipping
    # try:
    #     # wait for shipping button to load
    #     shipping = WebDriverWait(driver, 10).until(
    #         EC.presence_of_element_located((By.CLASS_NAME, "c-radio-brand"))
    #     )
    #     # find shipping button
    #     shipping_button = shipping.find_element_by_tag_name("input")
    #     # switch to shipping
    #     shipping_button.click()
    #     # attempt to check out
    try:
        # wait for checkout button to load
        checkout = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "checkout-buttons"))
        )
        # find checkout button
        checkout_button = checkout.find_element_by_tag_name("button")
        # click to checkout
        checkout_button.click()
        time.sleep(clickRandomDelay*np.random.random())
        # continue as guest
        try:
            checkout = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "button-wrap"))
            )
            # find guest checkout button
            checkout_button = checkout.find_element_by_tag_name("button")
            # click to checkout
            checkout_button.click()
            time.sleep(clickRandomDelay*np.random.random())
            try:
                # find switch checkout button
                switch = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "fulfillment"))
                )
                # find switch checkout button
                switch = switch.find_element_by_class_name("ispu-card__switch")
                # toggle to shipping page if not already
                if "Shipping" in switch.text:
                    switch.click()
                    time.sleep(clickRandomDelay*np.random.random())
                # now fill in information
                try:
                    blanks = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "clearFloat"))
                    )
                    if driver.page_source.__contains__("consolidatedAddresses.ui_address_2.firstName"):
                        address_path = "consolidatedAddresses.ui_address_2"
                    elif driver.page_source.__contains__("consolidatedAddresses.ui_address_1153.firstName"):
                        address_path = "consolidatedAddresses.ui_address_1153"
                    else:
                        print("No suitable key found")
                        pass
                    # find all blanks:
                    # First Name, Last Name, Address, City, ZIP Code, Email Address, Phone Number
                    #   0           1           2       3       4           5           6

                    # iterate over every field and input information as needed
                    # five fields with direct id
                    for i in range(5):
                        field = blanks.find_elements_by_id(address_path + ADDRESS_SUFFIXES[i])
                        field.send_keys(PERSONAL_INFO[i])
                    time.sleep(30)
                except:
                    print("Failed Form Input")
                    driver.quit()
            except:
                driver.quit()
        except:
            print("Failed Guest Checkout")
            driver.quit()
        # except:
        #     driver.quit()
    except:
        print("Failed Checkout Button")
        driver.quit()
except:
    print("Failed Item List")
    driver.quit()

# search.send_keys("rtx 3060 ti")
# search.send_keys(Keys.RETURN)
# # find GPU info
# try:
#     item_list = WebDriverWait(driver, 5).until(
#         EC.presence_of_element_located((By.CLASS_NAME, "sku-item-list"))
#     )
#     items = item_list.find_elements_by_class_name("sku-item")
#     for item in items:
#         header = item.find_element_by_class_name("sku-header")
#         price = item.find_elements_by_class_name("sr-only")[-1]
#         stock = item.find_element_by_class_name("fulfillment-add-to-cart-button")
#         print("Card: ", header.text,
#               "\nPrice: ", re.sub("[^(0-9.)]", '', price.text),
#               "\nStock: ", stock.text)
#
# except:
#     driver.quit()
