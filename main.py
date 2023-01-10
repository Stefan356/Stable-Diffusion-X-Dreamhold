#Importieren der Module
import PIL.ImageShow

#import chromedriver_binary
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
from PIL import Image, PngImagePlugin, ImageTk
import tkinter as tk

from bs4 import BeautifulSoup

#from prompt_summary import nltk_summarize

# Optionen die für den Web Treiber gesetzt werden können...
options = webdriver.ChromeOptions()
# options.add_argument("--headless")
options.add_experimental_option("excludeSwitches", ['enable-automation'])
driver = webdriver.Chrome(options=options)

# Url aufrufen
# driver.get("http://localhost/iplayif/parchment.html")
driver.get("https://iplayif.com/")

# Link wird in Eingabefeld kopiert und Enter gedrückt = Seite lädt Spiel
elem = driver.find_element(By.ID, "play-url-input")
elem.send_keys("https://eblong.com/zarf/ftp/dreamhold.z8")
elem.send_keys(Keys.RETURN)

# Variable für While Schleife
gameRunning = True

# GUI
root = tk.Tk()

# get screen width and height
ws = root.winfo_screenwidth()  # width of the screen
hs = root.winfo_screenheight()  # height of the screen

root.title("Dreamhold")
# position window on left side of the screen
root.geometry('%dx%d+%d+%d' % (ws / 2, hs, ws / 2, 0))

label = tk.Label(root)
label.pack(side="top", expand=True, fill="both")
tkimg = [None]

# list storing titles of already generated images
already_generated = []

# style prompt variables
prePrompt = "create an image from the perspective of the viewer where "
stylePrompt = " medieval, hyper-realistic."
negPrompt = "art, monochromatic, abstract, drawing, person, human, people"
numstyle = 1

# startup prompt / style select
print("Select desired visual style:\n   1: medieval, realistic\n   2: futuristic, realistc\n   3: painted, Salvador Dali (experimental)\n")

while True:
    try:
        numstyle = int(input("Enter number (default = 1): "))
    except ValueError:
        print("Please enter a valid number.")
        continue
    else:
        break

if numstyle == 1:
    prePrompt = "create an image from the perspective of the viewer where "
    stylePrompt = " medieval, by Adrian Smith."
    negPrompt = "monochromatic, person, human, people"

if numstyle == 2:
    stylePrompt = " sci-fi, futuristic, hyper-realistic."
    negPrompt = "art, monochromatic, abstract, drawing, person"

if numstyle == 3:
    stylePrompt = " illustrated by Salvador Dali."
    negPrompt = "text, person, frame"

print(f"Style-prompt is now: '{stylePrompt}'")

def GenerateImage(prompt, title):
    # run locally
    url = "http://127.0.0.1:7860"

    # run via FHOOE-Vpn
    #url = "http://10.21.3.217:7860"

    payload = {
        "prompt": prePrompt + prompt + stylePrompt,
        "steps": 20,
        "width": 768,
        "height": 768,
        "negative_prompt": negPrompt
    }

    response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)

    r = response.json()
    load_r = json.loads(r['info'])
    meta = load_r["infotexts"][0]

    for i in r['images']:
        image = Image.open(io.BytesIO(base64.b64decode(i.split(",", 1)[0])))
        pnginfo = PngImagePlugin.PngInfo()
        pnginfo.add_text("parameters", meta)
        image.save(f"./images/{title}.png", pnginfo=pnginfo)

    return image

# generate image of starting area for Dreamhold
desc = 'This space, barely wider than outstretched arms, seems to have been chopped raw and square from unfinished stone. Only the floor is smooth -- a fine white surface beneath your feet. There is a narrow gap in the east wall.'
name = 'Cell'
img = GenerateImage(desc, name)
already_generated.append(name)

# show image
tkimg[0] = ImageTk.PhotoImage(img)
label.config(image=tkimg[0])

while gameRunning:
    time.sleep(0.25)

    # Warten auf Keyboard input
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

            # summarize description
            #desc_sum = nltk_summarize(desc)

            open('file.txt', 'w').close()
            with open("file.txt",
                      "w") as f:  # ("D:\\Daten\\FH dump\\Nextcloud Folder\\Pro5\\Pro5_test_project\\file.txt", "w")
                f.write(desc)
            print(name)
            print(desc)

            # generate and show image
            if name not in already_generated:
                img = GenerateImage(desc, name)
                already_generated.append(name)
            else:
                img = Image.open(f"./images/{name}.png")

            # swap image
            tkimg[0] = ImageTk.PhotoImage(img)
            label.config(image=tkimg[0])
            # update window
            root.update()
            break

        if keyboard.is_pressed("esc"):
            gameRunning = False
            driver.close()
            root.destroy()
            root.update()
            print("Game Ended")
            break

        root.update()
