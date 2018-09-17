# -*- coding: UTF-8 -*-

import time
import requests
from bs4 import BeautifulSoup  
from blockAll import BlockAll

def start(URL, country_href):
    """
    Parameters:
    URL = website URL -> 'https://www.transfermarkt.com.tr'
    country_href -> '/wettbewerbe/national/wettbewerbe/174' 
        - country_href is the link which belongs to a spesific country. And it includes
          all of leagues names in a table.
    """

    links_of_leagues = []

    r = send_request(URL + country_href)
    #print(r.text)

    # Soup for leagues table to get LINKS of them
    soup = BeautifulSoup(r.text, 'html.parser')

    table = soup.find_all('div', attrs = {'class' : 'responsive-table'})[0]
    
    get_links_of_leagues(table, links_of_leagues)
    
    return links_of_leagues 

def get_links_of_leagues(table, links_of_leagues):

    count = 1
    for row in table.findAll('a'):
        #start_time = time.time() # START TIME FOR ONE LEAGUE
        #currentLeague = LEAG() # CREATE LEAGUE OBJECT
        if row.get('title') != 'Müsabaka forumuna git':
            count+=1
            if count % 2 != 0:
                count=1
                league_href = row.get('href')
                league_name = row.get_text().strip()
                links_of_leagues.append((league_name, league_href))

def send_request(url):
    s = requests.Session()
    s.cookies.set_policy(BlockAll())

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'} 
    
    try:
        #time.sleep(2)
        return s.get(url, headers=headers)
    except Exception:
        print ('ERROR:(SEND REQUEST METHOD)')
        return send_request(url)

"""
l = start('https://www.transfermarkt.com.tr',
'/wettbewerbe/national/wettbewerbe/174')

for i in l:
    print (i)
"""