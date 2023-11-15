from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

from datetime import datetime
import time

# ----------------

def configure_driver():
    # Add additional Options to the webdriver
    options = webdriver.ChromeOptions()
    # add the argument and make the browser Headless.
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.page_load_strategy = 'normal'
    #Handle the service
    #service = Service(executable_path=r'/usr/bin/chromedriver')
    # Instantiate the Webdriver: Mention the executable path of the webdriver you have downloaded
    # driver = webdriver.Chrome(options=options)
    driver = webdriver.Chrome()
    return driver

# ----------------

def getChat(driver):
    # https://www.pluralsight.com/search?q=web%20scraping&categories=course
    # Step 1: Go to pluralsight.com, category section with selected search keyword
    # driver.get(f"https://www.pluralsight.com/search?q=*&categories=course%2Ccloud-courses&sort=displayDate")
    # driver.get(f"https://www.twitch.tv/hasanabi")
    driver.get(f"https://www.twitch.tv/kingsleague")
    # wait for the element to load
    wait = WebDriverWait(driver, 10)

    try:
      # WebDriverWait(driver, 20).until(lambda s: s.find_element("chat-scrollable-area__message-container").is_displayed())
      WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME,"chat-scrollable-area__message-container")))
      driver.find_element(By.CLASS_NAME,"chat-line__message").scrollIntoView()
    except TimeoutException:
      print("Timeout :(")
      return None
    i=0

    chat_container = (By.CLASS_NAME, 'chat-scrollable-area__message-container')
    
    print("moving on...")

    # Step 2: Create a parse tree of page sources after searching
    soup = BeautifulSoup(driver.page_source, "lxml")
    # Step 3: Iterar sobre los elementos del contenedor de chat. Capturar un id o array del ultimo elemento capturado

    data = []
    msg_elements = []
    print("after 20 sec...")
    contt = soup.select("div.chat-scrollable-area__message-container")
    
    element = driver.find_element(By.CLASS_NAME, "chat-scrollable-area__message-container")
    all_messages = element.find_elements(By.CLASS_NAME, "chat-line__message")

    for chat_msg in soup.select("div.chat-scrollable-area__message-container div.chat-line__message"):
      username_selector = "div.chat-line__message-container div.chat-line__username-container span.chat-author__display-name"
      body_selector = "div.chat-line__message-container div.chat-line__no-background span.text-fragment"
      live_date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
      message_selector = "div.chat-line__message-container div.chat-line__no-background span[data-a-target='chat-line-message-body']"
      print(chat_msg)
      for message_value in chat_msg.select('div.chat-line__message-container div.chat-line__no-background span[data-a-target="chat-line-message-body"]'):
        print(message_value)

      data.append({"user" : chat_msg.select_one(username_selector).text,
          "body" : chat_msg.select_one(body_selector).text,
          "live_date" : live_date,
          "message_selector" : chat_msg.select_one(message_selector).text})
    return data

# ----------------

# create the driver object.
driver = configure_driver()
driver.implicitly_wait(20)
data = getChat(driver)

data
print("--------")
print(data)
driver.close()

# ----------------

# import csv
# field_names= ['user', 'body', 'live_date', 'message_selector' ]

# with open('dataset_cursos.csv', 'w') as csvfile:
#     writer = csv.DictWriter(csvfile, fieldnames=field_names)
#     writer.writeheader()
#     writer.writerows(data)