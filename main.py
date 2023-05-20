# libraries
import csv
import json

import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import telebot
import logging
import logging.handlers
import os

import requests
import re

# from dotenv import load_dotenv
# load_dotenv()

username = os.environ.get("USER_NAME")
password = os.environ.get("PASSWORD")
# print(username, password)
bot_token = os.environ.get("BOTTOKEN")
chat_id = os.environ.get("CHAT_ID")
# print(bot_token, chat_id)
script_dir = os.path.dirname(os.path.abspath(__file__))
log_file_path = os.path.join(script_dir, "status.log")

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger_file_handler = logging.handlers.RotatingFileHandler(
    log_file_path,
    maxBytes=1024 * 1024,
    backupCount=1,
    encoding="utf8",
)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger_file_handler.setFormatter(formatter)
logger.addHandler(logger_file_handler)

logger.info("scrape_tasks activated")


class MoodleBot:
    # @classmethod

    # @classmethod

    # @classmethod

    # create a function to output the new tasks to a csv file
    def output_to_csv():
        with open("tasks.json", "r") as f:
            task = json.load(f)
        with open("tasks.csv", "w", encoding="utf-8") as f:  # Specify utf-8 encoding
            writer = csv.DictWriter(f, fieldnames=task[0].keys())
            writer.writeheader()
            writer.writerows(task)


if __name__ == "__main__":

    def get_moodle_tasks():
        # try:
        #     url = "https://moodle2.cs.huji.ac.il/nu22/login/index.php?slevel=4"
        #     driver = open_url_link_cs(url)
        #     print("Logged in to CS")
        # # url = "https://moodle2.cs.huji.ac.il/nu22/"
        # except:
        url_dom = "https://moodle2.cs.huji.ac.il/nu22"
        app_data = {"login": username, "password": password, "url": url_dom}
        session = open_url_link_cs(app_data)
        # print("Logged in to usual")
        old_tasks, new_tasks = scrape_tasks(session)
        time.sleep(5)
        # driver.quit()
        return old_tasks, new_tasks

    def open_url_link_cs(data: dict) -> requests.Session():
        # url = "https://moodle2.cs.huji.ac.il/nu22/login/index.php?slevel=4"

        login, password, url_domain = data.values()
        s = requests.Session()
        r_1 = s.get(url=url_domain + "/login/index.php")
        pattern_auth = '<input type="hidden" name="logintoken" value="\w{32}">'
        token = re.findall(pattern_auth, r_1.text)
        token = re.findall("\w{32}", token[0])[0]
        payload = {
            "anchor": "",
            "logintoken": token,
            "username": login,
            "password": password,
            "rememberusername": 1,
        }
        r_2 = s.post(url=url_domain + "/login/index.php", data=payload)
        for i in r_2.text.splitlines():
            if "<title>" in i:
                # print(i[15:-8:])
                break
        counter = 0
        for i in r_2.text.splitlines():
            if "loginerrors" in i or (0 < counter <= 3):
                counter += 1
                # print(i)
        # print(r_2.text)
        r_3 = s.get(
            url="https://moodle2.cs.huji.ac.il/nu22/calendar/view.php?view=upcoming"
        )
        return r_3

    def open_url_link_usual(url: str):
        logger.info("open_url_link activated")
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")

        # overcome limited resource problems
        options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=options
        )

        # driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="login"]/input'))
        ).click()

        time.sleep(2)
        driver.find_element(By.ID, "pills-email-tab").click()
        time.sleep(2)
        # the following code not working on github actions, there is a recaptcha that blocks it
        #

        driver.find_element(By.ID, "username").send_keys(str(username))
        driver.find_element(By.ID, "password").send_keys(str(password))
        wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="f3"]/div[3]/button'))
        ).click()
        time.sleep(5)
        driver.get("https://moodle2.cs.huji.ac.il/nu22/calendar/view.php?view=upcoming")
        logger.info("open_url_link finished")

        return driver

    def scrape_tasks(response: requests.Session()):
        url = "https://moodle2.cs.huji.ac.il/nu22/login/index.php?slevel=4"

    def get_previous_tasks():
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # print("\nscript_dir: \n", script_dir)
        try:
            logger.info("Searching for previous tasks")
            with open(os.path.join(script_dir, "tasks.json"), "r") as f:
                previous_tasks = json.load(f)
            logger.info("found previous tasks")
            # print("\n\nprevious tasks are not empty\n\n", previous_tasks)
        except FileNotFoundError:
            logger.info("did not find previous tasks")
            previous_tasks = []
        return previous_tasks

    # create a function to compare new and old tasks
    def compare_tasks(new_tasks, old_tasks):
        logger.info("compare_tasks activated")
        new_tasks = [task["title"] for task in new_tasks]
        old_tasks = [task["title"] for task in old_tasks]
        # print("OLD:", new_tasks, "\nNEW:", old_tasks)

        # get index of new tasks
        return [
            task for task in new_tasks if task not in old_tasks
        ]  # return the new tasks

    # create a function to get the new dictionaries
    def get_new_dictionaries(old_list, new_list):
        # create a new list to store the new dictionaries
        logger.info("get_new_dictionaries activated")
        new_dictionaries = []
        # iterate through the new_list
        for new_dict in new_list:
            # check if the dictionary is already present in the current_list
            if new_dict not in old_list:
                # add the new dictionary to the result list
                new_dictionaries.append(new_dict)
        return new_dictionaries

    # TELEGRAM BOT
    def send_telegram_if_new(new_posts, bot_token):  #
        bot = telebot.TeleBot(bot_token)

        # send message to the user about the a latest update with the link to the submission page and the due date of the task
        if len(new_posts) != 0:
            for task in new_posts:
                message_text = f"Master Bruce,\n Upcoming event:"
                if task["course"] != "":
                    message_text += (
                        f"\n \n{task['course']}.\n \n Name: \n'{task['title']}'"
                    )
                else:
                    message_text += f"\n \n Name: \n'{task['title']}'"
                if task["description"] != "":
                    message_text += f"\n \n Description: \ת{task['description']}; End of description"
                if task["link"] != "":
                    if task["date"] != "":
                        message_text += f"\n \n Deadline is {task['date']}."
                    message_text += f"\n \nLink: {task['link']}"
                else:
                    if task["date"] != "":
                        message_text += f"\n \n Deadline is {task['date']}."
                message_text += "\n Cheers👋"
                bot.send_message(
                    chat_id,
                    message_text,
                )
            logger.info("Finished running, new updates found and sent to user")
            print("\n\nNew moodle updates sent to user\n\n")
        else:
            logger.info("Finished running, no updates found")
            print("\n\n No new moodle updates")
            # bot.send_message(536568724, "No new moodle updates")

            # @bot.message_handler(commands=['start', 'hello'])
            # bot.reply_to(message, "Howdy, how are you doing?")

            # @bot.message_handler(func=lambda msg: True)
            # def echo_all(message):
            # bot.reply_to(message, message.text)

    # previous_tasks, new_tasks = get_moodle_tasks()

    # MoodleBot.output_to_csv()

