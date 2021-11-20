# I M P O R T A N T
# pip install bs4 lxml pyautogui
# correct event_link
# correct standing_link

import pyautogui
import time, datetime
import os
from bs4 import BeautifulSoup
from urllib.request import urlopen as uReq
from urllib.error import HTTPError, URLError
import socket
import random
import platform

standing_link = 'http://oj.synapse0.com/standings.php?contest=1001'
event_link = 'https://www.facebook.com/events/411079077292218/?active_tab=discussion'
robot_greeting = ['Beep bop I\'m a Robot', 'Robot says', 'Ranklist alert']
sleep_after_post_success = 900 # 15 minutes
sleep_after_post_fail = 60 # 1 minutes
sleep_start_time = 300 # 5 minutes
contest_start_time = datetime.datetime.now(datetime.timezone.utc).replace(day=20, month=11, year=2021, hour=4, minute=0, second=0, microsecond=0)

def GetGoogleChrome():
    system_ = platform.system()
    if system_ == 'Windows':
        return "C:\\Users\\User\\AppData\\Local\\Google\\Chrome\\Application\\chrome.exe"
    elif system_ == 'Darwin':
        return 'open -a /Applications/Google\ Chrome.app'
    elif system_ == 'Linux':
        return '/usr/bin/google-chrome'

chrome_path = GetGoogleChrome()

def FetchStandingHtmlPage():
    print(f'sending request [{standing_link}]...')
    isError, html = False, None
    try:
        client = uReq(standing_link, timeout=20)
        html = client.read()
        client.close()
    except HTTPError as error:
        print('[ERROR] data not retrieved because %s\nURL: <%s>', error)
        isError = True
    except URLError as error:
        if isinstance(error.reason, socket.timeout):
            print('[ERROR] socket timed out - URL')
        else:
            print('[ERROR] some other error happened')
        isError = True
    except socket.timeout:
        print('[ERROR] socket timed out - URL')
        isError = True
    except ValueError:
        print('[ERROR] invalid URL')
        isError = True
    else:
        print(f'[SUCCESS] successfully received response!')

    return isError, html

def GetStanding():
    isError, htmlResponse = FetchStandingHtmlPage()

    if isError:
        raise Exception('Skipping process due to error...')

    soup = BeautifulSoup(htmlResponse, features="lxml")

    spans = soup.find_all('span', class_='standings-list-item')
    # span <- th <- tr <- thead -> tbody -> trs
    trs = spans[0]\
        .find_parent()\
        .find_parent()\
        .find_parent()\
        .find_next_sibling('tbody')\
        .find_all('tr')
        # .find_parent()\
    tds = trs[0].find_all('td')
    
    rank = tds[0].string.strip()
    name = tds[1].string.strip()
    problems_solved = tds[2].string.strip()
    print(rank, name, problems_solved)
    return rank, name, problems_solved

def PressEnter():
    pyautogui.keyDown('enter')
    pyautogui.keyUp('enter')

def PressShiftEnter():
    pyautogui.keyDown('shift')
    PressEnter()
    pyautogui.keyUp('shift')

def PressCtrlT():
    pyautogui.keyDown('ctrl')
    pyautogui.keyDown('t')
    pyautogui.keyUp('t')
    pyautogui.keyUp('ctrl')

def PressCtrlEnter():
    pyautogui.keyDown('ctrl')
    PressEnter()
    pyautogui.keyUp('ctrl')

def GetCommandKeyByOS():
    system_ = platform.system()
    if system_ == 'Windows' or system_ == 'Linux':
        return 'ctrl'
    elif system_ == 'Darwin':
        return 'command'

def PressCommandF():
    pyautogui.keyDown(GetCommandKeyByOS())
    pyautogui.keyDown('f')
    pyautogui.keyUp('f')
    pyautogui.keyUp(GetCommandKeyByOS())

def PressCommandW():
    pyautogui.keyDown(GetCommandKeyByOS())
    pyautogui.keyDown('w')
    pyautogui.keyUp('w')
    pyautogui.keyUp(GetCommandKeyByOS())

def PressCommandT():
    pyautogui.keyDown(GetCommandKeyByOS())
    pyautogui.keyDown('t')
    pyautogui.keyUp('t')
    pyautogui.keyUp(GetCommandKeyByOS())

def WriteFBEventPost(rank, name, problems_solved, post_number):
    # open chrome
    os.system(chrome_path)
    time.sleep(5)

    # open new tab
    PressCommandT()
    time.sleep(5)

    # type facebook event link
    pyautogui.typewrite(event_link)
    PressEnter()
    time.sleep(10)

    # find post button
    PressCommandF()
    time.sleep(2)
    pyautogui.typewrite('Add a Post')
    PressCtrlEnter()
    time.sleep(2)

    # write post
    greeting_text = robot_greeting[ random.randint(0, len(robot_greeting)-1) ]
    pyautogui.typewrite(f'{greeting_text} post {post_number}:')
    PressShiftEnter()
    pyautogui.typewrite(f'Rank: {rank}, Name: {name}, Problems solved: {problems_solved}')
    PressCtrlEnter()
    time.sleep(5)
    # close window
    PressCommandW()

def FetchRankAndPost(post_number):
    # check contest start time
    if datetime.datetime.now(datetime.timezone.utc) < contest_start_time:
        print(f'Contest has not started yet... start time: {contest_start_time}')
        time.sleep(sleep_start_time)
        FetchRankAndPost(post_number+1)
        return

    try:
        rank, name, problems_solved = GetStanding()
        print('Posting in Facebook...')
        WriteFBEventPost(rank, name, problems_solved, post_number)
        print(f'Successfully posted post no. {post_number} in Facebook!')
        time.sleep(sleep_after_post_success)
    except Exception as e:
        print(f'[ERROR] getting standings: {e}')
        time.sleep(sleep_after_post_fail)

    print('----------------------')
    FetchRankAndPost(post_number+1)

FetchRankAndPost(1)