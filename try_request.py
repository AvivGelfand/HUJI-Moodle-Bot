import requests
import re
import os

username = os.environ.get("USER_NAME")
password = os.environ.get("PASSWORD")
bot_token = os.environ.get("BOTTOKEN")
chat_id = os.environ.get("CHAT_ID")
url = "https://moodle2.cs.huji.ac.il/nu22/login/index.php?slevel=4"

passwd = password
login = username

r = requests.get("https://moodle2.cs.huji.ac.il/nu22/login/index.php?slevel=4")
cookie = r.cookies.get_dict()
pattern = '<input type="hidden" name="logintoken" value="\w{32}">'
token = re.findall(pattern, r.text)
token = re.findall("\w{32}", token[0])
payload = {"username": login, "password": passwd, "anchor": "", "logintoken": token[0]}
r = requests.post(
    "https://moodle2.cs.huji.ac.il/nu22/login/index.php?slevel=4",
    cookies=cookie,
    data=payload,
)
print(r)


import requests
import re
import os

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
            print(i[15:-8:])
            break
    counter = 0
    for i in r_2.text.splitlines():
        if "loginerrors" in i or (0 < counter <= 3):
            counter += 1
            print(i)
    print(r_2.text)
    return s


print(auth_moodle(data=app_data))

print("try something else")
from requests import session

baseurl = "https://moodle2.cs.huji.ac.il/nu22/"


def login(user, pwd):
    authdata = {"action": "login", "username": user, "password": pwd}
    with session() as ses:
        r = ses.post(baseurl + "login/index.php", data=authdata)
        # check if login was successful
        if r.url == baseurl + "my/":
            print("login successful")
        return ses


print(login(username, password))
