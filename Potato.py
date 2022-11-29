#Importieren der Module
import PIL.ImageShow
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import keyboard
import codecs
import time
import json
import requests
import io
import base64
from PIL import Image, PngImagePlugin

from bs4 import BeautifulSoup


# Optionen die für den Web Treiber gesetzt werden können...
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ['enable-automation'])
driver = webdriver.Chrome(options = options)


#Url aufrufen
#driver.get("http://localhost/iplayif/parchment.html")
driver.get("https://iplayif.com/")

#Link wird in Eingabefeld kopiert und Enter gedrückt = Seite lädt Spiel
elem = driver.find_element(By.ID, "play-url-input")
elem.send_keys("https://eblong.com/zarf/ftp/dreamhold.z8")
elem.send_keys(Keys.RETURN)


#Variable für While Schleife
gameRunning = True

def GenerateImage(prompt):
    # run locally
    url = "http://127.0.0.1:7860"

    # run via FHOOE-Vpn
    #url = "http://10.21.3.217:7860"

    payload = {
        "prompt": prompt,
        "steps": 25
    }

    response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)

    r = response.json()
    load_r = json.loads(r['info'])
    meta = load_r["infotexts"][0]

    for i in r['images']:
        image = Image.open(io.BytesIO(base64.b64decode(i.split(",", 1)[0])))
        pnginfo = PngImagePlugin.PngInfo()
        pnginfo.add_text("parameters", meta)
        image.save('output.png', pnginfo=pnginfo)

#show image of starting area for Dreamhold
desc = 'This space, barely wider than outstretched arms, seems to have been chopped raw and square from unfinished stone. Only the floor is smooth -- a fine white surface beneath your feet. There is a narrow gap in the east wall.'
GenerateImage(desc)
image = Image.open('output.png')
image.show()
    
while gameRunning:
    time.sleep(0.25)

    #Warten auf Keyboard input
    while True:
        if keyboard.is_pressed("return"):

            # open html - aktuell laufendes HTML
            doc = driver.page_source

            # Initialize the object with the document
            soup = BeautifulSoup(doc, "html.parser")

            # find last subheader in html (i.e. the name of the current room the player is in)
            last_subheader = soup("div", {"class": "Style_subheader"})[-1]

            # get text of next 'div'-element (description of current room)
            desc = last_subheader.find_next('div').text
            name = last_subheader.text

            open('file.txt', 'w').close()
            with open("file.txt", "w") as f:   #("D:\\Daten\\FH dump\\Nextcloud Folder\\Pro5\\Pro5_test_project\\file.txt", "w")
                f.write(desc)
            print(name)
            print(desc)

            #generate and show image
            GenerateImage(desc)
            image = Image.open('output.png')
            image.show()
            break

        if keyboard.is_pressed("esc"):
            gameRunning = False
            print("Game Ended")
            break


   