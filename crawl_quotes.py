import json
import requests
import lxml
from bs4 import BeautifulSoup

def getResponse(web_url): 
    response = requests.get(web_url)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup


def getTagNames(tag_elements):
    tagNames = []
    for element in tag_elements:
        tagName = element.text.strip()
        tagNames.append(tagName)
    return tagNames

def getAuthorDictionary(author_link):
    reference = url.strip('/')+author_link
    response = requests.get(reference)
    author_soup = BeautifulSoup(response.text, "lxml")
    author_name = author_soup.select_one('.author-title').text.strip()
    born_date = author_soup.select_one('.author-born-date').text.strip()
    born_place = author_soup.select_one('.author-born-location').text.strip()
    born = born_date +" "+ born_place
    reference = response.url
    return { 'name':author_name, 'born':born, 'reference':reference}

def getQuoteDictionary(quote_container):
    quote = quote_container.select_one('div .text').text.strip()
    author = quote_container.select_one('.author').text.strip()
    tag_elements = (quote_container.select('div .tag'))
    tags = getTagNames(tag_elements)
    return {"quote": quote[1:len(quote)-1], "author": author, "tags": tags}

def getquotes(quotes_list,authors_list,page_number,url):
    page_number+=1
    web_url=url+'page/'+str(page_number)+'/'
    quote_soup=getResponse(web_url).select('div .quote')
    if page_number >10:
        return quotes_list,authors_list
    for quote_container in quote_soup:
        quote_dictionary = getQuoteDictionary(quote_container)
        author_tag= quote_container.select_one('a')['href']
        author_dictionary = getAuthorDictionary(author_tag)
        quotes_list.append(quote_dictionary)
        if author_dictionary not in authors_list :
            authors_list.append(author_dictionary)
    return getquotes(quotes_list,authors_list,page_number,url)
    
url='http://quotes.toscrape.com/'
quotes_list=[]
authors_list=[]
page_number=0
quotes,authors=getquotes(quotes_list,authors_list,page_number,url)
quotes_authors_dictionary=dict()
quotes_authors_dictionary["quotes"]=quotes_list
quotes_authors_dictionary["authors"]=authors_list


json_data = json.dumps(quotes_authors_dictionary, indent=4)
file = open('./quotes.json','w')
file.write(json_data)
file.close()