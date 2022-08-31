from selenium.webdriver import Keys

from group_parser import authorization, get_group_lst
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import time

options = Options()
options.add_argument("start-maximized")
driver = webdriver.Chrome(executable_path="driver\\chromedriver.exe", chrome_options=options)
auth_driver = authorization(driver=driver)

# groups = get_group_lst(auth_driver)
# first_group = groups[136]

groups_link = auth_driver.find_element(By.ID, "l_gr").find_element(By.TAG_NAME, "a")
groups_link.click()
time.sleep(7)
groups = auth_driver.find_element(By.CLASS_NAME, "groups_list")
first_group = groups.find_elements(By.CLASS_NAME, "group_list_row")[8]

action = ActionChains(auth_driver)
group_info = first_group.find_element(By.CLASS_NAME, "group_row_info")
group_link = group_info.find_element(By.TAG_NAME, "a")
auth_driver.execute_script("arguments[0].click();", group_link)
time.sleep(7)

try:
    followers_link = auth_driver.find_element(By.ID, "public_followers"). \
        find_element(By.TAG_NAME, "a")
    action.key_down(Keys.CONTROL).click(followers_link).key_up(Keys.CONTROL).perform()
except Exception:
    followers_link = auth_driver.find_element(By.ID, "group_followers"). \
        find_element(By.TAG_NAME, "a")
    action.key_down(Keys.CONTROL).click(followers_link).key_up(Keys.CONTROL).perform()

auth_driver.switch_to.window(driver.window_handles[1])
time.sleep(3)

auth_driver.close()
time.sleep(3)
auth_driver.switch_to.window(auth_driver.window_handles[0])
time.sleep(3)
auth_driver.back()
time.sleep(3)

auth_driver.close()
auth_driver.quit()
