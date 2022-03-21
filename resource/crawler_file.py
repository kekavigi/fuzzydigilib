from requests import get
from pickle import dump
from time import sleep
from re import compile

from bs4 import BeautifulSoup as bs
from tqdm import tqdm


remultspace = compile('[\t ]+').sub
URL = 'https://digilib.itb.ac.id/index.php/gdl/download/{}'.format
filename = 'batch_gdl_{}.pickle'.format


def crawl(gid):
    result = {'gid':gid}
    soup = bs(get(URL(gid)).text, 'lxml')
    result['file'] = soup.title.text
    try: result['url'] = soup.find('div', {'class':'pdf-viewer'}).attrs['data-url']
    except: result['url'] = ''
    return result


for batch in range(1, END, 100):
    collected = []
    for gid in tqdm(range(batch, batch+100)):
        try: collected.append(crawl(gid))
        except: pass
        sleep(5)
    with open(filename(batch), 'wb') as file:
        dump(collected, file)
