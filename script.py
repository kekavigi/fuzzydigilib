# Copyright 2023 Agapitus Keyka Vigiliant
# SPDX-License-Identifier: Apache-2.0

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from bs4 import BeautifulSoup as bs  #type: ignore

from time import sleep
from tqdm import tqdm  #type: ignore
from os import listdir
import json


options = Options()
options.add_argument('-headless')

driver = webdriver.Firefox(options=options)

def extract_page(id_library):
    driver.get(f'https://digilib.itb.ac.id/gdl/view/{id_library}')
    sleep(1)
    soup = bs(driver.page_source, 'lxml')
    find = soup.find

    data = {
        'Nomor': id_library,
        'Judul': find('h2', {
            'class': 'entry-title'
        }).text.strip(),
        'Abstrak': find('div', {
            'id': 'pills1-tab2'
        }).text.strip(),
        'Daftar File': {
            _.div.text: _.get('href')
            for _ in find('div', {
                'id': 'pills1-tab1'
            }).find_all('a')
        },
    }

    for td in soup.find_all('tr'):
        key, _, value = td.find_all('td')
        key = key.text.strip()
        if key == 'Kontributor / Dosen Pembimbing':
            value = [_.text.strip() for _ in value.find_all('li')]
        else:
            value = value.text.strip()
        data[key] = value

    return data

def save_json(id_library, data):
    g = 1+id_library//10000
    fpath = f'./raw_under_{g}0000/{id_library}.json'

    with open(fpath, 'w') as f:
        json.dump(data, f)


if __name__ == "__main__":
    limit = max(int(folder[10:]) for folder in listdir() if folder[:10]=='raw_under_')
    start = max(int(fname[:-5]) for fname in listdir(f"./raw_under_{limit}"))

    with open('config.json') as f:
        config = json.load(f)
    latest = config['latest']

    for i in tqdm(range(start,  latest+1)):
        try:
            save_json(i, extract_page(i))

        except AttributeError:
            pass