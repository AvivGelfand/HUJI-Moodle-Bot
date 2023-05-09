# Alfred - a Scraping Telegram Bot

**This is a python code:**

- Implement your script in `main.py`
- Inspect and configure cron job in GitHub Action `.github/workflows/actions.yml`
- It can install and use third party packages from `requirements.txt`
- Secret environment variables can be used. Set secrets in Settings/Secrets/Actions -> 'New repository secret'. Use the same secret name inside `actions.yml` and `main.py`

This project contains a Python script that allows a user to scrape tasks from the Moodle site. The bot logs into a Moodle account, navigates to the calendar page, and scrapes all of the upcoming tasks listed on the page. The tasks are saved to a JSON file, and the bot can compare the newly scraped tasks with the old tasks.

Requirements
The following libraries are required to run the script:

beautifulsoup4==4.9.3
dotenv==0.18.0
requests==2.25.1
selenium==3.141.0
webdriver_manager==3.3.0
These can be installed using the pip install -r requirements.txt command.

Configuration
Before running the script, you need to set the following environment variables:

USERNAME: Your Moodle username.
PASSWORD: Your Moodle password.
Running the script
To run the script, simply run python main.py.

Files
.github/workflows: A folder containing the GitHub Actions configuration file for this project.
main.py: The Python script that logs into Moodle and scrapes the tasks.
requirements.txt: A file containing the required Python libraries.
status.log: A log file containing the script's status.
tasks.json: A JSON file containing the scraped tasks.
README.md: This file, containing information about the project.
