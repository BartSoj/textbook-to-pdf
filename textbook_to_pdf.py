import requests
import shutil
import os
from time import sleep
import img2pdf
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
    #  change your code here
    "auth_cookie": r"cookie_content"
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

        #  sleep(0.5)  # uncomment if you get connection time out

        page = str(i)
        #  page = page.zfill(3)  # uncomment to fill page number with leading zeros

        resp = requests.get(url.format(page), cookies=cookies, verify=False, stream=True)

        if resp.status_code != 200 or resp.headers["Content-Type"] != "image/jpeg":  # make sure your page url returns correct status code and content type
            break

        img_path = f"{dir_path}/image{i}.jpg"
        with open(img_path, 'wb') as file:
            resp.raw.decode_content = True
            shutil.copyfileobj(resp.raw, file)

        imgs.append(img_path)
        print(f"image{i}.jpg saved")

    with open(f"{dir_path}.pdf", "wb") as file:
        file.write(img2pdf.convert(imgs))

    print(f"textbook {textbook} saved as {dir_path}.pdf")
