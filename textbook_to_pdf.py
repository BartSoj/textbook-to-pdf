import requests
import shutil
import os
from PIL import Image
import json

requests.packages.urllib3.disable_warnings()


def generate_dir(name="textbook"):
    dir_i = ""
    dir_path = os.path.join(os.getcwd(), name)
    while True:
        isdir = os.path.isdir(dir_path + str(dir_i))
        if not isdir:
            os.mkdir(dir_path + str(dir_i))
            break
        if not dir_i:
            dir_i = 0
        dir_i += 1
    return dir_path + str(dir_i)


cookies = {
    "wsipnet_session": "eyJpdiI6ImcwUmRmYnkyeEthWHdHXC83QkdtYmhRPT0iLCJ2YWx1ZSI6IkhtbW83Z2pldWl6THJwSkgwdTRrcUhzek5qcW9jVFk1eTFreGFmSGZZK1FCamk3T2FJUDFDT2VYdXNFUnlXWVNmd25XWTNMOVpmSUN3bkVLc3djcVZ3PT0iLCJtYWMiOiI3MzQzYzEwMWQ5YTRlZjMzZWJhNTExNDJhY2Q5ZmQ5MjZmMDFjMjdhZTYxZWUyZDg1Zjg5Y2Q1MTY2MDE4ZTk1In0"
}

with open("textbook_urls.json") as file:
    textbooks = json.load(file)

for textbook, url in textbooks.items():
    dir_path = generate_dir(textbook)

    print(f"downloading {textbook} images from {url} to {dir_path}")

    imgs = []

    i = 0
    while True:
        i += 1
        resp = requests.get(url.format(i), cookies=cookies, verify=False, stream=True)

        if resp.status_code != 200 or resp.headers["Content-Type"] != "image/jpeg":
            break

        img_path = f"{dir_path}/image{i}.jpg"
        with open(img_path, 'wb') as file:
            resp.raw.decode_content = True
            shutil.copyfileobj(resp.raw, file)

        img = Image.open(img_path)
        img = img.convert("RGB")
        imgs.append(img)
        print(f"image{i}.jpg saved")

    imgs[0].save(f"{dir_path}.pdf", save_all=True, append_images=imgs[1:])

    print(f"textbook {textbook} saved as {dir_path}.pdf")
