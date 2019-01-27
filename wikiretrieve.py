import requests
from bs4 import BeautifulSoup
import wikipedia
import re
import lxml
import pandas as pd
from collections import OrderedDict
import time
import numpy as np
import string

url_input = input('Enter a valid URL: ')
url_input

class WikiRetrieve(object):
    def __init__(self, *args, **kwargs):
        self.url_input = url_input


    def url_retrieve(self, url_input):
        ''' Takes the URL input as the argument and returns a soup object of the webpage to be scraped. '''
        web = requests.request('GET', url_input)
        content = web.content
        soup = BeautifulSoup(content, 'lxml')
        return soup
# WikiSearch.url_retrieve('')
    def get_title(self, url_input):
        ''' With the help of URL supplied as an argument, identifies title tags from the webpage soup object'''
        title = WikiRetrieve.url_retrieve(self, url_input).find('h1', {'class': 'firstHeading'}).get_text()
        return title
    def get_content(self, url_input):
        ''' Uses Wikipedia API to collect plain text content from the webpages of the supplied URLs'''
        page = wikipedia.page(WikiRetrieve.get_title(self, url_input))
        body = page.content        
        return body
#wr = WikiRetrieve()    
#wr.get_content(url_input)
    def get_links(self, url_input):
        ''' Retrieves external links within Wikipedia ecosystem and also to news and articles related to the topics in webpage'''
        links = []
        for lin in WikiRetrieve.url_retrieve(self, url_input).find_all('a', {'href' : re.compile('^http://|^https://')}):
            links.append(lin.get('href'))
        return links
    def get_tables(self, url_input):
        ''' Returns tables present in the page using the table tags'''
        all_tables = WikiRetrieve.url_retrieve(self, url_input).find_all("table",{"class":["sortable", "plainrowheaders"]})
        return all_tables
    def get_tablelinks(self, url_input):
        ''' Identifies links in the table within Wikipedia pages '''        
        anchor_table = []
        for table in WikiRetrieve.get_tables(self, url_input):
            atable = WikiRetrieve.url_retrieve(self, url_input).find_all('a')
            anchor_table.append(atable)
        return anchor_table
    def get_tableheads(self, url_input):
        ''' Returns the column heads of tables in Wikipedia pages '''
        for table in WikiRetrieve.get_tables(self, url_input):
            theads = table.find_all('th')
            heads = [thead.text.strip() for thead in theads]
            return heads
        return heads
    def url_list(self, url_input):
        ''' Retrieves Wikipedia links in tables. '''
        links = []
        urllist = []
        for row in WikiRetrieve.url_retrieve(self, url_input).find(class_ = 'wikitable').find_all('tr')[1:]:
            for hyperlink in row.find_all('a'):
                links.append(hyperlink.get('href'))
        for link in links:
            web = 'https://en.wikipedia.org' + link
            urllist.append(web)
        regex = re.compile('http[s]?://([a-zA-Z.0-9]{,3}wikipedia.org/wiki/[/!@i^*$a-zA-Z0-9_-]*)(?:&quot)?')
        list_ = filter(regex.match, urllist)
        links_list = list(dict.fromkeys(list_))
        set_list = [x for x in links_list if not x.endswith('.svg')]
        return set_list
    def data2df(self, url_input):
        ''' Takes Wikipedia links in tables, visits pages, retrieves information on title, content and links and build a corpus '''
        dic = []
        titles = []
        contents = []
        exlinks = []
        for link in WikiRetrieve.url_list(self, url_input):
            try:
                WikiRetrieve.url_retrieve(self, link)
                WikiRetrieve.get_title(self, link)
                WikiRetrieve.get_content(self, link)
                WikiRetrieve.get_links(self, link)
                titles.append(WikiRetrieve.get_title(self, link))
                contents.append(WikiRetrieve.get_content(self, link))
                exlinks.append(WikiRetrieve.get_links(self, link))
            except:
                time.sleep(5)
                continue
        for title, content, links in zip(titles, contents, exlinks):
            dic.append({'Title':title, 'Content': content, 'Links':links})
        df = pd.DataFrame(dic)
        return df

# wr = WikiRetrieve(url_input)    
# wr.data2df(url_input)
