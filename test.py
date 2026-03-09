import requests
import argparse
from bs4 import BeautifulSoup
import json
import re
import time
import random

# 1. Setup Arguments
parser = argparse.ArgumentParser(description='Download information from ebay and convert to JSON.')
parser.add_argument('search_term')
parser.add_argument('--num_pages', type=int, default=3)
args = parser.parse_args()

items = []

# 2. Modern Browser Headers (Updated for 2026)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://www.google.com/",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1"
}

for page_number in range(1, args.num_pages + 1):
    url = f'https://www.ebay.com/sch/i.html?_nkw={args.search_term}&_pgn={page_number}&_ipg=60'
    print(f"Fetching: {url}")

    # Use a session to persist cookies (looks more human)
    session = requests.Session()
    session.get("https://www.ebay.com", headers=headers) # Get cookies
    r = session.get(url, headers=headers) # Now search
    
    # Check if we got the "Interruption" page
    if "pardon our interruption" in r.text.lower() or "captcha" in r.text.lower():
        print("❌ Blocked by eBay's bot detection. Use a proxy or wait 15 minutes.")
        break

    soup = BeautifulSoup(r.text, 'html.parser')
    
    # 3. Updated Selectors for 2026
    # eBay often wraps items in 's-item__wrapper' or 's-item__info'
    listings = soup.select('.s-item__wrapper')
    
    # If standard selector fails, try the older one as a backup
    if not listings:
        listings = soup.select('li.s-item')

    for container in listings:
        # Skip the "Shop on eBay" ad
        name_tag = container.select_one('.s-item__title')
        if not name_tag or "Shop on eBay" in name_tag.text:
            continue
        
        name = name_tag.get_text(strip=True)

        # Price parsing with fallback
        price_tag = container.select_one('.s-item__price')
        price_cents = None
        if price_tag:
            # Extract digits only (handles $10.00 to $20.00 ranges)
            price_match = re.search(r"(\d+\.\d+|\d+)", price_tag.text.replace(',', ''))
            if price_match:
                price_cents = int(float(price_match.group(1)) * 100)

        items.append({
            'name': name,
            'price_cents': price_cents,
            'page': page_number
        })

    print(f"✅ Found {len(listings)} items on page {page_number}")
    
    # 4. Randomized delay is mandatory in 2026
    time.sleep(random.uniform(2.0, 4.0))

# 5. Save to File
filename = f"{args.search_term.replace(' ', '_')}.json"
with open(filename, "w") as f:
    json.dump(items, f, indent=4)

print(f"\nFinished! Total items saved: {len(items)}")