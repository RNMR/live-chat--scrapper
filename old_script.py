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
import sys
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

def getChat(driver):
  
  # driver.get(f"https://www.twitch.tv/xcry")
  driver.get(f"https://www.twitch.tv/maximum")
  # wait for the element to load
  wait = WebDriverWait(driver, 10)

  chat_container = (By.CLASS_NAME, 'chat-scrollable-area__message-container')
  chat_message = (By.CLASS_NAME, 'chat-line__message')
  elementButon = wait.until(EC.visibility_of_element_located(chat_message))
  # all_chats = driver.find_elements(chat_message)
  
  data = []
  msg_elements = []
  
  # element = driver.find_element(By.CLASS_NAME, "chat-scrollable-area__message-container")
  # all_messages = element.find_elements(By.CLASS_NAME, "chat-line__message")

  dataCounter = 0
  msgLimit = 149
  while len(data) <= msgLimit:
  # while dataCounter <= 150:
    try:
      sys.stdout.write("\r%d%%" % (dataCounter/msgLimit*100))
      soup = BeautifulSoup(driver.page_source, "html.parser") #Repetir esto para refreshear mensajes
      # for chat_msg in driver.find_element("div.chat-scrollable-area__message-container div.chat-line__message"):
      # Aca empieza a tomar los mensajes de chat desde donde se quedo en la última leida
      for chat_msg in soup.select("div.chat-scrollable-area__message-container div.chat-line__message")[dataCounter:]:
        if(len(chat_msg) != 0):
          username_selector = "div.chat-line__message-container div.chat-line__username-container span.chat-author__display-name"
          # body_selector = "div.chat-line__message-container div.chat-line__no-background span.text-fragment"
          # raw = 'div.chat-line__message-container div.chat-line__no-background span[data-a-target="chat-line-message-body"]'
          raw = []
          classes = []
          textRow = []
          live_date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
          message_selector = "div.chat-line__message-container div.chat-line__no-background span[data-a-target='chat-line-message-body']"
          for message_value in chat_msg.select('div.chat-line__message-container div.chat-line__no-background span[data-a-target="chat-line-message-body"]'):
            classes.append(message_value['class'])
            textRow.append(message_value.get_text())
            raw.append(message_value)
            # print(message_value)
            # print(f"{dataCounter}")
            # print("--------")

          dataCounter = dataCounter + 1
          data.append({
            "user" : chat_msg.select_one(username_selector).text,
            # "body" : chat_msg.select_one(body_selector).text,
            # "raw" : chat_msg.select_one(raw),
            "live_date" : live_date,
            "message_selector" : chat_msg.select_one(message_selector).text,
            "classes" : classes,
            "rawText" : " ".join(textRow),
            # "rawText" : textRow,
            "raw" : raw
          })
          # print("row done")
        else:
          print("REFRESHING....")
      # out of the for loop
      # time.sleep(3)
    except Exception as e:
      print("ERROR:")
      print(f"Error es: {e}")
      exit()

  print("-----LOOP ENDED, CLOSING...---")

  return data

startTime = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
# create the driver object.
driver = configure_driver()
driver.implicitly_wait(20)
data = getChat(driver)



driver.close()


import csv
field_names= [
  'user',
  # 'body',
  'live_date',
  'message_selector',
  'classes',
  'rawText',
  'raw'
]
print("doing CSV")
with open('live_chat.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=field_names)
    endTime = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    header = "FROM: " + startTime + " - " + endTime
    writer.writeheader()
    # writer.writerow(header)
    print(header)
    writer.writerows(data)