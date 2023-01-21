![alt text](https://github.com/Stefan356/Dreamhold-X-Stable-Diffusion/blob/main/sxd_logo.png "Logo Title Text 1")

# Stable-Diffusion-X-Dreamhold
This is a semesterproject of the course Mediatechnology and -Design from the University of Applied Sciences Upper Austria.

This project aims to use Stable Diffusion to visualize the interactive fiction game Dreamhold during live play.
As soon as the player enters a new location, the respective description is modified and used as a prompt to create an image and visualize the game environments.

An example of a game environment created by Stable-Diffusion through an edited prompt taken from Dreamhold:

![alt text](https://github.com/Stefan356/Stable-Diffusion-X-Dreamhold/blob/main/vaulting_cavern.png "Image generated from Dreamhold prompt")
*A high, arched space opens around you, deep within the earth. The floor is unevenly
interspersed with stalagmites and stone columns; your torchlight glitters in droplets from the
stalactites above. Between the pale, hanging pinnacles of frozen stone, a vein of dark ore
streaks the vault.
A narrow passage leads away to the south. A broader one enters on the west side; it once
crossed the cave, but the eastern exit has collapsed. A low crawl runs northeast. At one edge of
the cave, a pit descends abruptly. Wisps of steam rise from its depths.*

## Installation and Setup

The image generation can be done locally by installing Stable Diffusion as well as on a University Server (only accessible from the FHOOE Network in Hagenberg).

### Local Image Generation

#### Install Stable Diffusion WebUI
- Install python 3.10.9 (it should work with any python version between 3.6 and 3.10
- Install git 
- Clone the Stable Diffusion webbui repo found here: https://github.com/AUTOMATIC1111/stable-diffusion-webui
- Download a model + model config (yaml) for Stable Diffusion; this was tested using Stable Diffusion 2.1, but it should work with later versions/model-checkpoints as well.
  The model can be downloaded here (5.21GB): https://huggingface.co/stabilityai/stable-diffusion-2/blob/main/768-v-ema.ckpt
  In addition to the model you need a yaml-file, which can be found here: https://raw.githubusercontent.com/Stability-AI/stablediffusion/main/configs/stable-diffusion/v2-inference-v.yaml
- Rename the yaml-file to be same name as the model-file
- Move model and yaml to the model directory in the Stable Diffusion repository. Detailed steps about the local installation of Stable Diffusion can be found at the stable-diffusion-webui repository linked above.
- Edit the file webui-user.bat found in the Stable Diffusion Web-UI main folder and add the following commandline arguments: 
  ```python
  set COMMANDLINE_ARGS= --api --xformers
  ```
  (--xformers is optional, but should allow for a more efficient image generation)
  
  ![alt text](https://github.com/Stefan356/Stable-Diffusion-X-Dreamhold/blob/main/webui-user.PNG "webui-user.bat")

#### Install Stable Diffusion X Dreamhold
- Clone the stable-diffusion-x-dreamhold repository
- Install necessary python packages either locally or in a virtual environment. Needed are: PIL (pillow), Beautiful Soup, Requests, Keyboard and Selenium
  You can use the following commands to install them via pip in Windows: 
  ```python
  pip install beautifulsoup4
  pip install selenium
  pip install keyboard
  pip install requests
  pip install Pillow
  ```
- Run webui-user.bat in the Stable Diffusion WebUI directory and wait for the setup to finish. After everything is done and the model is loaded, it should show the local URL as seen in this image:

![alt text](https://github.com/Stefan356/Stable-Diffusion-X-Dreamhold/blob/main/cmd.PNG "cmd window")

- Adjust parameters in main.py of this repository to generate the images locally:
  ```python
  url = "http://127.0.0.1:7860"
  ```
- Run stable-diffusion x dreamhold main.py

### Remote Image Generation

If you want to run our project with remote image generation, you can skip the installtion of the Stable Diffusion WebUI and only clone this repository / install the python packages mentioned above.
Just remember to change the URL for image generation to:
  ```python
  url = "http://10.21.3.217:7860"
  ```

## General Instructions

When you run main.py, a browser window opens, showing you the text of Dreamhold as well as an input field for your commands. Before an image is being generated, you have to select a desired visual style in the Python console. Currently implemented are:
1: medieval, realistic 
2: futuristic, realistc
3: painted, Salvador Dali (experimental)
4: custom style (input)

After you enter a number and press enter, a GUI window appears next to the browser window, showing you the currently active game environment. It may take a few seconds of waiting before Stable Diffusion initially stars generating an image upon the first command. In addition to that, the process of generation can take a few seconds depending on your GPU, but should not be overtly long.


## Troubleshooting

- If you get errors about the program not being able to find the images folder on your harddrive, try replacing the relative path in the code with an absolute one. (e.g. "./images/{title}.png" to "D:/projects/Stable-Diffusion-X-Dreamhold/images/{title}.png" in line 121 and 170)
- If you get errors about an out-of-date/incompatible chromium driver, downloading a new webdriver from https://chromedriver.chromium.org/downloads should solve the issue.
- If you use any 768 model for Stable Diffusion, it is avised to generate 768x768 images. If you want to change the resolution, you should also consider downloading the respective model checkpoint. 

## Credits

This project uses the Stable Diffusion WebUI (https://github.com/AUTOMATIC1111/stable-diffusion-webui) as well as the online interpreter for interactive fiction games found at https://iplayif.com/. The game Dreamhold was created by Zarfhome (https://zarfhome.com/dreamhold/). 



