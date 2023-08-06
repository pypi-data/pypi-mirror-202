import time
import json
import asyncio
import re
import os
from selenium import webdriver
from selenium.webdriver import Edge, Chrome, Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from .ConstantsDX import *
from .Constants import *
from .Edge import Chatbot, ConversationStyle


class DolbyChat:
    def __init__(self, email, password, browser='edge', headless=True):
        self.email = email
        self.password = password
        self.browser = browser
        self.headless = headless
        self.cookies_file = 'cookies.json'
        self.bot = None
        if not os.path.isfile(self.cookies_file):
            self.__login__()
        self.bot = Chatbot(cookiePath=self.cookies_file)

    def __login__(self):
        if self.browser == 'edge':
            driver = Edge()
        elif self.browser == 'chrome':
            driver = Chrome()
        elif self.browser == 'firefox':
            driver = Firefox()
        else:
            raise ValueError(f"Invalid browser specified: {self.browser}")

        edgeOptions = webdriver.EdgeOptions()
        edgeOptions.headless = self.headless
        options = Options()
        if self.headless:
            options.add_argument("--headless")
            options.add_argument('--disable-gpu')

        driver.get('https://login.live.com/')
        email_input = driver.find_element(By.NAME, 'loginfmt')
        email_input.send_keys(self.email)
        driver.find_element(By.ID, 'idSIButton9').click()
        time.sleep(3)

        password_input = driver.find_element(By.NAME, 'passwd')
        password_input.send_keys(self.password)
        driver.find_element(By.ID, 'idSIButton9').click()
        time.sleep(3)

        driver.get('https://www.bing.com/')
        driver.get('https://www.bing.com/')
        time.sleep(3)
        driver.find_element(By.CLASS_NAME, 'id_button').click()
        time.sleep(3)

        cookies = driver.get_cookies()
        with open(self.cookies_file, 'w') as f:
            json.dump(cookies, f)
        driver.quit()

    async def __call__(self, query: str):
        # type: ignore
        response = await self.bot.ask(prompt=query, conversation_style=ConversationStyle.precise)
        res = re.sub(r"\[\^[0-9]+\^\]", "", response['item']['messages'][1]['text']).strip().replace("  ", " ").replace("  ", " ").replace(" .", ".").replace("**", "")
        res = re.sub(r'[^\x00-\x7F]+', '', res)
        return res

    async def __talk__(self, speak=False):
        while True:
            query = input("You: ")
            print()
            if query == "bye":
                print("Bot: Bye, have a nice day!")
                if speak:
                    os.system('say "Bye, have a nice day!"')
                break
            res = await self.__call__(query)
            print("Bot:", res)
            print()
            if speak:
                os.system(f'say "{res}"')
        await self.bot.close()  # type: ignore

    async def __ask__(self, query: str, speak=False):
        res = await self.__call__(query)
        if speak:
            os.system(f'say "{res}"')
        return res

    def ask(self, query: str, speak=False):
        try:
            return asyncio.run(self.__ask__(query, speak))
        except Exception as e:
            self.__login__()
            return asyncio.run(self.__ask__(query, speak))

    def talk(self, speak=False):
        print("[Tip: Say bye to exit.]")
        print()
        print("Bot: Hello, this is DolbyChat. How can I help you?")
        if speak:
            os.system('say "Hello, this is DolbyChat. How can I help you?"')
        print()
        try:
            asyncio.run(self.__talk__(speak))
        except Exception as e:
            self.__login__()
            asyncio.run(self.__talk__(speak))
