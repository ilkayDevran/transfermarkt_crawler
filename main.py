# -*- coding: utf-8 -*-

'''
    ######################################
    #             Python 2.7             #      
    # __author__ = "İlkay Tevfik Devran" #   
    # __date__ = "07.09.2018"            #
    # __email__ = "devrani@mef.edu.tr"   # 
    ######################################
'''

import requests
import re
from bs4 import BeautifulSoup


def player_info_deneme():

    # Website URL
    durl = 'https://www.transfermarkt.com.tr/aktuell/newsarchiv'
    muslera_url = 'https://www.transfermarkt.com.tr/fernando-muslera/profil/spieler/58088'
    ronaldo_url = 'https://www.transfermarkt.com.tr/cristiano-ronaldo/profil/spieler/8198'
    
    # Get response 'r'
    r = send_request(url)

    # parse the response
    soup = BeautifulSoup(r.text, 'html.parser')

    try:
        table = soup.find('table')
        rows = table.findAll('tr')

        for tr in rows:
            info_title = tr.findAll('th')
            player_info = tr.findAll('td')
            player_data = []
            for info in player_info:
                text = info.get_text().strip()
                
                
            '''for td in player_info:
                text = ''.join(td)
                utftext = str(text.encode('utf-8'))
                text_data.append(utftext) # EDIT
            print (text_data)'''
    except:
		pass

def conv(a):
    a = str(a)
    for x in range(0, len(a)):
        a = a.replace('\"', '\'')
        a = a.replace('İ', 'I')
        a = a.replace('Ş', 's')
        a = a.replace('Ç', 'C')
        a = a.replace('Ü', 'U')
        a = a.replace('Ö', 'O')
        a = a.replace('ş', 's')
        a = a.replace('ğ', 'g')
        a = a.replace('ı', 'i')
        a = a.replace('ö', 'o')
        a = a.replace('ü', 'u')
        a = a.replace('ç', 'c')
        a = a.replace('/', '-')

    return a




def send_request(url):

    # Check 'User-Agent' whether website blocks traffic from non-browsers
    session = requests.Session()
    #print("\nSession Headers:", session.headers, "\n")

    # This is chrome, you can set whatever browser you like
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'} 
    
    try:
        r = requests.get(url, headers=headers)
    except:
        print 'ERROR:\nResponse Status:', r.status_code
        exit()

    return r

def get_leagues(soup):
    leagues_list = []

    try:
        for level1 in soup.find_all('div', attrs = {'class' : 'row'}):
            for level2 in level1.findAll('div', attrs = {'class' : 'large-8 columns'}):
                box_of_leagues = level2.findAll('div', attrs = {'class' : 'box'})[0]
        
        # Get Names and href links of Leagues
        table_of_leagues = BeautifulSoup(str(box_of_leagues.find('div', attrs = {'class' : 'responsive-table'})),'html.parser')
        for line in table_of_leagues.find_all('table', attrs = {'class':'inline-table'}):
            name = line.get_text().strip()   #leauge name
            for league_link in line.findAll('a'):
                if league_link.get('title') != None:
                    link = league_link.get('href')  #league href
            leagues_list.append((name,str(link)))
                    
    except:
        print('ERROR:\n Method: get_leagues')
        exit()

    '''
    for i in leagues_list:
        print (i)
        print (type(i[0]),type(i[1]))
        print('\n')
    '''

    return leagues_list

def get_teams_of_league(teams_soup):
    team_list = []
    
    try:
        responsive_tables = teams_soup.find_all('div', attrs = {'class' : 'responsive-table'})
        team_info_table = responsive_tables[0]
        rows = team_info_table.findAll('td', attrs = {'class':'hauptlink no-border-links hide-for-small hide-for-pad'})
        
        for row in rows:
            club = row.get_text().strip()   #club name
            print club
            for team_link in row.findAll('a'):
                team_link = team_link.get('href').strip()
                if team_link != '#':
                    team_list.append((club, str(team_link)))
        
    except:
        print('ERROR:\n Method: get_teams_of_league')
        exit()

    '''
    for i in team_list:
        print (i)
        print (type(i[0]),type(i[1]))
        print('\n')
    '''

    return team_list


def main():

    URL = 'https://www.transfermarkt.com.tr'

    # Lists of Necassary Infos and Links 
    country_href_list = ['/wettbewerbe/national/wettbewerbe/174'] # '/wettbewerbe/national/wettbewerbe/40'
    
    # Country Leagues -> Teams of a League -> Team Players -> Player Info
    for country_href in country_href_list:
        r = send_request(URL + country_href)
        # Parse the response
        soup = BeautifulSoup(r.text, 'html.parser')
        # GET LEAGUES' LINKS
        leagues= get_leagues(soup)

        
        for l in leagues:
            league_name, league_href = l
            print '\n\n', league_name, '\n'

            teams_r = send_request(URL + league_href)
            # Parse the response
            teams_soup = BeautifulSoup(teams_r.text, 'html.parser')
            # GET TEAMS IN LEAGUES
            list_of_teams = get_teams_of_league(teams_soup)
            
            

        print('\n\n******************\n\n\n')


    
        

if __name__ == '__main__':
    main()



