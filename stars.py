import tkinter as tk
import requests
from PIL import Image, ImageTk
import io

index = 0  # 画像のindexはグローバルで管理する
image_urls = []  # Web API から取得した画像のURLを保持するリスト


def fetch_images():
    global image_urls
    url = "https://livlog.xyz/hoshimiru/constellation?lat=35.6581&lng=139.7414&date=2020-01-15&hour=20&min=00"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        for item in data['result']:
            image_urls.append(item['starImage'])
    else:
        print("Failed to fetch images from the API")


def btn_click():
    global index
    index = (index + 1) % len(image_urls)
    load_and_display_image(image_urls[index])


def load_and_display_image(url):
    response = requests.get(url)
    if response.status_code == 200:
        img_data = response.content
        img = Image.open(io.BytesIO(img_data))
        photo = ImageTk.PhotoImage(img)
        canvas.delete('p1')
        canvas.create_image(320, 213, image=photo, tag='p1')
        # Keep a reference to the photo to prevent it from being garbage collected
        canvas.image = photo
    else:
        print(f"Failed to load image from URL: {url}")


root = tk.Tk()
root.geometry('700x560')
root['bg'] = 'lightgrey'
canvas = tk.Canvas(root, width=640, height=426, bd=0, highlightthickness=0, relief='ridge')
canvas.pack(pady=20)

# 画像の取得
fetch_images()

# 初期画像の表示
if image_urls:
    load_and_display_image(image_urls[index])

btn = tk.Button(text='Click', command=btn_click)
btn.pack(ipadx=10, ipady=5)

root.mainloop()
