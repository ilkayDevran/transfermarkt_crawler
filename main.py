# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup


def send_request(url):

    # Check 'User-Agent' whether website blocks traffic from non-browsers
    session = requests.Session()
    #print("\nSession Headers:", session.headers, "\n")

    # This is chrome, you can set whatever browser you like
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'} 
    
    try:
        r = requests.get(url, headers=headers)
    except:
        print ('ERROR:\nResponse Status:', r.status_code)
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

    
    for i in leagues_list:
        print (i)
        #print (type(i[0]),type(i[1]))
        print('\n')
    input()

    return leagues_list

def get_teams_of_league(teams_soup):
    team_list = []
    
    try:
        responsive_tables = teams_soup.find_all('div', attrs = {'class' : 'responsive-table'})
        team_info_table = responsive_tables[0]
        rows = team_info_table.findAll('td', attrs = {'class':'hauptlink no-border-links hide-for-small hide-for-pad'})
        
        for row in rows:
            club = row.get_text().strip()   #club name
            #print (club)
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

def get_players_in_team(club_soup):
    player_list = []

    try:
        tables = club_soup.find_all('table', attrs={'class':'items'})
        staff_table = tables[0]
        rows = staff_table.findAll('td', attrs = {'class':'posrela'})

        count = 1 # count is used to prevent repeating same links
        for row in rows:
            for player_link in row.findAll('a', attrs = {'class':'spielprofil_tooltip'}):
                if count%2 == 0:
                    count=1
                    continue
                player_name = player_link.text
                #print(player_name)
                player_list.append(str(player_link.get('href')))
                count+=1    
            
    except:
        print('ERROR:\n Method: get_players_in_team')
        exit()
    
    '''
    print(len(player_list))
    for i in player_list:
        print (i)
        print (type(i))
        print('\n')
    '''


    return player_list

def get_player_profile(profile_soup):
    profile = []
    
    try:
        info_table = profile_soup.find_all('table', attrs={'class':'auflistung'})
        print (info_table)
        rows = BeautifulSoup(str(info_table), "html.parser")
        #rows = info_table.findAll('tr')
        #print (rows[0])

        #BURDA KALDIN
        input()
        for tr in rows:
            info_title = tr.findAll('th')
            player_info = tr.findAll('td')
            player_data = []
            for info in player_info:
                text = info.get_text().strip()

        input()
       
            
    except:
        print('ERROR:\n Method: get_players_in_team')
        exit()
    
    '''
    print(len(profile))
    for i in profile:
        print (i)
        print (type(i))
        print('\n')
    '''


    return profile

def main():

    URL = 'https://www.transfermarkt.com.tr'

    # Lists of Necassary Infos and Links 
    country_href_list = ['/wettbewerbe/national/wettbewerbe/174'] # '/wettbewerbe/national/wettbewerbe/40'
    
    # Country Leagues -> Teams of a League -> Players in Team -> Player Info
    for country_href in country_href_list: # Country Leagues Page
        r = send_request(URL + country_href)
        # Parse the response
        soup = BeautifulSoup(r.text, 'html.parser')
        # GET LEAGUES' LINKS
        leagues = get_leagues(soup)


        for l in leagues: # League Info Page
            league_name, league_href = l
            #print ('\n\n', league_name, '\n')

            teams_r = send_request(URL + league_href)
            # Parse the response
            teams_soup = BeautifulSoup(teams_r.text, 'html.parser')
            # GET TEAMS IN LEAGUES
            teams = get_teams_of_league(teams_soup)
            

            for t in teams: # Club Info Page
                club, club_href = t
                #print '\n\n', club, '\n'

                club_r = send_request(URL + club_href)
                # Parse the response
                club_soup = BeautifulSoup(club_r.text, 'html.parser')
                # GET PLAYERS IN TEAM
                players = get_players_in_team(club_soup)


                for p_href in players: # Player Info Page
                    player_r = send_request(URL + p_href)
                    # Parse the response
                    profile_soup = BeautifulSoup(player_r.text, 'html.parser')
                    # GET PLAYER INFO
                    player_profile = get_player_profile(profile_soup)

            

        print('\n\n******************\n\n\n')


    
        

if __name__ == '__main__':
    main()