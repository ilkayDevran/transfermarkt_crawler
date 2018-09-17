# -*- coding: UTF-8 -*-

import time
import requests
from bs4 import BeautifulSoup  
from blockAll import BlockAll
from layer_2_dataBase import DataBase as DB

def start(URL, league_href):
    """
    Parameters:
    URL = website URL -> 'https://www.transfermarkt.com.tr'
    league_href -> '/super-lig/startseite/wettbewerb/TR1' 
        - league_href is the link which represent a infos and 
          teams of table of a league. 
    """

    links_of_clubs = []

    r = send_request(URL + league_href)
    #print(r.text)

    # Soup for clubs of table to get LINKS of them
    soup_of_league_page = BeautifulSoup(r.text, 'html.parser')

    #### national league checking part ####
    if (soup_of_league_page.find('th', attrs={'id':'yw1_c0'}).get_text(strip=True).strip()) != 'Kulüp':
        if (soup_of_league_page.find('th', attrs={'id':'yw1_c0'}).get_text(strip=True).strip()) != 'Verein':
            print('This is not a useful league table. Link, ', league_href)
            exit()
    
    # set league info
    league_id = set_league_infos(soup_of_league_page)


    # parsing team table in current league page to get links of teams
    # reaching to the team table in league page 
    table_of_clubs = soup_of_league_page.find('div', attrs={'id':'yw1', 'class':'grid-view'}) 
    # tbody
    tbody = table_of_clubs.find('tbody')  
    # (Kulup) column to reach the link 
    club_column = tbody.findAll('td', attrs={'class':'hauptlink no-border-links hide-for-small hide-for-pad'}) 

    # get clubs and links
    get_links_of_clubs(club_column, links_of_clubs)

    return (links_of_clubs, league_id)

def set_league_infos(soupOfLeaguePage):
    profileHeader = soupOfLeaguePage.find_all('table', attrs = {'class' : 'profilheader'})
    lst = [text for text in profileHeader[0].stripped_strings]
    
    # default values (in database everthing has been set as NOT NULL)
    name='unknown'
    country='unknown'
    league_type='unknown'
    totalValue='unknown'

    try:
        name = soupOfLeaguePage.find('h1', attrs = {'class' : 'spielername-profil'}).get_text(strip=True)
    except:
        pass

    try:
        name = soupOfLeaguePage.find('h1', attrs = {'itemprop' : 'name'}).get_text(strip=True)
    except:
        pass
    
    try:
        s = lst[lst.index('Lig seviyesi:')+1]
        try:
            league_type = s.split('\xa0')[0]
        except:
            league_type = lst[lst.index('Lig seviyesi:')+1]
            pass
    except:
        pass

    try:
        country = (lst[lst.index('Lig seviyesi:')+2].split(' '))[0]
    except:
        pass

    try:
        strng = soupOfLeaguePage.find('div', attrs = {'class' : 'marktwert'}).get_text(strip=True).split(':', 1)[-1]
        strng = strng[:strng.index('€')+1]
        strng = strng.replace("€", "Eur")
        strng = strng.replace(".", "")
        strng = strng.replace(",", ".")
        totalValue = str(strng)
    except:
        pass
    # create tuple of data like an object
    league_obj = (name,country,league_type,totalValue)
    # insert the current league infos into database
    league_id = insert_league_data_into_dataBase(league_obj)
    
    return league_id

def insert_league_data_into_dataBase(league_obj):
    db = DB('innodb')
    league_id = db.insert_league(league_obj)
 
    return league_id

def get_links_of_clubs(club_column, links_of_clubs):
    for clb in club_column:
        club_href = clb.find('a').get('href')
        club_name = clb.find('a').get_text()
        links_of_clubs.append((club_name, club_href))


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
l ,l_id= start('https://www.transfermarkt.com.tr',
    '/super-lig/startseite/wettbewerb/TR1')

print('main l_id:',l_id)
for i in l:
    print(i)
"""