# -*- coding: UTF-8 -*-

import requests
from bs4 import BeautifulSoup
from league import League as LEAG
from club import Club as CLB
from player import Player as PLYR
from dataBase import DataBase as DB
import time
from http import cookiejar  


class TransferMarktCrawler:
    def  __init__(self, s, e):
        self.strt = s
        self.end = e
        self.URL = 'https://www.transfermarkt.com.tr'
        self.country_href_list = ['/wettbewerbe/national/wettbewerbe/174']
        self.leagues = []
        self.db = DB('innodb')

    def start(self):
        for country_href in self.country_href_list: # Country Leagues Page
            r = self.send_request(self.URL + country_href)
            print(r.text)
            soup = BeautifulSoup(r.text, 'html.parser')
            tables = [soup.find_all('div', attrs = {'class' : 'responsive-table'})[0]]
            print(tables)
            for table in tables:
                self.leagues_loop(table)

    # LOOPS
    def leagues_loop(self,table):
        count = 1
        for league_link in table.findAll('a'):
            start_time = time.time() # START TIME FOR ONE LEAGUE
            currentLeague = LEAG() # CREATE LEAGUE OBJECT
            if league_link.get('title') != 'Müsabaka forumuna git':
                count+=1
                if count % 2 != 0:
                    count=1
                    league_href = league_link.get('href')
                    # Go Into Current LEAGUE Page and Initialize a League Object
                    leaguePage_r = self.send_request(self.URL + league_href)

                    soupOfLeaguePage = BeautifulSoup(leaguePage_r.text, 'html.parser')

                    if (soupOfLeaguePage.find('th', attrs={'id':'yw1_c0'}).get_text(strip=True).strip()) != 'Kulüp':
                        if (soupOfLeaguePage.find('th', attrs={'id':'yw1_c0'}).get_text(strip=True).strip()) != 'Verein':
                            print('This is not a useful league table. Link, ', league_href)
                            continue
                                
                    # set league info
                    self.set_league_infos(currentLeague,soupOfLeaguePage, league_href)
                    print(currentLeague.name, currentLeague.type, '------------------------')

                    # parsing team table in current league page to get links of teams
                    table_of_teams = soupOfLeaguePage.find('div', attrs={'id':'yw1', 'class':'grid-view'}) # reaching to the team table in league page 
                    tbody = table_of_teams.find('tbody')  # tbody
                    club_column = tbody.findAll('td', attrs={'class':'hauptlink no-border-links hide-for-small hide-for-pad'}) # (Kulup) column to reach the link

                    self.clubs_loop(club_column, currentLeague)
                else:
                    continue
            else:
                continue


            print("League:--- %s seconds ---" % (time.time() - start_time))
            self.leagues.append(currentLeague)
            
            print('\n\nInsertion time**************')
            start_time = time.time() # START TIME FOR ONE LEAGUE
            self.db.insert_league_data(currentLeague)
            print("Insertion Time:--- %s seconds ---" % (time.time() - start_time))
            print('Insertion has been complited! :)')
            print('\n\n\n')
            exit()

    def clubs_loop(self, club_column, currentLeague):
        for i in range(self.strt, self.end):
            clb = club_column[i]
            #start_time = time.time() # START TIME FOR ONE Club
            currentTeam = CLB() # CREATE CLUB OBJECT
            club_href = clb.find('a').get('href')

            # Go Into Current TEAM Page and Initialize a Team Object
            """------------********-----------"""
            teamPage_r = self.send_request(self.URL + club_href)
            """------------********-----------"""

            soupOfTeamPage = BeautifulSoup(teamPage_r.text, 'html.parser')
            
            # Set current team info
            self.set_club_infos(currentTeam, soupOfTeamPage, club_href)
            
            print(currentTeam.name)

            # parsing player table in current team page to get links of player profiles
            table_of_players = soupOfTeamPage.find('div', attrs={'id':'yw1', 'class':'grid-view'})
            tbody2 = table_of_players.find('tbody')  # tbody
            rows = tbody2.findAll('td', attrs = {'class':'posrela'})
            
            self.players_loop(rows, currentTeam)
            currentLeague.clubs.append(currentTeam)
            #print("Team:--- %s seconds ---" % (time.time() - start_time))
   
    def players_loop(self,rows, currentTeam):
        team_kadro_time = 0
        count = 1 # count is used to prevent repeating same links
        for row in rows:
            for player in row.findAll('a', attrs = {'class':'spielprofil_tooltip'}):
                if count%2 == 0:
                    count=1
                    continue
                player_href = player.get('href')
                count+=1
                #start_time = time.time() # START TIME FOR ONE Player
                currentPlayer = PLYR()  # CREATE PLAYER OBJECT

                """!!!!!!!------------********-----------"""
                # Go Into Current PLAYER Page and Initialize a Player Object
                playerProfile_r = self.send_request(self.URL + player_href)
                """!!!!!!!------------********-----------"""

                soupOfPlayerProfile = BeautifulSoup(playerProfile_r.text, 'html.parser')
                
                # Set player infos
                try:
                    self.set_player_infos(currentPlayer, soupOfPlayerProfile, player_href)
                except:
                    self.set_player_infos_DE(currentPlayer, soupOfPlayerProfile, player_href)
                else:
                    pass
                currentTeam.players.append(currentPlayer)
                #print("Player:--- %s seconds ---" % (time.time() - start_time))
                #team_kadro_time += (time.time() - start_time)
        #print("Team_Kadro_time:--- %s seconds ---" % team_kadro_time)
                

    
    # SETTERS IN BELOW

    def set_league_infos(self, leagueObj, soupOfLeaguePage,link):
        profileHeader = soupOfLeaguePage.find_all('table', attrs = {'class' : 'profilheader'})
        lst = [text for text in profileHeader[0].stripped_strings]
        try:
            leagueObj.name = soupOfLeaguePage.find('h1', attrs = {'class' : 'spielername-profil'}).get_text(strip=True)
        except:
            pass
        try:
            s = lst[lst.index('Lig seviyesi:')+1]
            try:
                leagueObj.type = s.split('\xa0')[0]
            except:
                leagueObj.type = lst[lst.index('Lig seviyesi:')+1]
                pass
        except:
            pass
        try:
            leagueObj.name = soupOfLeaguePage.find('h1', attrs = {'itemprop' : 'name'}).get_text(strip=True).strip()
        except:
            pass
        try:
            leagueObj.country = (lst[lst.index('Lig seviyesi:')+2].split(' '))[0]
        except:
            pass
        try:
            leagueObj.totalValue = soupOfLeaguePage.find('div', attrs = {'class' : 'marktwert'}).get_text(strip=True).strip().split(':', 1)[-1]
        except:
            pass
        leagueObj.href = link  #league href
        #leagueObj.toString()
        #leagueObj.dataTypestoString()
        #input()

        
    def set_club_infos(self, teamObj, soupOfTeamPage, link):
        try:
            teamObj.name = soupOfTeamPage.find('div', attrs={'class':'dataName'}).find('h1').get_text(strip=True).strip()
        except:
            pass
            
        dataContent = soupOfTeamPage.find('div', attrs={'class':'dataContent'})
        dataDaten = dataContent.find_all('div', attrs={'class':'dataDaten'})[0]
        rows = dataDaten.findAll('p')
        try:
            teamObj.numOfPlayers = rows[0].find('span', attrs={'class':'dataValue'}).get_text(strip=True).strip()
        except:
            pass
        try:
            teamObj.avrAge = rows[1].find('span', attrs={'class':'dataValue'}).get_text(strip=True).replace(",", ".")
        except:
            pass
        try:
            strng = rows[2].find('span', attrs={'class':'dataValue'}).get_text(" ",strip=True)
            strng = strng.split(' ')
            teamObj.numOflegionaries = strng[0]
        except:
            pass
        
        try:
            strng = soupOfTeamPage.find('div', attrs = {'class' : 'dataMarktwert'}).get_text(strip=True).strip()
            strng = strng[:strng.index('€')+1]
            strng = strng.replace("€", "Eur")
            strng = strng.replace(".", "")
            strng = strng.replace(",", ".")
            teamObj.marketValue = int(strng)
        except:
            pass

        teamObj.href = link
        
        #teamObj.toString()
        #teamObj.dataTypestoString()
        #input()


    def set_player_infos(self, playerObj, soupOfPlayerProfile, link):
        player_data_table = soupOfPlayerProfile.find('table', attrs={'class':'auflistung'})
        lst = [text for text in player_data_table.stripped_strings]
        #print(lst, '\n')
        try:
            playerObj.full_name = soupOfPlayerProfile.find_all('h1',attrs={'itemprop':'name'})[0].get_text(strip=True)
            try:
                playerObj.full_name = playerObj.full_name.replace("'"," ")
            except:
                pass
        except:
            pass
        try:
            indx = lst.index('Doğum tarihi:')
            playerObj.bday = self.date_converter_4_mysql(lst[indx+1])
        except:
            pass
        try:
            indx = lst.index('Doğduğu il:')
            playerObj.bplace = lst[indx+1]
        except:
            pass
        try:
            indx = lst.index('yaş:')
            playerObj.age = lst[indx+1]
        except:
            pass
        try:
            indx = lst.index('Boyu:')
            s = lst[indx+1].replace(",", ".")
            try:
                playerObj.hight = s.split('\xa0')[0]
            except:
                pass
        except:
            pass
        try:
            indx = lst.index('Uyruğu:')
            playerObj.nationality = lst[indx+1]
        except:
            pass
        try:
            indx = lst.index('Mevki:')
            playerObj.position = lst[indx+1]
        except:
            pass
        try:
            indx = lst.index('Ayak:')
            playerObj.leg = lst[indx+1]
        except:
            pass
        try:
            indx = lst.index('Oyuncu danışmanı:')
            playerObj.counselar = lst[indx+1]
            try:
                playerObj.counselar = playerObj.counselar.replace("'"," ")
            except:
                pass
        except:
            pass
        try:
            indx = lst.index('Güncel kulüp:')
            playerObj.currentClub = lst[indx+1]
            try:
                playerObj.currentClub = playerObj.currentClub.replace("'"," ")
            except:
                pass
        except:
            pass
        try:
            indx = lst.index('Takıma katılma tarihi:')
            playerObj.joinedDate = self.date_converter_4_mysql(lst[indx+1])
        except:
            indx = lst.index('Takıma katılma tarihi::')
            playerObj.joinedDate = self.date_converter_4_mysql(lst[indx+1])
        else:
            pass
        try:
            indx = lst.index('Sözleşme bitiş tarihi:')  ######
            playerObj.endOfContDate = self.date_converter_4_mysql(lst[indx+1])
        except:
            indx = lst.index('Sözleşme bitiş tarihi::')  ######
            playerObj.endOfContDate = self.date_converter_4_mysql(lst[indx+1])
        else:
            pass
        playerObj.href = link
        try:
            # Transfer Table Parsing
            transfer_table = soupOfPlayerProfile.find_all('div', attrs={'class':'responsive-table'})[0]
            rows = transfer_table.find('tbody').find_all('tr', attrs={'class':'zeile-transfer'})
            for row in rows:
                season = row.findAll('td', attrs={'class':'zentriert hide-for-small'})[0].get_text(strip=True).strip()
                date = self.date_converter_4_mysql(row.findAll('td', attrs={'class':'zentriert hide-for-small'})[1].get_text(strip=True).strip())
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
                playerObj.pastOfTransfers.append((season,date,old_team,new_team))
        except:
            playerObj.pastOfTransfers.append(('0/0','0000-00-00','unknow','unknow'))
        
        #playerObj.toString()
        #playerObj.dataTypestoString()
       

    def set_player_infos_DE(self, playerObj, soupOfPlayerProfile, link):
        player_data_table = soupOfPlayerProfile.find('table', attrs={'class':'auflistung'})
        lst = [text for text in player_data_table.stripped_strings]
        #print(lst, '\n')
        try:
            playerObj.full_name = soupOfPlayerProfile.find_all('h1',attrs={'itemprop':'name'})[0].get_text(strip=True)
            try:
                playerObj.full_name = playerObj.full_name.replace("'"," ")
            except:
                pass
        except:
            pass
        try:
            indx = lst.index('Geburtsdatum:')
            playerObj.bday = self.date_converter_4_mysql(lst[indx+1])
        except:
            pass
        try:
            indx = lst.index('Geburtsort:')
            playerObj.bplace = lst[indx+1]
        except:
            pass
        try:
            indx = lst.index('Alter:')
            playerObj.age = lst[indx+1]
        except:
            pass
        try:
            indx = lst.index('Größe:')
            s = lst[indx+1].replace(",", ".")
            try:
                playerObj.hight = s.split('\xa0')[0]
            except:
                pass
            
        except:
            pass
        try:
            indx = lst.index('Nationalität:')
            playerObj.nationality = lst[indx+1]
        except:
            pass
        try:
            indx = lst.index('Position:')
            playerObj.position = lst[indx+1]
        except:
            pass
        try:
            indx = lst.index('Fuß:')
            playerObj.leg = lst[indx+1]
        except:
            pass
        try:
            indx = lst.index('Spielerberater:')
            playerObj.counselar = lst[indx+1]
            try:
                playerObj.counselar = playerObj.counselar.replace("'"," ")
            except:
                pass
        except:
            pass
        try:
            indx = lst.index('Aktueller Verein:')
            playerObj.currentClub = lst[indx+1]
            try:
                playerObj.currentClub = playerObj.currentClub.replace("'"," ")
            except:
                pass
        except:
            pass

        try:
            indx = lst.index('Im Team seit:')
            playerObj.joinedDate = self.date_converter_4_mysql(lst[indx+1])
        except:
            pass
        try:
            indx = lst.index('Im Team seit::')
            playerObj.joinedDate = self.date_converter_4_mysql(lst[indx+1])
        except:
            pass

        try:
            indx = lst.index('Vertrag bis:')  ######
            playerObj.endOfContDate = self.date_converter_4_mysql(lst[indx+1])
        except:
            pass
        try:
            indx = lst.index('Vertrag bis::')  ######
            playerObj.endOfContDate = self.date_converter_4_mysql(lst[indx+1])
        except:
            pass
        playerObj.href = link
        
        # Transfer Table Parsing
        try:
            transfer_table = soupOfPlayerProfile.find_all('div', attrs={'class':'responsive-table'})[0]
            rows = transfer_table.find('tbody').find_all('tr', attrs={'class':'zeile-transfer'})
            for row in rows:
                season = row.findAll('td', attrs={'class':'zentriert hide-for-small'})[0].get_text(strip=True).strip()
                date = self.date_converter_4_mysql(row.findAll('td', attrs={'class':'zentriert hide-for-small'})[1].get_text(strip=True).strip())
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
                playerObj.pastOfTransfers.append((season,date,old_team,new_team))
        except:
            playerObj.pastOfTransfers.append(('0/0','0000-00-00','unknow','unknow'))
        #playerObj.toString()
        #playerObj.dataTypestoString()


    def date_converter_4_mysql(self,date):
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
        
    def send_request(self, url):
        s = requests.Session()
        s.cookies.set_policy(BlockAll())

        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'} 
        
        try:
            time.sleep(2)
            return s.get(url, headers=headers)
        except Exception:
            print ('ERROR:(SEND REQUEST METHOD)')
            return self.send_request(url)


class BlockAll(cookiejar.CookiePolicy):
    return_ok = set_ok = domain_return_ok = path_return_ok = lambda self, *args, **kwargs: False
    netscape = True
    rfc2965 = hide_cookie2 = False