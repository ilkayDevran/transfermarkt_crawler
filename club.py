class Club:
    def __init__(self):
        self.name = ''
        self.numOfPlayers = ''
        self.avrAge = ''
        self.numOflegionaries = ''
        self.marketValue = ''
        self.href = ''
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