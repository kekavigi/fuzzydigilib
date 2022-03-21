from requests import get
from pickle import dump
from time import sleep
from re import compile

from bs4 import BeautifulSoup as bs
from tqdm import tqdm


# to make extracting process a little bit faster
remultspace = compile('[\t ]+').sub
URL = 'https://digilib.itb.ac.id/index.php/gdl/view/{}/'.format
filename = 'batch_{}.pickle'.format


def crawl(idnum):
    # get html
    soup = bs(get(URL(idnum)).text, 'lxml')
    find = soup.find
    result = {'id':idnum}

    # get title
    result['title'] = find('p', {'class':'h5 my-4 text-left'}).text.strip()
    
    # get all data from infobox
    infobox = find('footer', {'class':'blockquote-footer'})
    result['oleh'] = infobox.b.text.strip()
    for y in infobox.table.select('tr'):
        key, ddot, value = [z.text for z in y.select('td')]
        result[key] = value
    result['Staf Input/Edit'] = remultspace(' ',result['Staf Input/Edit'])
    
    # get all filelink attachments
    result['file'] = []
    for file in find('div', {'id':'panel1'}).select('h10'):
        try: href = file.a.attrs['href']
        except: href = ''
        result['file'].append((file.text.strip(), href))
    result['abstrak'] = find('div', {'id':'panel2'}).p.text.strip()
    return result


# batch download
for batch in range(1, END, 100):
    collected = []
    for idnum in tqdm(range(batch, batch+100)):
        try: collected.append(crawl(idnum))
        except: pass
        
        # to respect website traffics
        sleep(5)
    
    # save as pickle file for easy access
    with open(filename(batch), 'wb') as file:
        dump(collected, file)
