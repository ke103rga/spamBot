from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from auth_data import auth_data
import time
from selenium.webdriver.chrome.service import Service as ChromeService
# from webdriver_manager.chrome import ChromeDriverManager


options = Options()
options.add_argument("start-maximized")
driver = webdriver.Chrome(executable_path="C:\\Users\\Анастасия\\PycharmProjects\\spamBot\\driver\\chromedriver.exe", chrome_options=options)

vk_url = "https://vk.com/"


def authorization(url=vk_url, driver=driver, auth_data=auth_data):
    driver.get(url)

    email_form = driver.find_element(By.CLASS_NAME, "VkIdForm__form").find_element(By.TAG_NAME, "input")
    email_form.send_keys(auth_data["email"])
    email_form.submit()
    time.sleep(5)

    email_form = driver.find_element(By.CLASS_NAME, "vkc__Password__Wrapper").find_element(By.TAG_NAME, "input")
    email_form.send_keys(auth_data["password"])
    email_form.submit()
    time.sleep(5)

    return driver


def get_whole_page(group_class_name, last_elem_classs_name):
    groups = driver.find_element(By.CLASS_NAME, group_class_name)
    last_group = groups.find_elements(By.CLASS_NAME, last_elem_classs_name)[-1]

    while True:
        actions = ActionChains(driver)
        actions.move_to_element(last_group).perform()
        time.sleep(7)
        # groups = driver.find_element(By.ID, "groups_list_groups")
        groups = driver.find_element(By.CLASS_NAME, group_class_name)
        if groups.find_elements(By.CLASS_NAME, last_elem_classs_name)[-1] == last_group:
            break
        else:
            last_group = groups.find_elements(By.CLASS_NAME, last_elem_classs_name)[-1]

    return groups.find_elements(By.CLASS_NAME, last_elem_classs_name)


def get_group_lst(driver):
    groups_link = driver.find_element(By.ID, "l_gr").find_element(By.TAG_NAME, "a")
    groups_link.click()
    time.sleep(7)
    return get_whole_page("groups_list", "group_list_row")

    # groups = driver.find_element(By.CLASS_NAME, "groups_list")
    # last_group = groups.find_elements(By.CLASS_NAME, "group_list_row")[-1]
    #
    # while True:
    #     actions = ActionChains(driver)
    #     actions.move_to_element(last_group).perform()
    #     time.sleep(7)
    #     # groups = driver.find_element(By.ID, "groups_list_groups")
    #     groups = driver.find_element(By.CLASS_NAME, "groups_list")
    #     if groups.find_elements(By.CLASS_NAME, "group_list_row")[-1] == last_group:
    #         break
    #     else:
    #         last_group = groups.find_elements(By.CLASS_NAME, "group_list_row")[-1]
    #
    # return groups.find_elements(By.CLASS_NAME, "group_list_row")


def get_followers_lst(driver):
    try:
        followers_link = driver.find_element(By.ID, "public_followers"). \
            find_element(By.TAG_NAME, "a")
        driver.execute_script("arguments[0].click();", followers_link)
    except Exception:
        followers_link = driver.find_element(By.ID, "group_followers"). \
            find_element(By.TAG_NAME, "a")
        driver.execute_script("arguments[0].click();", followers_link)

    time.sleep(7)
    # return get_whole_page("fans_rows", "fans_fan_row")

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

    return followers.find_elements(By.CLASS_NAME, "fans_fan_row")


def parse_groups(groups, driver):
    for group in groups:
        group_info = group.find_element(By.CLASS_NAME, "group_row_info")
        group_link = group_info.find_element(By.TAG_NAME, "a")
        driver.execute_script("arguments[0].click();", group_link)
        time.sleep(7)
        followers = get_followers_lst(auth_driver)
        break


if __name__ == "__main__":
    auth_driver = authorization()
    groups = get_group_lst(auth_driver)
    print(len(groups))
    parse_groups(groups, auth_driver)

    auth_driver.get_screenshot_as_file("test_screen.jpg")
    auth_driver.close()
    auth_driver.quit()