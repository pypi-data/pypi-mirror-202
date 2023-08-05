import time
import json
import asyncio
import re
import os
from selenium import webdriver
from selenium.webdriver import Edge, Chrome, Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from .edge import Chatbot, ConversationStyle

class BingSession:
    def __init__(self, email, password, browser='edge', headless=True):
        self.email = email
        self.password = password
        self.browser = browser
        self.headless = headless
        self.cookies_file = 'cookies.json'
        self.bot = None

    def login(self):
        # Select the appropriate browser driver
        if self.browser == 'edge':
            driver = Edge()
        elif self.browser == 'chrome':
            driver = Chrome()
        elif self.browser == 'firefox':
            driver = Firefox()
        else:
            raise ValueError(f"Invalid browser specified: {self.browser}")

        # Configure options
        edgeOptions = webdriver.EdgeOptions()
        edgeOptions.headless = self.headless
        options = Options()
        if self.headless:
            options.add_argument("--headless")
            options.add_argument('--disable-gpu')

        # Navigate to the login page and enter email
        driver.get('https://login.live.com/')
        email_input = driver.find_element(By.NAME, 'loginfmt')
        email_input.send_keys(self.email)
        driver.find_element(By.ID, 'idSIButton9').click()
        time.sleep(3)

        # Enter password and submit
        password_input = driver.find_element(By.NAME, 'passwd')
        password_input.send_keys(self.password)
        driver.find_element(By.ID, 'idSIButton9').click()
        time.sleep(3)

        # Navigate to chat page and click button
        driver.get('https://www.bing.com/')
        driver.get('https://www.bing.com/')
        time.sleep(3)
        driver.find_element(By.CLASS_NAME, 'id_button').click()
        time.sleep(3)

        # Save cookies to file and quit driver
        cookies = driver.get_cookies()
        with open(self.cookies_file, 'w') as f:
            json.dump(cookies, f)
        driver.quit()

    async def chat(self):
        if not os.path.isfile(self.cookies_file):
            self.login()

        self.bot = Chatbot(cookiePath=self.cookies_file)
        while True:
            message = input("You: ")
            if message == "bye":
                break
            response = await self.bot.ask(prompt=message, conversation_style=ConversationStyle.precise)
            res = response['item']['messages'][1]['text']
            pattern = r"\[\^[0-9]+\^\]"
            res = re.sub(pattern, "", res)
            res = res.strip()
            res = res.replace("  ", " ")
            res = res.replace("  ", " ")
            res = res.replace(" .", ".")
            res = res.replace("**", "")
            print("Bot:", res)
        await self.bot.close()

    def run(self):
        try:
            asyncio.run(self.chat())
        except Exception as e:
            print(e)
            self.login()
            asyncio.run(self.chat())
