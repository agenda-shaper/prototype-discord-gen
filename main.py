import os
import openai
import random
import re
import requests
import base64
import time
import imagehash

import undetected_chromedriver.v2 as uc
from PIL import Image
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


# Load your API key from an environment variable or secret management service

# openAIkey = "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"

# openai.api_key = os.getenv(openAIkey)

# response = openai.Completion.create(model="text-davinci-003", prompt="Say this is a test", temperature=0, max_tokens=7)


options = uc.ChromeOptions()
options.headless = False
driver = uc.Chrome(use_subprocess=True, options=options)
driver.get(
    "https://discord.com/register"
)  # my own test test site with max anti-bot protection


def extract_image(element, table):

    # Get the bounding box of the element
    location = element.location
    size = element.size

    # Calculate the coordinates of the element
    left = location["x"]
    top = location["y"]
    right = left + size["width"]
    bottom = top + size["height"]

    img = table.crop((left, top, right, bottom))  # defines crop points
    return img

    # Get the screenshot of the element as binary image data
    # screenshot = driver.get_screenshot_as_png(region=(left, top, size['width'], size['height']))
    # driver.screenshot(size)

    # Create a PIL.Image object from the binary data


wait = WebDriverWait(driver, timeout=10)

WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//*")))


email = driver.find_element(By.NAME, "email").send_keys(
    "jack.the.ripper+98test@gmail.com"
)
username = driver.find_element(By.NAME, "username").send_keys("testUserJohnCena4")
time.sleep(1)
password = driver.find_element(By.NAME, "password").send_keys(
    f"testStuff895\tJuly\t13\t1998\t\t{Keys.SPACE}"
)
time.sleep(1)

month = driver.find_element(By.XPATH, "//*[contains(@class, 'button-1c')]").click()

time.sleep(3)

WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//*")))

iframe = driver.find_element(
    By.XPATH,
    '//iframe[@title="Widget containing checkbox for hCaptcha security challenge"]',
)
driver.switch_to.frame(iframe)

captcha = driver.find_element(By.ID, "anchor").click()

time.sleep(2)

driver.switch_to.default_content()

MainCaptcha = driver.find_element(
    By.XPATH, '//iframe[@title="Main content of the hCaptcha challenge"]'
)
driver.switch_to.frame(MainCaptcha)

captchaName = driver.find_element(
    By.XPATH, '//span[contains(., "Please click each image containing")]'
)

SolveDir = ""

for name in os.listdir("./img"):
    if name in captchaName.text:
        SolveDir = name
        break


# Get the text from the element


# Print the text to the console
print()
print(SolveDir)


grid = driver.find_element(
    By.CLASS_NAME, "task-grid"
)  # slots = grid.find_elements(By.CLASS_NAME,'task-image')
images = grid.find_elements(By.CLASS_NAME, "image")


png = driver.get_screenshot_as_png()
CaptchaGrid = Image.open(BytesIO(png))  # uses PIL library to open image in memory

driver.switch_to.default_content()  # leave iframe to get correct location

location = MainCaptcha.location
size = MainCaptcha.size

# Calculate the coordinates of the element
left = location["x"]
top = location["y"]
right = left + size["width"]
bottom = top + size["height"]

CaptchaGrid = CaptchaGrid.crop((left, top, right, bottom))  # defines crop points
CaptchaGrid.show()

driver.switch_to.frame(MainCaptcha)  # come back to iframe
num = 1

for image in images:
    image1_gray = extract_image(image, CaptchaGrid).convert("L")
    hash1 = imagehash.phash(image1_gray)
    image1_gray.show()
    for filename in os.listdir(f"./img/{SolveDir}"):
        image2_gray = Image.open(f"./img/{SolveDir}/{filename}").convert("L")
        hash2 = imagehash.phash(image2_gray)
        image2_gray.show()
        if hash1 == hash2:
            print(f"{num} images are identical")
            break
        else:
            print("ss")
        num += 1

    # Get the bounding box of the element

    # style = image.get_attribute("style")
    # match = re.search(r'url\((.+)\)', style)
    # if match:
    # image_url = match.group(1).strip('"')

    # Download the image from the URL
    # response = requests.get(image_url)

    # Decode the image data from the URL using the base64 encoding
    # image_data = base64.b64decode(response.content)

    # Open the image using the Image.open() method and the image data
    # try:
    # CaptchaImage = Image.open(image_data)
    # except IOError as error:
    # print("Error:", error)

    # Find the element with the ID "content"

    # Image._show(CaptchaImage)

# driver.switch_to.default_content()

time.sleep(500)
