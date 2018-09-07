class League:
    def  __init__(self):
        self.name = ''
        self.type = ''
        self.country = ''
        self.totalValue = ''
        self.href = ''
        self.clubs = []
    
    def toString(self):
        print ('Name:', self.name)
        print ('Degree:', self.type)
        print ('Country:', self.country)
        print ('Total Value:', self.totalValue)
        print ('href:', self.href)
        for club in self.clubs:
            print (club.name)
        print('\n')