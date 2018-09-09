class Player:
    def  __init__(self):
        self.full_name = ''
        self.bday = ''
        self.bplace = ''
        self.age  = ''
        self.hight = ''
        self.nationality  = ''
        self.position = ''
        self.leg = ''
        self.counselar = ''
        self.currentClub = ''
        self.joinedDate = ''
        self.endOfContDate = ''
        self.href = ''
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