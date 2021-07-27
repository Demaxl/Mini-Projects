from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

PATH = 'chromedriver.exe'
driver = webdriver.Chrome(PATH)
driver.get('https://orteil.dashnet.org/cookieclicker/')

# Maximum number of each product
MAX = 1
CLICKS = 10000 # Number of times to click the big cookie

# This is block the execution of the driver for 5 seconds
driver.implicitly_wait(5) # for the site to load

cookie = driver.find_element_by_id('bigCookie')
count = driver.find_element_by_id('cookies')

actions = ActionChains(driver) # instance of ActionChains that allows us perform various actions

# clicks the cookie element
actions.click(cookie) # adds to the queue but doesnt execute until perform() is called

items = [driver.find_element_by_id(f'product{i}') for i in range(17, -1, -1)]

for i in range(CLICKS):
    actions.perform() # executes the action in the queue
    try:
        curr = int(count.text.split(" ")[0]) # current number of cookies
    except ValueError:
        curr = int(''.join(curr.split(',')))
        
    for item in items:
        try:
            lines = item.text.splitlines()
            product_name, price = lines[0], lines[1]
            owned = lines[2] if len(lines) >= 3 else 0
            try:
                price = int(price)
            except ValueError:
                price = int(''.join(price.split(',')))

            owned = int(owned)
            if curr >= price and owned < MAX:
                upgrade = ActionChains(driver)
                upgrade.move_to_element(item)
                upgrade.click()
                upgrade.perform()

        except IndexError:
            pass
