import requests
from bs4 import BeautifulSoup

#Create funcion to read file url.txt to array
def read_url():
    with open('url.txt', 'r') as f:
        url_list = f.readlines()
    return url_list


#create function to user get request from url input
def get_request(url):
    response = requests.get(url)
    return response
    
#create a function to convert response to soup
def response_to_soup(response):
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup


def FindPrice(soup):
    metas = soup.find_all('meta',itemprop="price")
    if len(metas) <0:
        return 0 
    return metas[0].get('content')

def FindStock(soup):
    data = soup.find('span',class_="ui-pdp-subtitle")
    return extract_number(data.text)

def FindSold(soup):
    data = soup.find('span',class_="ui-pdp-buybox__quantity__available")
    return extract_number(data.text)

def FindName(soup):
    data = soup.find('h1',class_="ui-pdp-title")
    return data.text

#create a function an extranct number from string
def extract_number(string):
    return int(''.join(filter(str.isdigit, string)))


#create function to write to file array to csv
def write_to_csv(array):
    with open('output.csv', 'w') as f:
        f.write('name,price,stock,sold,url\n')
        for item in array:
            out = "%s,%s,%s,%s,%s"%(item["name"],item["price"],item["stock"],item["sold"],item["url"])
            f.write(out)
    return





output = []

for url in read_url():
    product = {}
    product["url"] = url
    response = get_request(url)
    soup  = response_to_soup(response)
    product["price"]  = FindPrice(soup)
    product["stock"]  = FindStock(soup)
    product["sold"]   = FindSold(soup)
    product["name"]   = FindName(soup)
    print (product)
    output.append(product)

write_to_csv(output)