from selenium.webdriver import Keys
from group_parser import get_followers_lst
from group_parser import authorization, get_group_lst
from message_sender import send_message, messages
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
first_group = groups.find_elements(By.CLASS_NAME, "group_list_row")[2]

group_data = {"name": "", "link": ""}

action = ActionChains(auth_driver)
group_info = first_group.find_element(By.CLASS_NAME, "group_row_info")
group_link = group_info.find_element(By.TAG_NAME, "a")
auth_driver.execute_script("arguments[0].click();", group_link)
time.sleep(7)

# try:
#     followers_link = auth_driver.find_element(By.ID, "public_followers"). \
#         find_element(By.TAG_NAME, "a")
#     action.key_down(Keys.CONTROL).click(followers_link).key_up(Keys.CONTROL).perform()
# except Exception:
#     followers_link = auth_driver.find_element(By.ID, "group_followers"). \
#         find_element(By.TAG_NAME, "a")
#     action.key_down(Keys.CONTROL).click(followers_link).key_up(Keys.CONTROL).perform()

followers = get_followers_lst(auth_driver, action)
for follower in followers:
    time.sleep(3)
    follower_info = follower.find_element(By.CLASS_NAME, "labeled")

    user_data = {"name": follower_info.text,
                 "link": follower_info.find_element(By.TAG_NAME, "a").get_attribute("href")}
    print(user_data)
    # send_message(auth_driver, follower, messages["group_A_message"])


auth_driver.close()
auth_driver.quit()
