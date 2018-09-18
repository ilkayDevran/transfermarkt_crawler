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

    def insert_player(self, player_obj, club_id):
        (full_name, bday, bplace, age, hight, nationality, position, 
            leg, counselar, joinedDate, endOfContDate, pastOfTransfers) = player_obj

        with self.connection.cursor() as cur:
            cur.execute("""insert Into innodb.test_Players (full_name, bday, bplace, hight, age, nationality, position,leg, counselar, joined_date, end_of_cont_date, club_ID) values( '%s', '%s' , '%s', %s, %s, '%s', '%s', '%s', '%s', '%s','%s', %s); """ % (
                                full_name, bday, bplace, hight, age, nationality, position,
                                leg, counselar, joinedDate, endOfContDate, club_id))
            print('[INFO]: PLAYER INSERT OKAY')
            
            for transfer in pastOfTransfers:
                (season, date, old_team, new_team) = transfer
                cur.execute("""insert Into innodb.test_Transfers (season, date, old_team, new_team, player_ID) values('%s', '%s', '%s', '%s', (SELECT player_id FROM innodb.test_Players WHERE full_name = '%s' AND bday = '%s')); """ % (season, date, old_team, new_team, full_name, bday))
                print('[INFO]: TRANSFER INSERT OKAY')
            
            self.connection.commit()
            print('[INFO]: COMMIT')
            cur.close()