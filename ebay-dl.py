# imports
import requests
import argparse
from bs4 import BeautifulSoup
import pprint 
import json
import re

# get command line arguments
parser = argparse.ArgumentParser(description='Download information from ebay and convert to JSON.')
parser.add_argument('search_term')
parser.add_argument('--num_pages', type=int, default=10)
args = parser.parse_args()
print('args.search_term=', args.search_term)


items = []

for page_number in range(1, int(args.num_pages)+1):

    # build the url
    url = 'https://www.ebay.com/sch/i.html?_from=R40&_nkw='
    url += args.search_term
    url += '&_sacat=0&LH_TitleDesc=0&_pgn='
    url += str(page_number)
    url += '&rt=nc'
    print('url=', url)

    # download the html
    r = requests.get(url)
    status = r.status_code
    print('status=', status)
    html = r.text

    # process the html
    soup = BeautifulSoup(html, 'html.parser')

    tags_items = soup.select('.s-item')
    
    for tag in tags_items:
        # name 
        name = None
        tags_name = tag.select('.s-item__title')
        for tag_name in tags_name:
            name = tag_name.text

        # price 
        price = None 
        tags_price = tag.select('.s-item__price')
        for tag_price in tags_price: 
            text = tag_price.text 
            match = re.search(r'\$([\d,.]+)', text)
            if match:
                dollars = float(match.group(1).replace(',', ''))
                price = int(dollars * 100)

        # status 
        status = None 
        tags_status = tag.select('.SECONDARY_INFO')
        for tag_status in tags_status:
            status = tag_status.text
        
        # shipping 
        shipping = None
        tags_shipping = tag.select('.s-item__shipping')
        for tag_ship in tags_shipping:
            text = tag_ship.text

            if 'Free' in text:
                shipping = 0
            else:
                match = re.search(r'\$([\d,.]+)', text)
                if match:
                    dollars = float(match.group(1).replace(',', ''))
                    shipping = int(dollars * 100)

        # free returns
        freereturns = False
        tags_freereturns = tag.select('.s-item__free-returns')
        for tag_return in tags_freereturns:
            freereturns = True

        items.append({
            'name': name,
            'freereturns': freereturns,
            })

    #print('len(tags_name)=', len(tags_name))
    #print('len(tags_freereturns)=', len(tags_freereturns))
    pprint.pprint(items)

    filename = args.search_term.replace(" ", "_") + ".json"
    with open(filename, "w") as f: 
        json.dump(items, f, indent = 2)