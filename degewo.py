
import os

import requests
import telegram
from bs4 import BeautifulSoup
from dotenv import load_dotenv
load_dotenv(override=True)

DB_FILE = 'found_flats/degewo_flats.txt'

DEGEWO_URL = 'https://immosuche.degewo.de'
DEGEWO_ANGEBOTE_URL = DEGEWO_URL + '/de/search?size=10&page=1&property_type_id=1&categories[]=1&lat=&lon=&area=&address[street]=&address[city]=&address[zipcode]=&address[district]=&district=33%2C+46%2C+28%2C+71%2C+64%2C+4-8%2C+58%2C+60%2C+40-67&property_number=&price_switch=true&price_radio=null&price_from=&price_to=&qm_radio=custom&qm_from=70&qm_to=125&rooms_radio=custom&rooms_from=3&rooms_to=5&wbs_required=false&order=rent_total_without_vat_asc'

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = telegram.Bot(token=TOKEN)

with open(DB_FILE, 'r') as flat_file:
    seen_flats = flat_file.read()

response = requests.get(DEGEWO_ANGEBOTE_URL)
if response.content is not None:
    html = BeautifulSoup(response.content, 'html.parser')
    #print(html)
    for flat in html.find_all('article', attrs={'class': 'article-list__item article-list__item--immosearch'}):
        #print(flat)
        flat_url = flat.a['href']
        if flat_url in seen_flats:
            continue

        with open(DB_FILE, 'a') as flat_file:
            flat_file.write(f',{flat_url}')

        flat_link = DEGEWO_URL + flat_url

        bot.send_message(
            chat_id=CHAT_ID,
            text=f'Neue Degewo Wohnung!:\nLink: {flat_link}'
        )

print('DEGEWO search finished')
