from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from auth_data import auth_data
import time
from selenium.webdriver.chrome.service import Service as ChromeService

# from webdriver_manager.chrome import ChromeDriverManager


options = Options()
options.add_argument("start-maximized")
driver = webdriver.Chrome(executable_path="driver\\chromedriver.exe", chrome_options=options)

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


def check_by_id(driver, id):
    try:
        driver.find_element(By.ID, id)
    except NoSuchElementException:
        return False
    return True


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


def get_followers_lst(driver, actions, count):
    try:
        followers_link = driver.find_element(By.ID, "public_followers"). \
            find_element(By.TAG_NAME, "a")
        actions.key_down(Keys.CONTROL).click(followers_link).key_up(Keys.CONTROL).perform()
    except Exception:
        try:
            followers_link = driver.find_element(By.ID, "group_followers"). \
                find_element(By.TAG_NAME, "a")
            actions.key_down(Keys.CONTROL).click(followers_link).key_up(Keys.CONTROL).perform()
        except NoSuchElementException:
            print("The public is closed")
    driver.switch_to.window(driver.window_handles[count])

    time.sleep(3)
    followers = auth_driver.find_element(By.CLASS_NAME, "search_results")
    print(len(followers.find_elements(By.CLASS_NAME, "people_row")))
    last_follower = followers.find_elements(By.CLASS_NAME, "people_row")[-1]

    if check_by_id(driver, "ui_search_load_more"):
        print("more than 40")
        while True:
            page_end = followers.find_element(By.ID, "ui_search_load_more")
            actions = ActionChains(auth_driver)
            if page_end:
                actions.move_to_element(page_end).perform()
            else:
                break
            time.sleep(7)
            followers = driver.find_element(By.CLASS_NAME, "search_results")
            if followers.find_elements(By.CLASS_NAME, "people_row")[-1] == last_follower:
                break
            else:
                last_follower = followers.find_elements(By.CLASS_NAME, "people_row")[-1]
        followers = followers.find_elements(By.CLASS_NAME, "people_row")
    else:
        print("less than 40")
        followers = get_whole_page("search_results", "people_row")

    driver.switch_to.window(auth_driver.window_handles[0])
    driver.back()
    time.sleep(3)

    return followers


def parse_groups(groups, driver):
    count = 1
    for index, group in enumerate(groups):
        actions = ActionChains(driver)
        if index in [4, 5]:

            group_info = group.find_element(By.CLASS_NAME, "group_row_info")
            group_link = group_info.find_element(By.TAG_NAME, "a")
            # print(group_link)
            driver.execute_script("arguments[0].click();", group_link)
            time.sleep(7)

            followers = get_followers_lst(driver, actions, count)
            time.sleep(7)
            # print(len(followers))
            count += 1


if __name__ == "__main__":
    auth_driver = authorization()
    groups = get_group_lst(auth_driver)
    print(len(groups))
    parse_groups(groups, auth_driver)

    auth_driver.get_screenshot_as_file("test_screen.jpg")
    auth_driver.close()
    auth_driver.quit()
