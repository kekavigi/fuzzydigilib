from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from bs4 import BeautifulSoup as bs  #type: ignore

from time import sleep
from tqdm import tqdm  #type: ignore
import json

PATH_PROFILE = r'C:/Users/kekav/Documents/Koding/fuzzydigilib/profile'
PATH_GECKOD = r'C:/Users/kekav/Documents/Koding/fuzzydigilib/geckodriver.exe'
PATH_BINARY = r'C:/Program Files/Mozilla Firefox/firefox.exe'

options = Options()
options.headless = True
binary = FirefoxBinary(PATH_BINARY)
profile = FirefoxProfile(PATH_PROFILE)

driver = webdriver.Firefox(firefox_binary=binary,
                           firefox_profile=profile,
                           options=options)


def extract_page(id_library, folder):
    driver.get(f'https://digilib.itb.ac.id/gdl/view/{id_library}')
    sleep(0.5)
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

    with open(f'./{folder}/{id_library}.json', 'w') as f:
        json.dump(data, f)


start  = 69_040
end    = 70_000
folder = f"raw_under_{end}"

for i in tqdm(range(start,  end)):
    try:
        extract_page(i, folder)
    except AttributeError:
        pass