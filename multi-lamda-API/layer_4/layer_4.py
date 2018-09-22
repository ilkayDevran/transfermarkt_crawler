# -*- coding: UTF-8 -*-

import time
import requests
from bs4 import BeautifulSoup  
from blockAll import BlockAll
from layer_4_dataBase import DataBase as DB

def start(URL, player_href, club_id):
    """
    Parameters:
    URL = website URL -> 'https://www.transfermarkt.com.tr'
    player_href -> '/fernando-muslera/profil/spieler/58088' 
        - player_href is the link which has all player info
    """
    r = send_request(URL + player_href)
    print(r.text)
    
    # Soup for clubs of table to get LINKS of them
    soup_of_player_page = BeautifulSoup(r.text, 'html.parser')
    
    # Set player infos
    player_data_table = soup_of_player_page.find('table', attrs={'class':'auflistung'})
    lst = [text for text in player_data_table.stripped_strings]

    if 'Geburtsdatum:' in lst:
        set_player_infos_DE(soup_of_player_page, club_id, lst)
    else:
        set_player_infos(soup_of_player_page, club_id, lst)

def set_player_infos(soup_of_player_page, club_id, lst):
    """
    player_data_table = soup_of_player_page.find('table', attrs={'class':'auflistung'})
    lst = [text for text in player_data_table.stripped_strings]
    #print(lst, '\n')
    """
    full_name = 'unknown'
    bday = 'unknown'
    bplace = 'unknown'
    age  = 'unknown'
    hight = 0.0
    nationality  = 'unknown'
    position = 'unknown'
    leg = 'unknown'
    counselar = 'unknown'
    currentClub = club_id
    joinedDate = 'unknown'
    endOfContDate = 'unknown'
    pastOfTransfers = []

    try:
        full_name = soup_of_player_page.find_all('h1',attrs={'itemprop':'name'})[0].get_text(strip=True)
        try:
            full_name = full_name.replace("'"," ")
        except:
            pass
    except:
        pass

    try:
        indx = lst.index('Doğum tarihi:')
        bday = date_converter_4_mysql(lst[indx+1])
    except:
        pass
        
    try:
        indx = lst.index('Doğduğu il:')
        bplace = lst[indx+1]
    except:
        pass

    try:
        indx = lst.index('yaş:')
        age = lst[indx+1]
    except:
        pass

    try:
        indx = lst.index('Boyu:')
        s = lst[indx+1].replace(",", ".")
        try:
            hight = s.split('\xa0')[0]
        except:
            pass
    except:
        pass

    try:
        indx = lst.index('Uyruğu:')
        nationality = lst[indx+1]
    except:
        pass

    try:
        indx = lst.index('Mevki:')
        position = lst[indx+1]
    except:
        pass

    try:
        indx = lst.index('Ayak:')
        leg = lst[indx+1]
    except:
        pass
    
    try:
        indx = lst.index('Oyuncu danışmanı:')
        counselar = lst[indx+1]
        try:
            counselar = counselar.replace("'"," ")
        except:
            pass
    except:
        pass

    try:
        indx = lst.index('Takıma katılma tarihi:')
        joinedDate = date_converter_4_mysql(lst[indx+1])
    except:
        indx = lst.index('Takıma katılma tarihi::')
        joinedDate = date_converter_4_mysql(lst[indx+1])
    else:
        pass
    try:
        indx = lst.index('Sözleşme bitiş tarihi:')  ######
        endOfContDate = date_converter_4_mysql(lst[indx+1])
    except:
        indx = lst.index('Sözleşme bitiş tarihi::')  ######
        endOfContDate = date_converter_4_mysql(lst[indx+1])
    else:
        pass

    try:
        # Transfer Table Parsing
        transfer_table = soup_of_player_page.find_all('div', attrs={'class':'responsive-table'})[0]
        rows = transfer_table.find('tbody').find_all('tr', attrs={'class':'zeile-transfer'})
        for row in rows:
            season = row.findAll('td', attrs={'class':'zentriert hide-for-small'})[0].get_text(strip=True).strip()
            date = date_converter_4_mysql(row.findAll('td', attrs={'class':'zentriert hide-for-small'})[1].get_text(strip=True).strip())
            old_team = row.findAll('td', attrs={'class':'hauptlink no-border-links hide-for-small vereinsname'})[0].find('a').get_text(strip=True).strip()
            new_team = row.findAll('td', attrs={'class':'hauptlink no-border-links hide-for-small vereinsname'})[1].find('a').get_text(strip=True).strip()
            try:
                old_team = old_team.replace("'"," ")
            except:
                pass
            try:
                new_team = new_team.replace("'"," ")
            except:
                pass
            pastOfTransfers.append((season,date,old_team,new_team))
    except:
        pastOfTransfers.append(('0/0','0000-00-00','unknow','unknow'))

    player_obj = (full_name, bday, bplace, age, hight, nationality, position, 
        leg, counselar, joinedDate, endOfContDate, pastOfTransfers)

    insert_player_data_into_dataBase(player_obj, club_id)

