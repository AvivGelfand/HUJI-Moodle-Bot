<img align="right" alt="Alfred" src="https://assets.mycast.io/characters/alfred-pennyworth-627238-normal.jpg?1587997434"  height="180" />

# Alfred - a Personal Moodle Bot 

**Alfred is a Python-based bot Scraping & Messaging bot** that scrapes [Hebrew University of Jerusalem's Moodle](https://moodle2.cs.huji.ac.il/nu22/) and sends a message through Telegram about any new update or upload in upcoming deadlines for assignment.  

## Project Files

- `.github/workflows/new_pass` - A workflow file for GitHub Actions
- `.gitignore` - A file specifying intentionally untracked files that Git should ignore
- `README.md` - This file!
- `main.py` - The main Python script for the bot
- `requirements.txt` - A list of Python dependencies for the project
- `status.log` - A log file for the status of the bot
- `tasks.json` - A JSON file containing a list of the scraped tasks
- `testenv.py` - A Python script for testing the environment

## Installation

1. Clone the repository to your local machine
2. Install the required packages using the following command:

```
pip install -r requirements.txt
```

### Requirements

The following libraries are required to run the script:

- **`beautifulsoup4==4.9.3`**
- **`dotenv==0.18.0`**
- **`requests==2.25.1`**
- **`selenium==3.141.0`**
- **`webdriver_manager==3.3.0`**
  These can be installed using the **`pip install -r requirements.txt`** command.

## Configuration

Before running the script, create a `.env` file in the root directory of the project and add the following variables:

```
USERNAME==<Your Moodle username>
PASSWORD==<Your Moodle password>
BOTTOKEN==<Your Telegram bot token>
CHATID==Your Telegram chat ID>
```

## Running the script

To run the script, simply run **`python main.py`**.

## Files

- **`.github/workflows`** A folder containing this project's GitHub Actions configuration file.
- **`main.py`**: The Python script logs into Moodle and scrapes the tasks.
- **`requirements.txt`**: A file containing the required Python libraries.
- **`status.log`**: A log file containing the script's status.
- **`tasks.json`**: A JSON file containing the scraped tasks.
- **`README.md`**: This file contains information about the project.

## Running the bot automatically in time intervals:

- Inspect and configure the cron job in GitHub Action `.github/workflows/actions.yml`
- It can install and use third-party packages from `requirements.txt`
- Secret environment variables can be used. Set secrets in Settings/Secrets/Actions -> 'New repository secret'. Use the same secret name inside `actions.yml` and `main.py`

## Credits

This project's structure is a [for of the python-github-action-template repository](https://github.com/patrickloeber/python-github-action-template). Special thanks to [patrickloeber](https://github.com/patrickloeber) for his hard work and for making his code available under an open-source license. While working on this project, I learned a lot from his [youtube channel](https://www.youtube.com/@patloeber).
