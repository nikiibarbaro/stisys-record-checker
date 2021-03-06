import os
import pathlib
import re
import sys
import time
import argparse
import requests
import smtplib
from email.mime.text import MIMEText
from bs4 import BeautifulSoup
from datetime import datetime

if not len(sys.argv) > 1:
    print("To login use -u 'username' -p 'password'")
    exit(0)

parser = argparse.ArgumentParser(description='Program for checking if new records are listed in StISys')
parser.add_argument('-u',
                    help='username for StISys')
parser.add_argument('-p',
                    help='password for the login')
parser.add_argument('-e',
                    help='your HAW Hamburg email adress')
parser.add_argument('-t',
                    help='interval in seconds for checking StISys', default=600)

args = parser.parse_args()
username = args.u
password = args.p
email = args.e
interval = int(args.t)

COURSES_COUNT = 0
cookie = None

cwd = os.getcwd()
path = os.path.join(cwd, "data")
path_file = os.path.join(path, "count.dat")
pathlib.Path(path).mkdir(parents=True, exist_ok=True)

if (os.path.isfile(path_file)):
    with open(path_file, 'r') as f:
        output = f.read()
        COURSES_COUNT = int(output)



def examination_check(cookie_stisys):
    headers_examination = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'de,en-US;q=0.7,en;q=0.3',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Referer': 'https://stisys.haw-hamburg.de/login.do',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
    }
    global COURSES_COUNT
    global cookie
    cookie = cookie_stisys
    #testing------------
    #soup_examination = BeautifulSoup(open("test.html"), 'lxml')
    #-------------------
    examination_get = requests.get('https://stisys.haw-hamburg.de/viewExaminationData.do', cookies=cookie,headers=headers_examination)
    soup_examination = BeautifulSoup(examination_get.text, 'lxml')

    if not (is_logged_in(soup_examination)):
        print("Login...")
        cookie = login()
        examination_get = requests.get('https://stisys.haw-hamburg.de/viewExaminationData.do', cookies=cookie, headers=headers_examination)
        soup_examination = BeautifulSoup(examination_get.text, 'lxml')

    tables = soup_examination.find_all('tr', {"class": ["tablecontentbackdark", "tablecontentbacklight"]})
    courses = []
    for table in tables:
        courses.append(table.find_all_next('td')[1].text)
    len1 = len(courses)
    if (len(courses) > COURSES_COUNT):
        if (len(courses) - COURSES_COUNT) == 1:
            print("[{0}] {1} new record detected".format(get_time(), len(courses) - COURSES_COUNT))
            if email is not None:
                send_email(1)
        else:
            print("[{0}] {1} new records detected".format(get_time(), len(courses) - COURSES_COUNT))
            if email is not None:
                send_email(len(courses) - COURSES_COUNT)
    else:
        print("[{0}] No new records detected".format(get_time()))
    COURSES_COUNT = len(courses)
    with open(path_file, 'w') as f:
        f.write(str(COURSES_COUNT))

def get_time():
    time_now = datetime.now()
    time_now = time_now.strftime("%H:%M:%S")
    return time_now

def login():
    headers_login = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'de,en-US;q=0.7,en;q=0.3',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://stisys.haw-hamburg.de/',
        'Origin': 'https://stisys.haw-hamburg.de',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
    }

    data = {
        'username': username,
        'password': password,
    }
    # prepare login
    login_post = requests.post('https://stisys.haw-hamburg.de/login.do', headers=headers_login, data=data)
    if login_post.status_code != 200:
        print("Something went wrong, try again")
        exit
    soup_login = BeautifulSoup(login_post.text, 'lxml')
    # check if login was successful
    login_state = soup_login.find_all('li')
    found = False
    for item in login_state:
        found = re.search('.*fehlgeschlagen.*', item.text)
    if (found):
        print("=== Login failed - Username or password did not match ===")
        exit(0)
    else:
        print("=== Login successful - You're logged in as {0} ===".format(username))
    return login_post.cookies

def is_logged_in(response):
    state = response.find_all('li')
    found = False
    for item in state:
        found = re.search('.*Session Timeout!.*', item.text)
    if (found):
        print("Could not fetch data from StISys because the session is expired")
        return False
    return True

def send_email(count):
    msg = MIMEText("")
    toaddr = email
    msg['From'] = email
    msg['To'] = email
    msg['Subject'] = "{0} new records arrived in Stisys".format(count)

    server = smtplib.SMTP("haw-mailer.haw-hamburg.de:587")
    server.starttls()
    server.login(email, password)
    text = msg.as_string()
    server.sendmail(email, toaddr, text)
    server.quit
if __name__ == '__main__':
    cookie = login()
    while True:
        examination_check(cookie)
        time.sleep(interval)
