# README.md

## Overview 

My ebay-dl.py file collects information from ebay about a given keyword. It stores the information in a json file.

Each item in the JSON file includes: 
(1) name - the title of the listing 
(2) price - the price of the listing 
(3) status - the listing condition or stubtitle information 
(4) shipping - the shipping cost; 0 if free 
(5) free_returns - whether the item allows free returns
(6) items_sold - the number of items sold if available 

My program automatically skips promotional listings.

## How to Run the Program 

Step 1: Install the required Python packages if you haven't already: 

```
pip3 install requests 
pip3 install beautifulsoup4 
pip3 install playwright
pip3 install ndetected-playwright 
pip3 install playwright-stealth
```

Step 2: Install the browser used by Playwright:

```
playwright install
```

Step 3: Run the scraper from the command line (terminal) with a search term. Example search terms used to generate the JSON files in this repository are iphone, laptop, and stuffed animals. If your search term is more than one word, put it in quotation marks. 

```
python3 ebay-dl.py iphone
python3 ebay-dl.py laptop
python3 ebay-dl.py "stuffed animals"
```
Step 4: If you want to save your findings to the csv files, add the --csv tag. 
```
python ebay-dl.py iphone --csv
python ebay-dl.py laptop --csv
python ebay-dl.py "stuffed animals" --csv
```

## Files in this Repository 

- ebay-dl.py: main scraping script
- iphone.json (and the .csv equivalent): scraped eBay data for iPhone listings
- stuffed_animals.json (and the .csv equivalent): scraped eBay data for stuffed animals listings
- laptop.json (and the .csv equivalent): scraped eBay data for laptop listings 

## Course Project 

Course project repository: https://github.com/mikeizbicki/cmc-csci040/tree/2026spring/project_02_webscraping


