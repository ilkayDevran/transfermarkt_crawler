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
        
    def insert_club(self, club_obj, league_id):
        name, numOfPlayers, avrAge, numOflegionaries, marketValue = club_obj
        print(name, numOfPlayers, avrAge, numOflegionaries, marketValue)
        with self.connection.cursor() as cur:
            cur.execute("""insert Into innodb.test_Clubs (name, num_of_player, avg_age, num_of_legioner, market_value) values( '%s', %s , %s, %s, '%s'); """ % (name, numOfPlayers, avrAge, numOflegionaries, marketValue))
            print('[INFO]: CLUB INSERT OKAY')
            #print("""insert Into innodb.test_Clubs (name, num_of_player, avg_age, num_of_legioner, market_value) values( '%s', %s , %s, %s, '%s'); """ % (name, numOfPlayers, avrAge, numOflegionaries, marketValue))

            cur.execute("""insert Into innodb.test_Clubs_has_test_leagues (club_ID, league_ID) values( (SELECT club_id FROM innodb.test_Clubs WHERE name = '%s'), %s); """ % (name, league_id))
            print('[INFO]: CLUB_has_leagues INSERT OKAY')

            cur.execute("""select club_id from test_Clubs where name = '%s' """ % (name))
            club_id = '-1'
            result = cur.fetchall()
            for row in result:
                club_id = row[0]
            #print('club_id:',club_id)

            self.connection.commit()
            print('[INFO]: COMMIT')
            cur.close()
            
        return club_id