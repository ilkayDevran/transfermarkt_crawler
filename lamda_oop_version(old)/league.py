class League:
    def  __init__(self):
        self.name = 'unknown'
        self.type = 'unknown'
        self.country = 'unknown'
        self.totalValue = 'unknown'
        self.href = 'unknown'
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

    def dataTypestoString(self):
        print ('Name:', type(self.name))
        print ('Degree:', type(self.type))
        print ('Country:', type(self.country))
        print ('Total Value:', type(self.totalValue))
        print ('href: ', type(self.href))