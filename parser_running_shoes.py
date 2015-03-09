"""
Running Shoes Information Collector

Author: Yi Zhang
Date: Mar/08/2015
"""
from BeautifulSoup import BeautifulSoup
import urllib2
import datetime
import boto

import pandas as pd

def product_info_parser(item):
    """
    """
    components = []
    for i in item.contents:
	    if i != u"\n":
	        components.append(i)

    try:
	    ratings = components[0].findAll("div")[1]['alt']
    except:
	    ratings = None
    try:
	    n_colorways = int( components[0].div.string.split(" ")[0] )
    except:
	    n_colorways = None

    product_info = components[1].findAll("p")
    prod_name = str(product_info[0].string)
    prod_category = str(product_info[1].string)

    price_info = components[2].findAll(attrs={"class":"bulk-pricing"})
    retail_price = str(price_info[0]['data-obp'])
    bulk_price = str(price_info[0]['data-bp'])

    profile = {"name": prod_name, "category": prod_category, "num_colors": n_colorways,
	 		   "retail_price": retail_price, "bulk_price": bulk_price, 
	 		   "ratings": ratings}
    return profile

## ##############################
## collecting webpage information 
nike_running_shoes_webpage = urllib2.urlopen("http://store.nike.com/us/en_us/pw/mens-running-shoes/7puZbrkZ8yz?ipp=71")
soup = BeautifulSoup(nike_running_shoes_webpage)
all_items = soup.findAll("div", attrs = {"class": "grid-item-info"})
run_datetime_str = datetime.datetime.now().strftime("%B/%d/%Y %I:%M%p")
profiles = []
for i in all_items:
    profiles.append(product_info_parser(i))

df = pd.DataFrame(profiles)
final_output = {"datetime": run_datetime_str, "data": df.as_matrix(), "columns": df.columns}