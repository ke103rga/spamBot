import sqlite3 as sql
from selenium.webdriver.common.by import By


def create_data_base(data_base_name="users.db"):
    con = sql.connect(data_base_name)
    with con:
        cur = con.cursor()
        cur.execute(
            "CREATE TABLE IF NOT EXISTS `groups` (group_id INTEGER PRIMAREKEY, group_name VARCHAR(50), group_link "
            "VARCHAR(30))")
        con.commit()

        cur.execute("CREATE TABLE IF NOT EXISTS `users` (user_id INTEGER PRIMAREKEY AUTO_INCREMENT, group_id INTEGER "
                    "FOREIGNKEY, "
                    "user_name VARCHAR(50), user_link VARCHAR(30))")
        con.commit()


def insert_group_data(driver, cur, con,  count):
    group_data = {"name": driver.find_element(By.CLASS_NAME, "page_top"). \
        find_element(By.CLASS_NAME, "page_name").text, "link": driver.current_url}

    cur.execute("INSERT INTO 'groups' (group_id, group_name, group_link)"
                f"({count}, {group_data['name'], group_data['link']})")

    con.commit()


def insert_user_data(follower, cur, con, count):
    follower_info = follower.find_element(By.CLASS_NAME, "labeled name")

    user_data = {"name": follower_info.text,
                 "link": follower_info.get_attribute("href")}

    cur.execute("INSERT INTO 'users' (group_id, user_name, user_link)"
                f"({count}, {user_data['name'], user_data['link']})")

    con.commit()