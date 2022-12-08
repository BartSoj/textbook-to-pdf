import requests
import shutil
import os
from time import sleep
import img2pdf
import json

requests.packages.urllib3.disable_warnings()


def get_textbook_urls(filename="textbook_urls.json"):
    with open(filename) as file:
        textbooks = json.load(file)
        return textbooks


def get_cookies(filename="cookies.txt"):
    with open(filename) as file:
        cookies = ";".join(file.read().split("\n"))
        cookies = [cookie.split("=") for cookie in cookies.split(";") if "=" in cookie]
        cookies = {key: value for key, value in cookies}
        return cookies


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


def imgs_to_pdf(pdf_path, imgs):
    if not pdf_path.endswith(".pdf"):
        pdf_path += ".pdf"

    with open(pdf_path, "wb") as file:
        file.write(img2pdf.convert(imgs))


def download_image(url, page, img_dir):
    #  sleep(0.5)  # uncomment if you get connection timeout

    page = str(page)
    #  page = page.zfill(3)  # uncomment to fill page number with leading zeros

    cookies = get_cookies()
    resp = requests.get(url.format(page), cookies=cookies, verify=False, stream=True)

    # make sure your page url returns correct status code and content type
    if resp.status_code != 200 or resp.headers["Content-Type"] != "image/jpeg":
        return

    img_path = f"{img_dir}/image{page}.jpg"
    with open(img_path, 'wb') as file:
        resp.raw.decode_content = True
        shutil.copyfileobj(resp.raw, file)

    return img_path


def run():
    textbooks = get_textbook_urls()

    for textbook, url in textbooks.items():
        textbook_dir = generate_dir(textbook)

        print(f"downloading {textbook} images from {url} to {textbook_dir}")

        imgs = []
        page = 1
        while True:
            img_path = download_image(url, page, textbook_dir)

            if img_path:
                imgs.append(img_path)
                page += 1
                print(f"{img_path} saved")
            else:
                if page > 1:
                    print(f"finished, saved {page - 1} pages")
                    break
                else:
                    print("textbook cannot be downloaded from this url")
                    return

        imgs_to_pdf(textbook_dir, imgs)
        print(f"textbook {textbook} saved as {textbook_dir}.pdf")


if __name__ == "__main__":
    run()
