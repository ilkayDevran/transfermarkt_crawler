class Club:
    def __init__(self):
        self.name = 'unknown'
        self.numOfPlayers = 0
        self.avrAge = 0.0
        self.numOflegionaries = 0
        self.marketValue = 'unknown'
        self.href = 'unknown'
        self.players = []
    
    def toString(self):
        print ('Name:', self.name)
        print ('# Players:', self.numOfPlayers)
        print ('Avg. Age:', self.avrAge)
        print ('Total Market Value:', self.marketValue)
        print ('href:', self.href)
        for player in self.players:
            print (player.name)
        print('\n')

    def dataTypestoString(self):
        print ('Name:', type(self.name))
        print ('# Players:', type(self.numOfPlayers))
        print ('Avg. Age:', type(self.avrAge))
        print ('Total Market Value:', type(self.marketValue))
        print ('href: ', type(self.href))