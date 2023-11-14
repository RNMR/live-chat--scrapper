import json
import os
import time

import requests
from webdriver_manager.chrome import ChromeDriverManager

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

TOKEN_FILE_PATH=os.path.dirname(__file__)+"/metabypass.token"

#from seleniumwire.undetected_chromedriver.v2 import Chrome, ChromeOptions


#------------- IMAGE CAPTCHA ----------------

# Your Credentials
CLIENT_ID='961' #****CHANGE HERE WITH YOUR VALUE*******
CLIENT_SECRET='5LOFpsJ28lbPbGJhYTUOwxxNyOHNAcs3jA3YlNmg' #****CHANGE HERE WITH YOUR VALUE*******
EMAIL='iepvjortiz@gmail.com' #****CHANGE HERE WITH YOUR VALUE*******
PASSWORD='170273#@=!081889831491216' #****CHANGE HERE WITH YOUR VALUE*******

# -----------------------GET ACCESS TOKEN------------------------
def getNewAccessToken():
    request_url = "https://app.metabypass.tech/CaptchaSolver/oauth/token"
    payload=json.dumps({
        "grant_type":"password" ,
        "client_id":CLIENT_ID,
        "client_secret":CLIENT_SECRET,
        "username":EMAIL,
        "password":PASSWORD
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response = requests.request("POST", request_url, headers=headers, data=payload)
    
    if response.status_code ==200 :

        response_dict=json.loads(response.text)

        #store access token at cache file
        try:
            with open(TOKEN_FILE_PATH, 'w') as f:
                f.write(response_dict['access_token'])
                f.close()
                return response_dict['access_token']
        except Exception as e:
            print(f"Error writing token to file: {e}")
            exit()

    else:
        print('unauth!')
        exit()

def image_captcha(image_base64):
    
    request_url = "https://app.metabypass.tech/CaptchaSolver/api/v1/services/captchaSolver"

    payload=json.dumps({
        "image":f"{image_base64}" ,  #PUT CORRECT BASE64 OF IMAGE
    })

    #generate access token
    if os.path.exists(TOKEN_FILE_PATH):
        try:
            with open(TOKEN_FILE_PATH, 'r') as f:
                access_token=f.read()
                f.close()
        except Exception as e:
            print(f"Error writing token to file: {e}")
            exit()
    else:
        access_token=getNewAccessToken()

    #prepare headers
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.request("POST", request_url, headers=headers, data=payload)

    if response.status_code==401:
        access_token=getNewAccessToken()
        headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {access_token}'
        }
        response = requests.request("POST", request_url, headers=headers, data=payload)
        
    if response.status_code==200:

        response_dict=json.loads(response.text)

        if response_dict['status_code']==200:
            return response_dict['data']['result']
        else:
            print(response_dict['message'])
            return False
    else:
        return False

def image_to_base64(image_file_path):
    import base64
    with open(image_file_path, "rb") as image_file:
        image_data = image_file.read()
        base64_data = base64.b64encode(image_data).decode('utf-8')
        image_file.close()
        return base64_data


def main():

      driver = webdriver.Chrome()
      driver.get("https://prod2.seace.gob.pe/seacebus-uiwd-pub/buscadorPublico/buscadorPublico.xhtml")
      wait = WebDriverWait(driver, 10)

      action = ActionChains(driver)

      element_locatorButton = (By.ID, 'tbBuscador:idFormBuscarProceso:btnBuscarSel')
      
      elementButon = wait.until(EC.visibility_of_element_located(element_locatorButton))
      element_locatorCaptchaEditText = (By.ID, 'tbBuscador:idFormBuscarProceso:codigoCaptcha')
      elementCaptchaEditText = wait.until(EC.visibility_of_element_located(element_locatorCaptchaEditText))
      
      imageElement = driver.find_element (By.ID, 'tbBuscador:idFormBuscarProceso:captchaImg')
      src=imageElement.get_attribute("src")
      imageElement.screenshot_as_base64
      with open('article.png', 'wb') as f:
        f.write(imageElement.screenshot_as_png)
      image_base64=image_to_base64(r'.\\article.png')
      captcha_rsponse=image_captcha(image_base64)
      print(captcha_rsponse)

      elementCaptchaEditText.send_keys(captcha_rsponse)
      elementButon.click()
      
      buttonExport = driver.find_element (By.ID, 'tbBuscador:idFormBuscarProceso:btnExportar')
      time.sleep(10)

      buttonExport.click()

      
      
      
     # driver.save_screenshot()
      #sd=driver.find('#tbBuscador:idFormBuscarProceso:captchaImg').screenshot_as_png


      #tbBuscador:idFormBuscarProceso:codigoCaptcha
      
     # 


    #  
    #  tbBuscador
    #  driver.find_element(By.ID, "tbBuscador").click()
    #  driver.find_element(By.ID, "tbBuscador").click()
    #  driver.find_element(By.ID, "tbBuscador").click()

      time.sleep(30)
      print("finish")
      
      


##############


#wait(driver, 50).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='subText']")))

main()


###
#while True:
       # try:
      #  except Exception as err:
      #          print(Exception, err)
               # break
                #count_reinit=count_reinit+1
               # print("reinit "+str(count_reinit))
             #   continue




