class Player:
    def  __init__(self):
        self.full_name = 'unknown'
        self.bday = 'unknown'
        self.bplace = 'unknown'
        self.age  = 'unknown'
        self.hight = 0.0
        self.nationality  = 'unknown'
        self.position = 'unknown'
        self.leg = 'unknown'
        self.counselar = 'unknown'
        self.currentClub = 'unknown'
        self.joinedDate = 'unknown'
        self.endOfContDate = 'unknown'
        self.href = 'unknown'
        self.pastOfTransfers = []

    def toString(self):
        print ('\nFull Name: ', self.full_name)
        print ('Birth Day: ', self.bday)
        print ('Birth Place: ', self.bplace)
        print ('Age: ', self.age)
        print ('Hight: ', self.hight)
        print ('Nationality: ', self.nationality)
        print ('Position: ', self.position)
        print ('Leg: ', self.leg)
        print ('Counselar: ', self.counselar)
        print ('Current Club: ', self.currentClub)
        print ('Joined Date: ', self.joinedDate)
        print ('End Of Cont Date: ', self.endOfContDate)
        print ('href: ', self.href)
        print('\nTransfer History')
        for t in self.pastOfTransfers:
            print (t)
        print('\n')

    def dataTypestoString(self):
        print ('\nFull Name: ', type(self.full_name))
        print ('Birth Day: ', type(self.bday))
        print ('Birth Place: ', type(self.bplace))
        print ('Age: ', type(self.age))
        print ('Hight: ', type(self.hight))
        print ('Nationality: ', type(self.nationality))
        print ('Position: ', type(self.position))
        print ('Leg: ', type(self.leg))
        print ('Counselar: ', type(self.counselar))
        print ('Current Club: ', type(self.currentClub))
        print ('Joined Date: ', type(self.joinedDate))
        print ('End Of Cont Date: ', type(self.endOfContDate))
        print ('href: ', type(self.href))
