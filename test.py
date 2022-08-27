from group_parser import authorization, get_group_lst
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import time

options = Options()
options.add_argument("start-maximized")
driver = webdriver.Chrome(executable_path="C:\\Users\\Анастасия\\PycharmProjects\\spamBot\\driver\\chromedriver.exe", chrome_options=options)
auth_driver = authorization(driver=driver)

groups = get_group_lst(auth_driver)
first_group = groups[136]

group_info = first_group.find_element(By.CLASS_NAME, "group_row_info")
group_link = group_info.find_element(By.TAG_NAME, "a")
driver.execute_script("arguments[0].click();", group_link)
time.sleep(7)

try:
    followers_link = auth_driver.find_element(By.ID, "public_followers"). \
        find_element(By.TAG_NAME, "a")
    auth_driver.execute_script("arguments[0].click();", followers_link)
except Exception:
    followers_link = auth_driver.find_element(By.ID, "group_followers"). \
        find_element(By.TAG_NAME, "a")
    auth_driver.execute_script("arguments[0].click();", followers_link)

time.sleep(3)

followers = driver.find_element(By.CLASS_NAME, "fans_rows")
last_follower = followers.find_elements(By.CLASS_NAME, "fans_fan_row")[-1]

while True:
    page_end = driver.find_element(By.ID, "fans_more_linkmembers")
    actions = ActionChains(driver)
    actions.move_to_element(page_end).perform()
    time.sleep(7)
    # groups = driver.find_element(By.ID, "groups_list_groups")
    followers = driver.find_element(By.CLASS_NAME, "fans_rows")
    if followers.find_elements(By.CLASS_NAME, "fans_fan_row")[-1] == last_follower:
        break
    else:
        last_follower = followers.find_elements(By.CLASS_NAME, "fans_fan_row")[-1]

print(len(followers.find_elements(By.CLASS_NAME, "fans_fan_row")))

driver.quit()
driver.close()