import requests
import re
import os

url = "https://moodle2.cs.huji.ac.il/nu22/login/index.php?slevel=4"
username = os.environ.get("USER_NAME")
password = os.environ.get("PASSWORD")
bot_token = os.environ.get("BOTTOKEN")
chat_id = os.environ.get("CHAT_ID")
app_data = {
    "login": username,
    "password": password,
    "url": url,
}


def auth_moodle(data: dict) -> requests.Session():
    login, password, url_domain = data.values()
    s = requests.Session()
    r_1 = s.get(url=url_domain)
    time.sleep(4.2)

    # how to make it work: sleep(1)

    pattern_auth = '<input type="hidden" name="logintoken" value="\w{32}">'
    token = re.findall(pattern_auth, r_1.text)
    token = re.findall("\w{32}", token[0])[0]
    payload = {
        "anchor": "",
        "logintoken": token,
        "username": login,
        "password": password,
        "rememberusername": 1,
    }
    r_2 = s.post(url=url_domain + "/login/index.php", data=payload)
    time.sleep(4.5)
    for i in r_2.text.splitlines():
        if "<title>" in i:
            # print(i[15:-8:])
            break
    counter = 0
    for i in r_2.text.splitlines():
        if "loginerrors" in i or (0 < counter <= 3):
            counter += 1
            # print(i)
    # print(r_2.text)

    r_3 = s.get(
        url="https://moodle2.cs.huji.ac.il/nu22/calendar/view.php?view=upcoming"
    )
    time.sleep(4.5)

    soup = BeautifulSoup(r_3.content, "html.parser")
    # print(soup.prettify())
    return r_3


logged_in = auth_moodle(data=app_data)
soup = BeautifulSoup(logged_in.content, "html.parser")
# print(soup.prettify())

logger.info("open_url_link_cs activated")
# Get the events.
events = soup.find_all("div", class_="event")
# logger.info(f"events: { events }")
# print("events: ", events)

# Loop through all the events and extract the necessary information
new_tasks = []

for event in events:
    data = {}

    title_replacements = {
        "הגשה: ": "",
        "Submission": "",
        "הגשה ": "",
        "is due": "",
        ":": "",
        "יש להגיש את ": "",
        "של": "",
    }

    data["title"] = event["data-event-title"]

    if data["title"] == "מטלת בונוס דורש התייחסות":
        continue  # skip this event
    # contains "סימולציה" or "simulation" in the title
    if data["title"].find("סימולציה") != -1 or data["title"].find("3 חלקי א'") != -1:
        continue
    logger.info(f'title: {data["title"]}')
    # print(data["title"])
    for old, new in title_replacements.items():
        data["title"] = data["title"].replace(old, new)
    # print reveresed title
    # reverse every hebrew word in the title
    hebrew_letters = "אבגדהוזחטיכלמנסעפצקרשת"
    str_title = data["title"]
    # for word in data["title"].split(" "):
    #     if word[0] in hebrew_letters:
    #         str_title = data["title"].replace(word, word[::-1])
    #         # print(str_title)
    #     # else:
    # print(str_title)
    if data["title"][0] in hebrew_letters:
        str_title = data["title"][::-1]
    print(str_title)

    data["date"] = event.find_all("div", class_="col-11")[0].text

    if event.find("div", class_="description-content") != None:
        data["description"] = event.find("div", class_="description-content").text
        course_index = 3
    else:
        data["description"] = ""
        course_index = 2
    try:
        # get the course name, if the course name is not Nan
        data["course"] = event.find_all("div", class_="col-11")[course_index].text
        # print(data["course"])
    except:
        data["course"] = ""
    # print(data)
    try:
        # get link to the event submission page
        data["link"] = event.find("div", class_="card-footer").find(
            "a", class_="card-link"
        )["href"]
    except:
        data["link"] = ""
        # print("no link found")

    # append the data to the result list
    new_tasks.append(data)

previous_tasks = get_previous_tasks()

json_file_path = os.path.join(script_dir, "tasks.json")
with open(json_file_path, "w") as f:
    json.dump(new_tasks, f)

logger.info("scrape_tasks finished, JSON file created")
new_posts = get_new_dictionaries(previous_tasks, new_tasks)
print("new posts: ", len(new_posts))
send_telegram_if_new(new_posts, bot_token)
