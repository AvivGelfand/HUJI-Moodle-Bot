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


if __name__ == "__main__":
    logger.info(f"Token value: {USERNAME2}")

    r = requests.get(
        "https://weather.talkpython.fm/api/weather/?city=Berlin&country=DE"
    )
    if r.status_code == 200:
        data = r.json()
        temperature = data["forecast"]["temp"]
        logger.info(f"Weather in Berlin: {temperature}")


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

from dotenv import dotenv_values

# config = dotenv_values(".env")
# from methods import get_date_format, get_task_from_date
# load_dotenv("C:/Users/avivg/Shtroodle moodle bot/.env")
# get username from the .env file
# username = os.getenv("USERNAME")

# username = "aviv.gelfand@mail.huji.ac.il"
try:
    SOME_SECRET = os.environ["PASSWORD"]
except KeyError:
    SOME_SECRET = "Token not available!"
password = os.environ.get("PASSWORD")
username = os.environ.get("USERNAME2")
# print('env_path  \n',os.getenv("PATH"),'\n\n','done')
# print(username, password)
# username = USERNAME = "aviv.gelfand@mail.huji.ac.il"
# password = PASSWORD = "qmGn!2u9cftnLiN"
# print(username, password)


class GetTask:
    @classmethod
    def get_moodle_tasks(cls) -> list:
        # load_dotenv()
        url = "https://moodle2.cs.huji.ac.il/nu22/login/index.php?slevel=4"
        driver = cls.open_url_link(url)
        new_scan_result = cls.scrape_tasks(driver)
        driver.quit()
        return new_scan_result

    def open_url_link(url: str):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        # overcome limited resource problems
        options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get(url)
        driver.find_element(By.ID, "login_username").send_keys(str(username))
        driver.find_element(By.ID, "login_password").send_keys(str(password))
        driver.find_element(By.ID, "loginbtn").click()
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
        # index=
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
        # @classmethod
        # def task_update(cls):
        #     GetTask.get_moodle_tasks()
        #     today = get_date_format("today")
        #     todays_tasks = get_task_from_date(today)
        #     near_tasks = []
        #     if len(todays_tasks) != 0:
        #         now = datetime.datetime.now()
        #         for todays_task in todays_tasks:
        #             time_limit = datetime.datetime(
        #                 year=now.year,
        #                 month=now.month,
        #                 day=now.day,
        #                 hour=int(todays_task["time"].split(":")[0]),
        #                 minute=int(todays_task["time"].split(":")[1]),
        #             )
        #             if (time_limit - now).seconds < 7200:
        #                 near_tasks.append(todays_task)
        #     with open("./near_tasks.json", "w") as f:
        #         json.dump(near_tasks, f, ensure_ascii=False)


if __name__ == "__main__":
    # with open("task.json", "w") as f:
    try:
        with open("tasks.json", "r") as f:
            previous_tasks = json.load(f)
    except FileNotFoundError:
        previous_tasks = []

    # If the file doesn't exist, assume there is no previous data
    res = GetTask.get_moodle_tasks()
    # check = GetTask.compare_tasks(res, previous_tasks)
    new_posts = GetTask.get_new_dictionaries(previous_tasks, res)
    # print("done", check)
# GetTask.output_to_csv(res)

# turn all the tasks into a dataframe
# import pandas as pd
# df = pd.DataFrame(res)
# df

import telebot

BOT_TOKEN = BOT_TOKEN = "5415991109:AAF6Vk7BVF5IDcRRzaC-C1Q6-lp0aeEMcDk"

bot = telebot.TeleBot(BOT_TOKEN)

# print a message to the user about the a latest update with the link to the submission page and the due date of the task
if len(new_posts) != 0:
    for task in new_posts:
        # res[che]
        bot.send_message(
            536568724,
            f"New moodle update: \n\n Course: {task['course']}\n Assignment name: '{task['title']}'. \n Was just uploaded with a deadline set for {task['date']}. \nLink: {task['link']} \n Good luck!",
        )
# else:
# bot.send_message(536568724, "No new moodle updates")
# message_text = f"New moodle update {check}"


# bot.send_message(536568724, "New moodle update: " + message_text)
# @bot.message_handler(commands=['start', 'hello'])
# def send_welcome(message):
# bot.reply_to(message, "Howdy, how are you doing?")

# @bot.message_handler(func=lambda msg: True)
# def echo_all(message):
# bot.reply_to(message, message.text)

# bot.infinity_polling()
