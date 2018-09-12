import requests
from bs4 import BeautifulSoup

class ProxyCollector:
    def __init__(self):
        self.url = 'https://free-proxy-list.net/'
        self.proxies = []
        self.get_proxies()
    
    def get_proxies(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')
       
        tbody = soup.find_all('tbody')[0]
        rows = tbody.find_all('tr')

        for row in rows[:25]:
            lst = [text for text in row.stripped_strings]
            if lst[6] == 'yes':
                #Grabbing IP and corresponding PORT
                self.proxies.append(":".join([lst[0], lst[1]]))

    def refresh_proxies(self):
        self.get_proxies()