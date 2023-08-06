import requests
from PIL import Image
import io
import base64
from PIL import Image, PngImagePlugin


def call_interrogate(url, img_path, interrogater="blip"):
    with open(img_path, 'rb') as img:
        base64_string = base64.b64encode(img.read()).decode('utf8')

        if interrogater == "blip":
            payload = {
                "image": base64_string,
                "model": "clip",
            }
            response = requests.post(url=f'{url}/sdapi/v1/interrogate', json=payload)
            r = response.json()  
            prompt = r['caption']
        else:
            payload = {
                "image": base64_string,
                "model": "wd14-vit-v2",
            }
            response = requests.post(url=f'{url}/tagger/v1/interrogate', json=payload)
            r = response.json()  
            prompt = ','.join(list(r['caption'].keys()))

            # 이상한거 제거
            prompt = prompt.replace("general,sensitive,questionable,explicit,", "")
            prompt = prompt.replace("1boy,", "")
            prompt = prompt.replace("1girl,", "")
            prompt = prompt.replace("solo,", "")
            prompt = prompt.replace(",1boy", "")
            prompt = prompt.replace(",1girl", "")
            prompt = prompt.replace(",solo", "")

    return prompt

def call_txt2img(url, payload, save_path):
    response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)
    r = response.json()

    for i in r['images']:
        image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[0])))

        png_payload = {
            "image": "data:image/png;base64," + i
        }
        response2 = requests.post(url=f'{url}/sdapi/v1/png-info', json=png_payload)

        pnginfo = PngImagePlugin.PngInfo()
        pnginfo.add_text("parameters", response2.json().get("info"))

        image.save(save_path, pnginfo=pnginfo)

def pil_to_base64(pil_image):
    with io.BytesIO() as stream:
        pil_image.convert('RGB').save(stream, "PNG", pnginfo=None)
        base64_str = str(base64.b64encode(stream.getvalue()), "utf-8")
        return "data:image/png;base64," + base64_str
    
def call_img2img(url, payload, img_path, save_path):
    base64_string = None
    with open(img_path, 'rb') as img:
        base64_string = base64.b64encode(img.read()).decode('utf8')

    payload["init_images"] = [base64_string]
    response = requests.post(url=f'{url}/sdapi/v1/img2img', json=payload)
    r = response.json()
    
    for i in r['images']:
        image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[0])))

        png_payload = {
            "image": "data:image/png;base64," + i
        }
        response2 = requests.post(url=f'{url}/sdapi/v1/png-info', json=png_payload)

        pnginfo = PngImagePlugin.PngInfo()
        pnginfo.add_text("parameters", response2.json().get("info"))
        image.save(save_path, pnginfo=pnginfo)