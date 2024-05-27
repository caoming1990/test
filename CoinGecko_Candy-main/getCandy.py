import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from tqdm import tqdm
import time
import platform

# List of tokens
TOKENS = [
    "7b8f42a6e8686d6024c80449c9f6cb1c",  # qiao643919914@126.com(Edge 448187805@qq.com)
    "54d925b31a6062c43c60ff8b8fd9ef1a",  # qingshi256214735@126.com(Edge 11)
    "83a5b199ee94efd3a9e358767e0b6781",  # ding317731392151@126.com(Edge 12)
    "e12c6b706246e83863982a184911ba92",  # xiuzongh27362584@126.com(Edge 13)
    "419d2aa131d48acfae23cf3454293f91",  # yiduan9770392@126.com(Edge 14)
    "d910ad1cb108320b0b2931a65a33447a",  # yun103917069247@126.com(Edge 1)
    "c47e97ecfb523cdd912c65aa73a80395",  # lu087984314098@126.com(Edge 2)
    "458aa1660ce2ac84ea5d15a02b7178c8",  # buzhisuo540169@126.com(Edge 3)
    "32779e961908246e00ef9d0c8bbcb906",  # fengfuxi8210051@126.com(Edge 4)
    "d52100f61c2a1bb879803d1d7ecf9ceb",  # jinwulan739171@126.com(Edge 5)
    "a9fdcdc81da796d10af0391af8da3130",  # yi540528462847@126.com(Edge 6)
    "e645a9bd290d2c3e306e61e331e0a816",  # xidongqi47695847@126.com(Edge 7)
    "aaeeb8c645de6ac4226d38dca0b359de",  # jingyuqi53924@126.com(Edge 8)
    "cb6c8f49814a68e17f508987fe198c8f",  # wozhilei958695@126.com(Edge 9)
    "c95192277889a8893803693d53b5f859",  # diaogong42173911@126.com(Edge 10)
    "667394d94cf3e9a02d2b561516cee825",  # mi15199145140924@126.com(Edge 15)
    "89e8686ff5438441131711db2e41ded8",  # quliangq055847@126.com(Edge 16)
    # "",
    # "",
    # "",
    # "",
    # "",
]


def get_news_details(auth_token):
    options = webdriver.ChromeOptions()

    if platform.system() == 'Darwin':
        options.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
    elif platform.system() == 'Windows':
        options.binary_location = r'C:\Program Files\Google\Chrome\Application\chrome.exe'

    driver = webdriver.Chrome(options=options)
    driver.get("https://www.coingecko.com/zh/candy")

    if not auth_token or auth_token == "YOUR_GOOGLE_AUTH_TOKEN_HERE":
        raise ValueError("Access token is missing. Please configure it properly.")

    # Set the session_id cookie
    driver.add_cookie({"name": "_session_id", "value": auth_token})

    # Wait for the page to load
    WebDriverWait(driver, 10).until(lambda d: d.execute_script('return document.readyState') == 'complete')
    driver.refresh()

    # Wait for the page to load
    driver.implicitly_wait(10)

    # Get the page source
    html = driver.page_source

    # Use BeautifulSoup to parse the HTML
    soup = BeautifulSoup(html, 'html.parser')

    # Find the button
    button = driver.find_element(By.ID, "collectButton")
    button_text = soup.find('button', {'id': 'collectButton'}).text.strip()
    balance_div = soup.find('div', {'data-candy-target': 'balance'}).text

    return balance_div, button, button_text


# Iterate over the tokens and perform sign-in
for i, token in tqdm(enumerate(TOKENS), total=len(TOKENS), desc="Signing in"):
    balance_div, button, button_text = get_news_details(token)
    if button_text == '收集糖果':
        button.click()
        print(token + '签到成功')
    else:
        print('\n' + token + '已签到，糖果为：' + balance_div)

    random_interval = random.randint(12, 24) * 3600
