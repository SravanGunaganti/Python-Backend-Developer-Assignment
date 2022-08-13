import json
import requests
import lxml
from bs4 import BeautifulSoup

def get_stripped_response(web_url):
    response = requests.get(web_url)
    stripped_response = BeautifulSoup(response.text, "lxml")
    return stripped_response


def get_tag_names_list(tag_elements):
    tag_names_list = []
    for element in tag_elements:
        tag_name = element.text.strip()
        tag_names_list.append(tag_name)
    return tag_names_list

def get_author_details(quote_container,page_url):
    author_path= quote_container.select_one('a')['href']
    reference_url = page_url.strip('/')+author_path
    stripped_author_response = get_stripped_response(reference_url)
    author_name = stripped_author_response.select_one('.author-title').text.strip()
    born_date = stripped_author_response.select_one('.author-born-date').text.strip()
    born_place = stripped_author_response.select_one('.author-born-location').text.strip()
    born_date_place = born_date +" "+ born_place
    author_item={ 'name':author_name, 'born':born_date_place, 'reference':reference_url}
    return author_item

def get_quote_details(quote_container):
    quote = quote_container.select_one('div .text').text.strip()[1:-1]
    author = quote_container.select_one('.author').text.strip()
    tag_elements = (quote_container.select('div .tag'))
    tags = get_tag_names_list(tag_elements)
    return {"quote": quote, "author": author, "tags": tags}

def get_quotes(quotes_details_list,authors_details_list,page_number,page_url):
    page_number+=1
    web_url=page_url+'page/'+str(page_number)+'/'
    quote_response=get_stripped_response(web_url)
    quote_soup=quote_response.select('div .quote')
    if quote_soup==[]:
        return quotes_details_list,authors_details_list
    for quote_container in quote_soup:
        quote_details = get_quote_details(quote_container)
        author_details = get_author_details(quote_container,page_url)
        quotes_details_list.append(quote_details)
        author_details not in authors_details_list and authors_details_list.append(author_details)
    return get_quotes(quotes_details_list,authors_details_list,page_number,page_url)


def writing_json_data_to_file(quotes_authors_details):
    json_data = json.dumps(quotes_authors_details, indent=4)
    file = open('./quotes.json','w')
    file.write(json_data)
    file.close()
    
def crawling_data_from_internet():
    page_url='http://quotes.toscrape.com/'
    quotes_details_list=[]
    authors_details_list=[]
    page_number=0
    quotes_authors_details=dict()
    get_quotes(quotes_details_list,authors_details_list,page_number,page_url)
    quotes_authors_details["quotes"]=quotes_details_list
    quotes_authors_details["authors"]=authors_details_list
    writing_json_data_to_file(quotes_authors_details)
    
crawling_data_from_internet()