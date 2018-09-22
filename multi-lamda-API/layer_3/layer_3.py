# -*- coding: UTF-8 -*-

import time
import requests
from bs4 import BeautifulSoup  
from blockAll import BlockAll
from layer_3_dataBase import DataBase as DB
from multiprocessing import Process

def start(URL, club_href, league_id):
    """
    Parameters:
    URL = website URL -> 'https://www.transfermarkt.com.tr'
    club_href -> '/galatasaray-istanbul/startseite/verein/141/saison_id/2018' 
        - club_href is the link which crawler can reach to player table of a club.
    """

    links_of_players = []

    r = send_request(URL + club_href)
    print(r.text)

    # Soup for player of table to get LINKS of them
    soup_of_club_page = BeautifulSoup(r.text, 'html.parser')
    

    # set club info
    club_id = set_club_infos(soup_of_club_page, league_id)

    # parsing player table in current team page to get links of players
    table_of_players = soup_of_club_page.find('div', attrs={'id':'yw1', 'class':'grid-view'})
    tbody = table_of_players.find('tbody')  # tbody
    rows = tbody.findAll('td', attrs = {'class':'posrela'})

    # get clubs and links
    get_links_of_players(rows, links_of_players)

    return (links_of_players, club_id)

def set_club_infos(soup_of_club_page, league_id):
    name='unknown'
    numOfPlayers=0
    avrAge=0.0
    numOflegionaries=0
    marketValue='unknown'
    try:
        name = soup_of_club_page.find('div', attrs={'class':'dataName'}).find('h1').get_text(strip=True).strip()
    except:
        pass
        
    dataContent = soup_of_club_page.find('div', attrs={'class':'dataContent'})
    dataDaten = dataContent.find_all('div', attrs={'class':'dataDaten'})[0]
    rows = dataDaten.findAll('p')

    try:
        numOfPlayers = rows[0].find('span', attrs={'class':'dataValue'}).get_text(strip=True).strip()
    except:
        pass
    try:
        avrAge = rows[1].find('span', attrs={'class':'dataValue'}).get_text(strip=True).replace(",", ".")
    except:
        pass
    try:
        strng = rows[2].find('span', attrs={'class':'dataValue'}).get_text(" ",strip=True)
        strng = strng.split(' ')
        numOflegionaries = strng[0]
    except:
        pass
    
    try:
        strng = soup_of_club_page.find('div', attrs = {'class' : 'dataMarktwert'}).get_text(strip=True).strip()
        strng = strng[:strng.index('€')+1]
        strng = strng.replace("€", "Eur")
        strng = strng.replace(".", "")
        strng = strng.replace(",", ".")
        marketValue = str(strng)
    except:
        pass

    club_obj = (name,numOfPlayers,avrAge,numOflegionaries,marketValue)
    club_id = insert_club_data_into_dataBase(club_obj,league_id)
    
    return club_id

def insert_club_data_into_dataBase(club_obj, league_id):
    db = DB('innodb')
    club_id = db.insert_club(club_obj, league_id)
 
    return club_id

def get_links_of_players(rows, links_of_players):
    team_kadro_time = 0
    count = 1 # count is used to prevent repeating same links
    for row in rows:
        for player in row.findAll('a', attrs = {'class':'spielprofil_tooltip'}):
            if count%2 == 0:
                count=1
                continue
            player_href = player.get('href')
            player_name = player.get_text().strip()
            links_of_players.append((player_name,player_href))
            count+=1

def send_request(url):
    s = requests.Session()
    s.cookies.set_policy(BlockAll())

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'} 
    try:
        
        return s.get(url, headers=headers)
    except Exception:
        print ('ERROR:(SEND REQUEST METHOD)')
        return send_request(url)

def invoke_layer_4(url):
    requests.get(url)

def main(event, context):
    # start returns  club_id in the database and links of Players of the Current CLUB
    time.sleep(1)
    players ,c_id = start('https://www.transfermarkt.com.tr', event['club_href'], int(event['league_id']) ) # '/galatasaray-istanbul/startseite/verein/141/saison_id/2018',2)

    for player in players:
        name, href = player
        url = 'https://jrhwzgwx7c.execute-api.eu-central-1.amazonaws.com/invoke/layer4' + '?player_href=' + href + '&club_id=' + str(c_id)

        # create and run process
        p = Process(target=invoke_layer_4, args=(url,))
        p.start()
        time.sleep(25/len(players))

    return players, c_id
        