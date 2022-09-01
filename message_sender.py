from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time


def check_message_button(follower, class_name="friends_field_act"):
    try:
        follower.find_element(By.CLASS_NAME, "friends_user_info_actions").\
            find_element(By.CLASS_NAME, class_name)
        print("There is an opportunity to send message!")
    except NoSuchElementException:
        return False
    return True


def send_message(driver, follower, message):
    if check_message_button(follower):
        message_button = follower.find_element(By.CLASS_NAME, "friends_user_info_actions").\
            find_element(By.CLASS_NAME, "friends_field_act")
        driver.execute_script("arguments[0].click();", message_button)

        time.sleep(3)

        mail_box = driver.find_element(By.CLASS_NAME, "box_layout").\
            find_element(By.ID, "mail_box_editable")
        mail_box.send_keys(message)

        # send_button = driver.find_element(By.CLASS_NAME, "box_layout").\
        #     find_element(By.ID, "mail_box_controls").find_element(By.ID, "mail_box_send")
        # driver.execute_script("arguments[0].click();", send_button)
        # mail_box.submit()

        # time.sleep(3)
        #
        x_button = driver.find_element(By.CLASS_NAME, "box_x_button")
        driver.execute_script("arguments[0].click();", x_button)


messages = {"group_A_message": "[ТЕСТ]Это сообщение отправлено от лица пользователя этой странички.\n"
                               "И если вы блять это видите, то все заебись.",
            "group_B_message": "[ТЕСТ]Уже чуть более официальное сообщение чем было отправлено другой группе."}


