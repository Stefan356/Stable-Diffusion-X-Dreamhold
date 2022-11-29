import json
import requests
import io
import base64
from PIL import Image, PngImagePlugin

# run locally
url = "http://127.0.0.1:7860"

# run via FHOOE-Vpn
#url = "http://10.21.3.217:7860"

payload = {
    "prompt": "a group of people in halloween outfits",
    "steps": 5
}

response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)

r = response.json()
load_r = json.loads(r['info'])
meta = load_r["infotexts"][0]

for i in r['images']:
    image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[0])))
    pnginfo = PngImagePlugin.PngInfo()
    pnginfo.add_text("parameters", meta)
    image.save('output.png', pnginfo=pnginfo)