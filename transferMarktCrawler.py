# -*- coding: UTF-8 -*-

import requests
from bs4 import BeautifulSoup
from league import League as LEAG
from club import Club as CLB
from player import Player as PLYR


class TransferMarktCrawler:
    def  __init__(self):
        self.URL = 'https://www.transfermarkt.com.tr'
        self.country_href_list = ['/wettbewerbe/national/wettbewerbe/174']
        self.leagues = []

    def start(self):
        
        # Country Leagues -> Teams of a League -> Players in Team -> Player Info
        for country_href in self.country_href_list: # Country Leagues Page
            r = self.send_request(self.URL + country_href)
            # Parse the response
            soup = BeautifulSoup(r.text, 'html.parser')
            tables = soup.find_all('div', attrs = {'class' : 'responsive-table'})
            
            count = 1
            for table in tables:
                #print('1')
                for league_link in table.findAll('a'):
                    #print('2')
                    currentLeague = LEAG()
                    if league_link.get('title') != 'Müsabaka forumuna git':
                        #print('1 if')
                        count+=1
                        if count % 2 != 0:
                            #print('2 if')
                            count=1
                            # Go Into Current LEAGUE Page and Initialize a League Object
                            leaguePage_r = self.send_request(self.URL + league_link.get('href'))
                            
                            soupOfLeaguePage = BeautifulSoup(leaguePage_r.text, 'html.parser')
                            # set league info
                            self.set_league_infos(currentLeague,soupOfLeaguePage, league_link.get('href'))
                            self.leagues.append(currentLeague)

                            # parsing team table in current league page to get links of teams
                            table_of_teams = soupOfLeaguePage.find('div', attrs={'id':'yw1', 'class':'grid-view'}) # reaching to the team table in league page 
                            tbody = table_of_teams.find('tbody')  # tbody
                            club_column = tbody.findAll('td', attrs={'class':'hauptlink no-border-links hide-for-small hide-for-pad'}) # (Kulup) column to reach the link
                            for clb in club_column:
                                #print('3')
                                currentTeam = CLB()
                                # Go Into Current TEAM Page and Initialize a Team Object
                                teamPage_r = self.send_request(self.URL + clb.find('a').get('href'))
                                soupOfTeamPage = BeautifulSoup(teamPage_r.text, 'html.parser')
                                self.set_club_infos(currentTeam, soupOfTeamPage, clb.find('a').get('href'))
                                
                                # parsing player table in current team page to get links of player profiles
                                table_of_players = soupOfTeamPage.find('div', attrs={'id':'yw1', 'class':'grid-view'})
                                tbody2 = table_of_players.find('tbody')  # tbody
                                rows = tbody2.findAll('td', attrs = {'class':'posrela'})
                                count = 1 # count is used to prevent repeating same links
                                for row in rows:
                                    for player in row.findAll('a', attrs = {'class':'spielprofil_tooltip'}):
                                        if count%2 == 0:
                                            count=1
                                            continue

                                        count+=1
                                        currentPlayer = PLYR()
                                        # Go Into Current PLAYER Page and Initialize a Player Object
                                        playerProfile_r = self.send_request(self.URL + player.get('href'))
                                        soupOfPlayerProfile = BeautifulSoup(playerProfile_r.text, 'html.parser')
                                        self.set_player_infos(currentPlayer, soupOfPlayerProfile, player.get('href'))
                                        
                                        input()
                        
                        
                        
                        else:
                            continue
                    else:
                        continue
                                

                    input() 
                input() 

    def set_league_infos(self, leagueObj, soupOfLeaguePage,link):
        profileHeader = soupOfLeaguePage.find_all('table', attrs = {'class' : 'profilheader'})
        try:
            lst = [text for text in profileHeader[0].stripped_strings]
            leagueObj.name = soupOfLeaguePage.find('h1', attrs = {'class' : 'spielername-profil'}).get_text().strip()
            leagueObj.type = lst[lst.index('Lig seviyesi:')+1]
        except:
            pass
        try:
            leagueObj.name = soupOfLeaguePage.find('h1', attrs = {'itemprop' : 'name'}).get_text().strip()
        except:
            pass
        try:
            leagueObj.country = lst[lst.index('Lig seviyesi:')+2]
        except:
            pass
        try:
            leagueObj.totalValue = soupOfLeaguePage.find('div', attrs = {'class' : 'marktwert'}).get_text().strip().split(':', 1)[-1]
        except:
            pass
        leagueObj.href = link  #league href
        #leagueObj.toString()
      
    def set_club_infos(self, teamObj, soupOfTeamPage, link):
        try:
            teamObj.name = soupOfTeamPage.find('div', attrs={'class':'dataName'}).find('h1').get_text().strip()
        except:
            pass
            
        dataContent = soupOfTeamPage.find('div', attrs={'class':'dataContent'})
        dataDaten = dataContent.find_all('div', attrs={'class':'dataDaten'})[0]
        rows = dataDaten.findAll('p')
        try:
            teamObj.numOfPlayers = rows[0].find('span', attrs={'class':'dataValue'}).get_text().strip()
        except:
            pass
        try:
            teamObj.avrAge = rows[1].find('span', attrs={'class':'dataValue'}).get_text().strip()
        except:
            pass
        try:
           teamObj.numOflegionaries = rows[2].find('span', attrs={'class':'dataValue'}).get_text().strip()
        except:
            pass
        
        try:
            strng = soupOfTeamPage.find('div', attrs = {'class' : 'dataMarktwert'}).get_text().strip()
            teamObj.marketValue= strng[:strng.index('€')+1]

        except:
            pass

        teamObj.href = link
        #teamObj.toString()

    def set_player_infos(self, playerObj, soupOfPlayerProfile, link):
        player_data_table = soupOfPlayerProfile.find('table', attrs={'class':'auflistung'})
        lst = [text for text in player_data_table.stripped_strings]
        try:
            playerObj.full_name = soupOfPlayerProfile.find_all('h1',attrs={'itemprop':'name'})[0].get_text()
        except:
            pass
        try:
            indx = lst.index('Doğum tarihi:')
            playerObj.bday = lst[indx+1]
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
        except:
            pass
        try:
            indx = lst.index('Güncel kulüp:')
            playerObj.currentClub = lst[indx+1]
        except:
            pass
        try:
            indx = lst.index('Takıma katılma tarihi:')
            playerObj.joinedDate = lst[indx+1]
        except:
            pass
        try:
            indx = lst.index('Sözleşme bitiş tarihi:')  ######
            playerObj.currentClub = lst[indx+1]
        except:
            pass
        playerObj.href = link
        playerObj.toString()

    def send_request(self, url):
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


def main():
    myCrawler = TransferMarktCrawler()
    myCrawler.start()

if __name__ == '__main__':
    main()