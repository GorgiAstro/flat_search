
import os

import requests
import telegram
from bs4 import BeautifulSoup
from dotenv import load_dotenv
load_dotenv(override=True)

DB_FILE = 'found_flats/gewobag_flats.txt'

GEWOBAG_URL = 'https://www.gewobag.de/'
GEWOBAG_ANGEBOTE_URL = GEWOBAG_URL + 'fuer-mieter-und-mietinteressenten/mietangebote/?bezirke[]=charlottenburg-wilmersdorf&bezirke[]=charlottenburg-wilmersdorf-charlottenburg&bezirke[]=friedrichshain-kreuzberg&bezirke[]=friedrichshain-kreuzberg-friedrichshain&bezirke[]=friedrichshain-kreuzberg-kreuzberg&bezirke[]=mitte&bezirke[]=mitte-gesundbrunnen&bezirke[]=mitte-moabit&bezirke[]=mitte-tiergarten&bezirke[]=mitte-wedding&bezirke[]=pankow&bezirke[]=pankow-prenzlauer-berg&bezirke[]=reinickendorf&bezirke[]=reinickendorf-hermsdorf&bezirke[]=reinickendorf-tegel&bezirke[]=reinickendorf-waidmannslust&bezirke[]=spandau&bezirke[]=spandau-hakenfelde&bezirke[]=spandau-haselhorst&bezirke[]=spandau-staaken&bezirke[]=steglitz-zehlendorf&bezirke[]=steglitz-zehlendorf-lichterfelde&bezirke[]=tempelhof-schoeneberg&bezirke[]=tempelhof-schoeneberg-lichtenrade&bezirke[]=tempelhof-schoeneberg-mariendorf&bezirke[]=tempelhof-schoeneberg-marienfelde&bezirke[]=tempelhof-schoeneberg-schoeneberg&objekttyp[]=wohnung&gesamtmiete_von=400&gesamtmiete_bis=1600&gesamtflaeche_von=70&gesamtflaeche_bis=150&zimmer_von=3&zimmer_bis=4&keinwbs=1&sort-by=recent'
#GEWOBAG_ANGEBOTE_URL = GEWOBAG_URL + 'fuer-mieter-und-mietinteressenten/mietangebote/?bezirke[]=charlottenburg-wilmersdorf&bezirke[]=charlottenburg-wilmersdorf-charlottenburg&bezirke[]=friedrichshain-kreuzberg&bezirke[]=friedrichshain-kreuzberg-friedrichshain&bezirke[]=friedrichshain-kreuzberg-kreuzberg&bezirke[]=lichtenberg&bezirke[]=lichtenberg-alt-hohenschoenhausen&bezirke[]=lichtenberg-falkenberg&bezirke[]=lichtenberg-fennpfuhl&bezirke[]=mitte&bezirke[]=mitte-gesundbrunnen&bezirke[]=mitte-moabit&bezirke[]=mitte-tiergarten&bezirke[]=mitte-wedding&bezirke[]=neukoelln&bezirke[]=neukoelln-britz&bezirke[]=neukoelln-buckow&bezirke[]=neukoelln-rudow&bezirke[]=pankow&bezirke[]=pankow-prenzlauer-berg&bezirke[]=reinickendorf&bezirke[]=reinickendorf-hermsdorf&bezirke[]=reinickendorf-tegel&bezirke[]=reinickendorf-waidmannslust&bezirke[]=reinickendorf-wittenau&bezirke[]=spandau&bezirke[]=spandau-hakenfelde&bezirke[]=spandau-haselhorst&bezirke[]=spandau-staaken&bezirke[]=steglitz-zehlendorf&bezirke[]=steglitz-zehlendorf-lichterfelde&bezirke[]=tempelhof-schoeneberg&bezirke[]=tempelhof-schoeneberg-lichtenrade&bezirke[]=tempelhof-schoeneberg-mariendorf&bezirke[]=tempelhof-schoeneberg-marienfelde&bezirke[]=tempelhof-schoeneberg-schoeneberg&bezirke[]=treptow-koepenick&bezirke[]=treptow-koepenick-niederschoeneweide&bezirke[]=treptow-koepenick-oberschoeneweide&objekttyp[]=wohnung&gesamtmiete_von=&gesamtmiete_bis=&gesamtflaeche_von=&gesamtflaeche_bis=&zimmer_von=&zimmer_bis=&sort-by=recent'

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = telegram.Bot(token=TOKEN)

with open(DB_FILE, 'r') as flat_file:
    seen_flats = flat_file.read()

response = requests.get(GEWOBAG_ANGEBOTE_URL)
if response.content is not None:
    html = BeautifulSoup(response.content, 'html.parser')
    print(html)
    for flat in html.find_all('article', attrs={'class': 'angebot-big-layout'}):
        flat_id = flat['id']
        if flat_id in seen_flats:
            continue

        with open(DB_FILE, 'a') as flat_file:
            flat_file.write(f',{flat_id}')

        flat_link = flat.find('a', attrs={'class': 'read-more-link'})['href']

        bot.send_message(
            chat_id=CHAT_ID,
            text=f'Neue Wohnung aktiv:\nID #{flat_id}\nLink: {flat_link}'
        )

print('GEWOBAG search finished')
