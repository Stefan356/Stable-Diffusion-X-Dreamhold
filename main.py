#Importieren der Module
import PIL.ImageShow

#import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import keyboard
import codecs
import time
import random
import json
import requests
import io
import base64
from PIL import Image, PngImagePlugin, ImageTk
import tkinter as tk

from bs4 import BeautifulSoup

# only needed for low-level NLTK summarization
#from prompt_summary import nltk_summarize

# ---IMPORTANT PARAMETERS---
# run via FHOOE-Vpn
#sdURL = "http://10.21.3.217:7860"
# run locally
sdURL = "http://127.0.0.1:7860"
imgHeight = 768
imgWidth = 768
cfg = 8
samplingSteps = 20
# alternative sampling methods include: "Euler", "Euler a", "DPM ++ SDE", ""DPM2 Karras"
samlingMethod = "Euler"
seed = random.randint(1, 1000000000)
# ------

# how many styles to choose from (needed for catching input errors)
numStyles = 4

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

# startup prompt / style select
print("Select desired visual style:\n   1: medieval fantasy, illustrated\n   2: sci-fi, futuristic, realistc\n   3: painted, Salvador Dali (experimental)\n   4: custom style (input, experimental)\n")

while True:
    try:
        styleInt = int(input("Enter number: "))
        assert numStyles >= styleInt > 0
    except (ValueError, AssertionError):
        print("Please enter a valid number between 1 and 4.")
        continue
    break

if styleInt == 1:
    prePrompt = "create an image from the perspective of the viewer where "
    stylePrompt = " medieval fantasy, ((illustrated by Adrian Smith))."
    negPrompt = "monochromatic, person, human, people"

if styleInt == 2:
    prePrompt = "create an image from the perspective of the viewer where "
    stylePrompt = " ((sci-fi)), ((futuristic)), realistic."
    negPrompt = "art, monochromatic, drawing, person, human, people"

if styleInt == 3:
    prePrompt = "create an image from the perspective of the viewer where "
    stylePrompt = " illustrated ((by Salvador Dali))."
    negPrompt = "text, person, frame"

if styleInt == 4:
    stylePrompt = "In the style of ((" + input("Please enter the desired visual style: ") + "))."
    negPrompt = "text, person, frame, human, people"

print(f"Style-prompt is now: '{stylePrompt}'")
print(f"Your seed for this run is: ", seed)

def GenerateImage(prompt, title):
    url = sdURL

    payload = {
        "prompt": prePrompt + prompt + stylePrompt,
        "steps": samplingSteps,
        "width": imgWidth,
        "height": imgHeight,
        "cfg_scale": cfg,
        "sampler_index": samlingMethod,
        "seed": seed,
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

            # change wood to metal in most furniture for sci-fi prompt
            if styleInt == 2:
                desc = desc.replace("shelve", "((futuristic, metallic)) shelve")
                desc = desc.replace("shelves", "((futuristic, metallic)) shelves")
                desc = desc.replace("cupboard", "((futuristic metallic cupboard))")
                desc = desc.replace("cupboard", "((futuristic, metallic cupboards))")
                desc = desc.replace("wooden", "((futuristic, metallic))")

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
