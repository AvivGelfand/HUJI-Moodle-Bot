import logging
import logging.handlers
import os

import requests

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger_file_handler = logging.handlers.RotatingFileHandler(
    "status.log",
    maxBytes=1024 * 1024,
    backupCount=1,
    encoding="utf8",
)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger_file_handler.setFormatter(formatter)
logger.addHandler(logger_file_handler)

try:
    USERNAME2 = os.environ["USERNAME2"]
except KeyError:
    USERNAME2 = "Token not available!"
    # logger.info("Token not available!")
    # raise


import csv
import datetime
import json
import os
import time
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from dotenv import dotenv_values
import telebot

# load_dotenv("C:/Users/avivg/Shtroodle moodle bot/.env")
# get username from the .env file
username = os.environ.get("USERNAME")
password = os.environ.get("PASSWORD")


class GetTask:
    @classmethod
    def get_moodle_tasks(cls) -> list:
        # url = "https://moodle2.cs.huji.ac.il/nu22/login/index.php?slevel=4"
        # url = "https://moodle2.cs.huji.ac.il/nu22/"
        url = "https://moodle2.cs.huji.ac.il/nu22/login/index.php"

        driver = cls.open_url_link(url)
        new_scan_result = cls.scrape_tasks(driver)
        driver.quit()
        return new_scan_result

    def open_url_link(url: str):
        # def open_url_link(url: str):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        # overcome limited resource problems
        options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="login"]/input'))
        ).click()
        # wait until the page loads
        time.sleep(3)
        driver.find_element(By.ID, "pills-email-tab").click()
        time.sleep(2)
        driver.find_element(By.ID, "username").send_keys(str(username))
        driver.find_element(By.ID, "password").send_keys(str(password))
        # press enter key
        # driver.find_element(By.ID, "password").send_keys(u"\ue007")
        wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="f3"]/div[3]/button'))
        ).click()
        time.sleep(5)
        driver.get("https://moodle2.cs.huji.ac.il/nu22/calendar/view.php?view=upcoming")
        return driver

    # GetTask.get_moodle_task()

    def scrape_tasks(driver):
        soup = BeautifulSoup(driver.page_source, "html.parser")  # Get the events
        # Get the events
        events = soup.find_all("div", class_="event")
        # Loop through all the events and extract the necessary information
        result = []
        for event in events:
            data = {}

            title_replacements = {
                "הגשה: ": "",
                "Submission": "",
                "הגשה ": "",
                "is due": "",
                ":": "",
                "יש להגיש את ": "",
            }
            data["title"] = event["data-event-title"]
            for old, new in title_replacements.items():
                data["title"] = data["title"].replace(old, new)

            # print(data["title"])

            data["date"] = event.find_all("div", class_="col-11")[0].text
            if event.find("div", class_="description-content") != None:
                data["description"] = event.find(
                    "div", class_="description-content"
                ).text
                course_index = 3
            else:
                data["description"] = ""
                course_index = 2

            try:
                # get the course name, if the course name is not Nan
                data["course"] = event.find_all("div", class_="col-11")[
                    course_index
                ].text
                # get link to the event submission page
                data["link"] = event.find_all("div", class_="col-11")[
                    course_index
                ].find("a")["href"]
                # print(data["course"])
            except:
                data["course"] = ""
                data["link"] = ""
            result.append(data)
            # print(data)

        # Save the information to a json file
        with open("tasks.json", "w") as f:
            json.dump(result, f)
        return result

    # create a function to compare new and old tasks
    def compare_tasks(new_tasks, old_tasks):
        new_tasks = [task["title"] for task in new_tasks]
        old_tasks = [task["title"] for task in old_tasks]
        # get index of new tasks
        return [task for task in new_tasks if task not in old_tasks]

    def get_new_dictionaries(current_list, new_list):
        # create a new list to store the new dictionaries
        result = []

        # iterate through the new_list
        for new_dict in new_list:
            # check if the dictionary is already present in the current_list
            if new_dict not in current_list:
                # add the new dictionary to the result list
                result.append(new_dict)

        return result

    def output_to_csv(output_dict):
        with open("tasks.json", "r") as f:
            task = json.load(f)
        with open("tasks.csv", "w", encoding="utf-8") as f:  # Specify utf-8 encoding
            writer = csv.DictWriter(f, fieldnames=task[0].keys())
            writer.writeheader()
            writer.writerows(task)


if __name__ == "__main__":
    # with open("task.json", "w") as f:
    try:
        with open("tasks.json", "r") as f:
            previous_tasks = json.load(f)
    except FileNotFoundError:
        previous_tasks = []
    logger.info(f"Token value: {USERNAME2}")

    r = requests.get(
        "https://weather.talkpython.fm/api/weather/?city=Berlin&country=DE"
    )
    if r.status_code == 200:
        data = r.json()
        temperature = data["forecast"]["temp"]
        logger.info(f"Weather in Berlin: {temperature}")

    res = GetTask.get_moodle_tasks()
    # print(res)

    new_posts = GetTask.get_new_dictionaries(previous_tasks, res)
    # print("done", check)

    # print(new_posts)
    # GetTask.output_to_csv(res)

    # TELEGRAM BOT
    BOT_TOKEN = os.environ["BOT_TOKEN"]
    bot = telebot.TeleBot(BOT_TOKEN)

    # send message to the user about the a latest update with the link to the submission page and the due date of the task
    if len(new_posts) != 0:
        for task in new_posts:
            # res[che]
            bot.send_message(
                536568724,
                f"Master Bruce, there is a new moodle for the Course: {task['course']}\n \n Assignment named: '{task['title']}' was just uploaded.\n \n The deadline set for {task['date']}. \nLink: {task['link']} \n \n Best of luck!",
            )
        logger.info("Finished running, new updates found and sent to user")
    else:
        logger.info("Finished running, no updates found")
        # bot.send_message(536568724, "No new moodle updates")

# @bot.message_handler(commands=['start', 'hello'])
# bot.reply_to(message, "Howdy, how are you doing?")

# @bot.message_handler(func=lambda msg: True)
# def echo_all(message):
# bot.reply_to(message, message.text)
