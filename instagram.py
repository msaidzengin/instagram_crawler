from selenium import webdriver
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
from pandas.io.json import json_normalize
import pandas as pd
import numpy as np
import time
import json
import re


def get_profile_info(driver):
    profile_info = driver.find_element_by_class_name('zwlfE').text
    html_to_parse = str(driver.page_source)
    html = bs(html_to_parse, "html5lib")
    profile_photo = html.find("img", {"class": "_6q-tv"}).get('src')

    return profile_info, profile_photo


def load_all_page(driver):

    time.sleep(3)
    SCROLL_PAUSE_TIME = 2
    images_data = []
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            driver.execute_script("window.scrollTo(document.body.scrollHeight,0);")
            break
        last_height = new_height
        time.sleep(1)
        html_to_parse = str(driver.page_source)
        html = bs(html_to_parse, "html5lib")
        images_url = html.findAll("div", {"class": "v1Nh3 kIKUG  _bz0w"})
        images_data += images_url

    images_data = set(images_data)

    return images_data


def process_data(images_data):
    result_data = []

    for image in images_data:
        link = 'https://www.instagram.com' + image.find('a', href=True)['href']
        photo_html = image.find("img", {"class": "FFVAD"})
        content = photo_html.get('alt')
        url = photo_html.get('src')

        result_data.append({
            'post_url': link,
            'image_url': url,
            'content': content
        })

    return result_data


def main():
    path = r"/home/msaidzengin/chromedriver"
    instagram_url = 'msaidzengin'
    url = 'https://www.instagram.com/' + instagram_url
    result_name = 'result_' + instagram_url + '.json'

    driver = webdriver.Chrome(path)
    driver.get(url)
    profile_info, profile_photo = get_profile_info(driver)

    images_data = load_all_page(driver)
    driver.quit()

    post_data = process_data(images_data)

    result_data = {
        'name': instagram_url,
        'profile_info': profile_info,
        'profile_photo_url': profile_photo,
        'posts': post_data
    }

    with open(result_name, 'w', encoding='utf-8') as f:
        json.dump(result_data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()
