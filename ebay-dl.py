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
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    }
    r = requests.get(url, headers=headers)
    status = r.status_code
    print('status=', status)
    html = r.text

    # process the html
    soup = BeautifulSoup(html, 'html.parser')
    item = {}
    tags_items = soup.select('#srp-river-results li.s-item')
    
    for tag in tags_items:
        # name 
        name = None
        tag_name = tag.select_one('.s-item__title')
        for tag in tag_name:   
            name = tag.text
        print(name)
            
        # price 
        price = None 
        tags_price = tag.select('.s-item__price')

        if tags_price:
            text = tags_price.text.strip()
            text = text.replace('$', '').replace(',', '')
            first_price = text.split()[0]
            try:
                dollars = float(first_price)
                price = int(dollars * 100)
            except:
                price = None
        print(price)

        # status 
        item_status = None 
        tags_status = tag.select('.SECONDARY_INFO')
        if tags_status:
            item_status = tags_status.text.strip()

        
        # shipping 
        shipping = None
        tag_shipping = tag.select_one('.s-item__shipping')
        if tag_shipping:
            text = tag_shipping.text.strip()
            if 'Free' in text:
                shipping = 0
            else:
                text = text.replace('$', '').replace(',', '').replace('+', '')
                parts = text.split()
                try:
                    dollars = float(parts[0])
                    shipping = int(dollars * 100)
                except:
                    shipping = None

        # free returns
        freereturns = False
        tags_freereturns = tag.select('.s-item__free-returns')
        for tag_return in tags_freereturns:
            freereturns = True

        # items sold 
        items_sold = None
        tags_sold = tag.select('.s-item__hotness')
        if tags_sold:
            text = tags_sold.text.strip()
            number = text.split()[0]
            number = number.replace(',', '')
            items_sold = int(number)
        
        items.append({
            'name': name,
            'price': price,
            'status': status,
            'shipping': shipping,
            'free_returns': freereturns,
            'items_sold': items_sold,
            })

    #print('len(tags_name)=', len(tags_items))
    #print('len(tags_freereturns)=', len(tags_freereturns))
    pprint.pprint(items)

    filename = args.search_term.replace(" ", "_") + ".json"
    with open(filename, "w") as f: 
        json.dump(items, f)