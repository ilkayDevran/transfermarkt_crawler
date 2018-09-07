# -*- coding: UTF-8 -*-

import requests
from bs4 import BeautifulSoup
import json
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
                for league_link in table.findAll('a'):
                    currentLeague = LEAG()
                    if league_link.get('title') != 'Müsabaka forumuna git':
                        count+=1
                        if count % 2 != 0:
                            count=1
                            # Go Into Current League Page and Initialize a League Object
                            leaguePage_r = self.send_request(self.URL + league_link.get('href'))
                            
                            soupOfLeaguePage = BeautifulSoup(leaguePage_r.text, 'html.parser')
                            profileHeader = soupOfLeaguePage.find_all('table', attrs = {'class' : 'profilheader'})
                            # set league info
                            self.set_league_infos(currentLeague,soupOfLeaguePage,profileHeader,league_link.get('href'))
                            self.leagues.append(currentLeague)   
                
                print (len(self.leagues))
                input()             

    def set_league_infos(self,currentLeague,soupOfLeaguePage,profileHeader,link):
        try:
            lst = [text for text in profileHeader[0].stripped_strings]
            currentLeague.name = soupOfLeaguePage.find('h1', attrs = {'class' : 'spielername-profil'}).get_text().strip()
            currentLeague.type = lst[lst.index('Lig seviyesi:')+1]
        except:
            pass
        try:
            currentLeague.name = soupOfLeaguePage.find('h1', attrs = {'itemprop' : 'name'}).get_text().strip()
        except:
            pass
        try:
            currentLeague.country = lst[lst.index('Lig seviyesi:')+2]
        except:
            pass
        try:
            currentLeague.totalValue = soupOfLeaguePage.find('div', attrs = {'class' : 'marktwert'}).get_text().strip().split(':', 1)[-1]
        except:
            pass
        currentLeague.href = link  #league href
        
        #currentLeague.toString()
      

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