def set_player_infos_DE(soup_of_player_page, club_id, lst):
    """
    player_data_table = soup_of_player_page.find('table', attrs={'class':'auflistung'})
    lst = [text for text in player_data_table.stripped_strings]
    """

    full_name = 'unknown'
    bday = 'unknown'
    bplace = 'unknown'
    age  = 'unknown'
    hight = 0.0
    nationality  = 'unknown'
    position = 'unknown'
    leg = 'unknown'
    counselar = 'unknown'
    joinedDate = 'unknown'
    endOfContDate = 'unknown'
    pastOfTransfers = []

    try:
        full_name = soup_of_player_page.find_all('h1',attrs={'itemprop':'name'})[0].get_text(strip=True)
        try:
            full_name = full_name.replace("'"," ")
        except:
            pass
    except:
        pass

    try:
        indx = lst.index('Geburtsdatum:')
        bday = date_converter_4_mysql(lst[indx+1])
    except:
        pass
        
    try:
        indx = lst.index('Geburtsort:')
        bplace = lst[indx+1]
    except:
        pass

    try:
        indx = lst.index('Alter:')
        age = lst[indx+1]
    except:
        pass

    try:
        indx = lst.index('Größe:')
        s = lst[indx+1].replace(",", ".")
        try:
            hight = s.split('\xa0')[0]
        except:
            pass
    except:
        pass

    try:
        indx = lst.index('Nationalität:')
        nationality = lst[indx+1]
    except:
        pass

    try:
        indx = lst.index('Position:')
        position = lst[indx+1]
    except:
        pass

    try:
        indx = lst.index('Fuß:')
        leg = lst[indx+1]
    except:
        pass
    
    try:
        indx = lst.index('Spielerberater:')
        counselar = lst[indx+1]
        try:
            counselar = counselar.replace("'"," ")
        except:
            pass
    except:
        pass

    try:
        indx = lst.index('Im Team seit:')
        joinedDate = date_converter_4_mysql(lst[indx+1])
    except:
        indx = lst.index('Im Team seit::')
        joinedDate = date_converter_4_mysql(lst[indx+1])

    try:
        indx = lst.index('Vertrag bis:') 
        endOfContDate = date_converter_4_mysql(lst[indx+1])
    except:
        indx = lst.index('Vertrag bis::')  
        endOfContDate = date_converter_4_mysql(lst[indx+1])

    try:
        # Transfer Table Parsing
        transfer_table = soup_of_player_page.find_all('div', attrs={'class':'responsive-table'})[0]
        rows = transfer_table.find('tbody').find_all('tr', attrs={'class':'zeile-transfer'})
        for row in rows:
            season = row.findAll('td', attrs={'class':'zentriert hide-for-small'})[0].get_text(strip=True).strip()
            date = date_converter_4_mysql(row.findAll('td', attrs={'class':'zentriert hide-for-small'})[1].get_text(strip=True).strip())
            old_team = row.findAll('td', attrs={'class':'hauptlink no-border-links hide-for-small vereinsname'})[0].find('a').get_text(strip=True).strip()
            new_team = row.findAll('td', attrs={'class':'hauptlink no-border-links hide-for-small vereinsname'})[1].find('a').get_text(strip=True).strip()
            try:
                old_team = old_team.replace("'"," ")
            except:
                pass
            try:
                new_team = new_team.replace("'"," ")
            except:
                pass
            pastOfTransfers.append((season,date,old_team,new_team))
    except:
        pastOfTransfers.append(('0/0','0000-00-00','unknow','unknow'))

    player_obj = (full_name, bday, bplace, age, hight, nationality, position, 
        leg, counselar, joinedDate, endOfContDate, pastOfTransfers)

    insert_player_data_into_dataBase(player_obj, club_id)

def insert_player_data_into_dataBase(player_obj, club_id):
    db = DB('innodb')
    db.insert_player(player_obj, club_id)


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

def date_converter_4_mysql(date):
    try:
        if '.' not in date:
            months = {'Oca':'01', 'Şub':'02', 'Mar':'03', 'Nis':'04', 'May':'05', 'Haz':'06',
                'Tem':'07', 'Ağu':'08','Eyl':'09', 'Eki':'10', 'Kas':'11', 'Ara':'12'}
            date = date.split(' ')
            date = date[2] + '-' + months[date[1]] + '-' + date[0]
        else:
            date = date.split('.')
            date = date[2] + '-' + date[1] + '-' + date[0]
    except:
        return '0000-00-00'
    return date


def main(event, context):
    start('https://www.transfermarkt.com.tr', event['player_href'], int(event['club_id']) ) # '/fernando-muslera/profil/spieler/58088', 1) 
    return 'Done!'