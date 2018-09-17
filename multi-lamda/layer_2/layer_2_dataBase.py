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

    def insert_league(self, league_obj):
        name, country, league_type, totalValue = league_obj
        
        with self.connection.cursor() as cur:
            # !!!!!! REPLACE innodb.test_leagues with innodb.leagues !!!!!!
            cur.execute("""insert Into innodb.test_leagues (name, country, type, total_value) values( '%s', '%s', '%s', '%s'); """ % (name, country, league_type, totalValue))
            print('[INFO]: LEAGUE INSERT OKAY')
            self.connection.commit()
            print('[INFO]: COMMIT')
            cur.execute("""select league_id from test_leagues where name = '%s' """ % (name))
            league_id = '-1'
            result = cur.fetchall()
            for row in result:
                league_id = row[0]
            #print('id:',league_id)

            cur.close()
            
        return league_id

        

