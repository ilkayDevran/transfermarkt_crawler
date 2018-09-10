import pymysql

class DataBase:
    def __init__(self, db):
        self.choosen_DB = db
        ########
        
    def insert_league_data(self, leagueObj):  
        with self.connection.cursor() as cur:
            cur.execute("""insert Into innodb.leagues (name, country, type, total_value) values( "%s", "%s" , "%s", "%s"); """ % (leagueObj.name, leagueObj.country, leagueObj.type, leagueObj.total_value))
            for club in leagueObj.clubs:
                cur.execute("""insert Into innodb.Clubs (name, num_of_player, avg_age, num_of_legioner, market_value) values( "%s", %s , %s, %s, "%s"); """ % (club.name, club.numOfPlayer, club.avrAge, club.numOflegioneries, club.marketValue))
                cur.execute("""insert Into innodb.Clubs_has_leagues (club_ID, league_ID) values( (SELECT club_id FROM innodb.Clubs WHERE name = "%s"), (SELECT league_id FROM innodb.leagues WHERE name = "%s")); """ % (club.name, leagueObj.name))
                for player in club.players:
                    cur.execute("""insert Into innodb.Players (full_name, bday, bplace, hight, age, nationality, position,
                                leg, counselar, joined_date, end_of_cont_date, club_ID) values( "%s", "%s" , "%s", %s, %s, "%s", "%s", "%s", "%s", "%s","%s", (SELECT club_id FROM innodb.Clubs WHERE name = "%s")); """ % (
                                player.full_name, player.bday, player.bplace, player.hight, player.age, player.nationality, player.position,
                                player.leg, player.counselar, player.joinedDate, player.endOfContDate, club.name))

                    for transfer in player.pastOfTransfers:
                        (season, date, old_team, new_team) = transfer
                        cur.execute("""insert Into innodb.Transfers (season, date, old_team, new_team, player_ID) values("%s", "%s", "%s", "%s", (SELECT player_id FROM innodb.Players WHERE name = "%s")); """ % (season, date, old_team, new_team, player.name))
            self.connection.commit()
            cur.close()

    def insert_player_data(self, full_name, bday, bplace, age, hight, nationality, position,
        leg,counselar, club_name, joinDate, endOfContDate):
        if self.choosen_DB == 'innodb':
                with self.connection.cursor() as cur:
                    cur.execute("""insert Into eksiSozlukCrawler.News (full_name, bday, bplace, hight, age, nationality, position,
                                leg,counselar, joinDate, endOfContDate, club_ID) values( "%s", "%s" , "%s", %s, %s, "%s", "%s", "%s", "%s", "%s","%s", (SELECT club_id FROM Clubs WHERE name = "%s")); """ % (
                                full_name, bday, bplace, hight, age, nationality, position,
                                leg, counselar, joinDate, endOfContDate, club_name))
                    
                    self.connection.commit()
                    cur.close()


    def insert_test_data(self,name, date, hight, leg):
        if self.choosen_DB == 'innodb':
                with self.connection.cursor() as cur:
                    cur.execute("""insert Into innodb.Test (name, date, hight) values( "%s", "%s" , %s); """ % (name, date, hight))
                    cur.execute("""insert Into innodb.Test_2 (leg, test_ID) values( "%s", LAST_INSERT_ID()); """ % (leg))
                    self.connection.commit()
                    cur.close()
    

"""
db = DataBase('innodb')

db.insert_test_data('ilkay', '1996-07-11', 1.8, 'sağ ayak')
"""