import pymysql

class DataBase:
    def __init__(self, db):
        self.choosen_DB = db
        self.connection = pymysql.connect(
                host = 'tmcrawler.cb5e4o6zarmq.eu-central-1.rds.amazonaws.com'
                , user = 'tmroot'
                , passwd = 'transfermarktPassw0rd'
                , db = self.choosen_DB,
                charset='utf8')
        
    def insert_league_data(self, leagueObj):  
        with self.connection.cursor() as cur:
           
            for club in leagueObj.clubs:
                #print('\n\nCLUB\n',"""insert Into innodb.Clubs (name, num_of_player, avg_age, num_of_legioner, market_value) values( '%s', %s , %s, %s, '%s'); """ % (club.name, club.numOfPlayers, club.avrAge, club.numOflegionaries, club.marketValue))
                cur.execute("""insert Into innodb.Clubs (name, num_of_player, avg_age, num_of_legioner, market_value) values( '%s', %s , %s, %s, '%s'); """ % (club.name, club.numOfPlayers, club.avrAge, club.numOflegionaries, club.marketValue))
                print('[INFO]: CLUB INSERT OKAY')
                
                #print("""insert Into innodb.Clubs_has_leagues (club_ID, league_ID) values( (SELECT club_id FROM innodb.Clubs WHERE name = '%s'), (SELECT league_id FROM innodb.leagues WHERE name = '%s')); """ % (club.name, leagueObj.name))
                cur.execute("""insert Into innodb.Clubs_has_leagues (club_ID, league_ID) values( (SELECT club_id FROM innodb.Clubs WHERE name = '%s'), (SELECT league_id FROM innodb.leagues WHERE name = '%s')); """ % (club.name, leagueObj.name))
                print('[INFO]: CLUB_has_leagues INSERT OKAY')
                
                for player in club.players:
                    #print('\n\nPLAYER\n',"""insert Into innodb.Players (full_name, bday, bplace, hight, age, nationality, position,leg, counselar, joined_date, end_of_cont_date, club_ID) values( '%s', '%s' , '%s', %s, %s, '%s', '%s', '%s', '%s', '%s','%s', (SELECT club_id FROM innodb.Clubs WHERE name = '%s'));"""% (
                                #player.full_name, player.bday, player.bplace, player.hight, player.age, player.nationality, player.position,
                                #player.leg, player.counselar, player.joinedDate, player.endOfContDate, club.name))
                    cur.execute("""insert Into innodb.Players (full_name, bday, bplace, hight, age, nationality, position,leg, counselar, joined_date, end_of_cont_date, club_ID) values( '%s', '%s' , '%s', %s, %s, '%s', '%s', '%s', '%s', '%s','%s', (SELECT club_id FROM innodb.Clubs WHERE name = '%s')); """ % (
                                player.full_name, player.bday, player.bplace, player.hight, player.age, player.nationality, player.position,
                                player.leg, player.counselar, player.joinedDate, player.endOfContDate, club.name))
                    print('[INFO]: PLAYER INSERT OKAY')
                    
                    for transfer in player.pastOfTransfers:
                        (season, date, old_team, new_team) = transfer
                        #print("""insert Into innodb.Transfers (season, date, old_team, new_team, player_ID) values('%s', '%s', '%s', '%s', (SELECT player_id FROM innodb.Players WHERE full_name = '%s')); """ % (season, date, old_team, new_team, player.full_name))
                        cur.execute("""insert Into innodb.Transfers (season, date, old_team, new_team, player_ID) values('%s', '%s', '%s', '%s', (SELECT player_id FROM innodb.Players WHERE full_name = '%s' AND bday = '%s')); """ % (season, date, old_team, new_team, player.full_name, player.bday))
                        print('[INFO]: TRANSFER INSERT OKAY')
            
            self.connection.commit()
            print('[INFO]: COMMIT')
            cur.close()

    def insert_club(self, club_obj, league_id):
        name, numOfPlayers, avrAge, numOflegionaries, marketValue = club_obj
        
        with self.connection.cursor() as cur:
            cur.execute("""insert Into innodb.test_Clubs (name, num_of_player, avg_age, num_of_legioner, market_value) values( '%s', %s , %s, %s, '%s'); """ % (name, numOfPlayers, avrAge, numOflegionaries, marketValue))
            print('[INFO]: CLUB INSERT OKAY')

            cur.execute("""insert Into innodb.Clubs_has_leagues (club_ID, league_ID) values( (SELECT club_id FROM innodb.test_Clubs WHERE name = '%s'), '%s')); """ % (name, league_id))
            print('[INFO]: CLUB_has_leagues INSERT OKAY')

            cur.execute("""select club_id from test_Clubs where name = '%s' """ % (name))
            club_id = '-1'
            result = cur.fetchall()
            for row in result:
                club_id = row[0]
            #print('club_id:',club_id)
            cur.close()
            
        return club_id