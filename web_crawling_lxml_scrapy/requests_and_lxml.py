import os
import json
import requests
from lxml import html


############################## DOWNLOAD TOP PAGE ##############################
#
# Start by downloading the main page you want to extract information from.
# - Use requests to get the page content
# - Cache the page in a file for analysis and to avoid over-scraping
#
###############################################################################
print("""
--------------- DOWNLOADING TOP PAGE ---------------
""")

# specify the url
url = 'https://webscraper.io/test-sites/e-commerce/allinone'
cache_filename = url.replace('/','|') + '.html'

if not os.path.isfile('cache/'+cache_filename):
    print(f"Scraping: {cache_filename}")
    
    # query the website and return the html (stored in the 'content' method)
    response = requests.get(url)
    content = response.content
    
    # save the html to disk so we can look at it at another time
    os.makedirs('cache/', exist_ok=True)
    with open('cache/'+cache_filename, 'wb') as f:
        f.write(content)

else:
    print(f"Loading from cache: {cache_filename}")
    with open('cache/'+cache_filename, 'rb') as f:
        content = f.read()
        
        
############################## EXTRACT CATEGORIES #############################
#
# From the page content use the lxml XPath functionality to get the categories
# - `html.fromstring` parses the page content
# - `nodes.xpath` extracts the relevant relative links from the nav bar
#
###############################################################################
print("""
--------------- EXTRACT CATEGORIES ---------------
""")

# parse the html using lxml
nodes = html.fromstring(content)

# relative link extracted using xpath
rel_category_urls = nodes.xpath('//ul[@class="nav"]/li/a[@class="category-link "]/@href')

# full link by combining the domain with the relative links
full_category_urls = ['https://webscraper.io'+u for u in rel_category_urls]

print(json.dumps(full_category_urls, indent=2))


############################## EXTRACT SUB-CATEGORIES #########################
#
# For each of the extracted categories URL get the sub-categories with XPath
# - Download the content of the categories pages with requests
# - Parse the content with lxml.fromstring
# - Extracts the relevant sub-category relative links from the nav bar
#
###############################################################################
print("""
--------------- EXTRACT SUB-CATEGORIES ---------------
""")

all_sub_category_urls = []

for url in full_category_urls:
    cache_filename = url.replace('/','|') + '.html'
    
    if not os.path.isfile('cache/'+cache_filename):
        print(f"Scraping: {cache_filename}")

        # query the website and return the html
        response = requests.get(url)
        content = response.content
        with open('cache/'+cache_filename, 'wb') as f:
            f.write(content)
    
    else:
        print(f"Loading from cache: {cache_filename}")
        with open('cache/'+cache_filename, 'rb') as f:
            content = f.read()
    
    # parse the html using lxml
    tree = html.fromstring(content)

    # extract the sub-category urls using xpath 
    rel_sub_category_urls = tree.xpath('//ul[@class="nav"]//li/a[@class="subcategory-link "]/@href')
    full_sub_category_urls = ['https://webscraper.io'+u for u in rel_sub_category_urls]
    
    # store all in a list
    all_sub_category_urls += full_sub_category_urls
    
print(json.dumps(all_sub_category_urls, indent=2))


############################## EXTRACT ITEMS INFO #############################
#
# For each of the extracted sub-categories URL get each item infor with XPath
# - Download the content of the sub-categories pages with requests
# - Parse the content with lxml.fromstring
# - Extracts the relevant information for each item using XPath
#
###############################################################################
print("""
--------------- EXTRACT ITEMS INFO ---------------
""")


def extract_items_from_url(url):
    """Example extractor for https://webscraper.io/test-sites/e-commerce/allinone
    items.
    
    Args:
        url (str): The url we which to scrape
    
    Returns:
        list(dict): The parsed items information.
    """
    
    cache_filename = url.replace('/','|') + '.html'
    
    if not os.path.isfile('cache/'+cache_filename):
        print(f"Scraping: {cache_filename}")
        
        # query the website and return the html
        response = requests.get(url)
        content = response.content
        with open('cache/'+cache_filename, 'wb') as f:
            f.write(content)
    
    else:
        print(f"Loading from cache: {cache_filename}")
        with open('cache/'+cache_filename, 'rb') as f:
            content = f.read()
    
    # parse the html using lxml
    root_node = html.fromstring(content)
    
    # get item nodes
    nodes = root_node.xpath('//div[@class="col-sm-4 col-lg-4 col-md-4"]')

    all_items = []

    # loop through all relevant nodes and extract 
    # the relevant information for each item using XPath
    for node in nodes:
        all_items.append(
            {
                'image_url':node.xpath('//img')[0].attrib['src'],
                'price':node.xpath('//h4[contains(@class, "price")]')[0].text,
                'title':node.xpath('//h4/a[@class="title"]')[0].text,
                'product_url':node.xpath('//h4/a[@class="title"]')[0].attrib['href'],
                'description':node.xpath('//p[@class="description"]')[0].text,
                'review':node.xpath('//div[@class="ratings"]/p')[0].text,
                'ratings':node.xpath('//div[@class="ratings"]/p[boolean(@data-rating)]')[0].attrib['data-rating'],
            }
        )

    return all_items


all_items = []

for url in all_sub_category_urls:
    all_items += extract_items_from_url(url)

print(f"Number of items: {len(all_items)}")
print(json.dumps(all_items[:1], indent=2))