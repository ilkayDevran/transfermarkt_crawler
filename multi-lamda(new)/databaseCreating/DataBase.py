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

    def createTables(self):
        
        with self.connection.cursor() as cur:

            # test_Clubs
            cur.execute("""CREATE TABLE IF NOT EXISTS `innodb`.`test_Clubs` (`club_id` INT(11) NOT NULL AUTO_INCREMENT,`name` VARCHAR(45) CHARACTER SET 'utf8' COLLATE 'utf8_turkish_ci' NOT NULL,`num_of_player` INT(11) NOT NULL,`avg_age` FLOAT NOT NULL,`num_of_legioner` INT(11) NOT NULL,`market_value` VARCHAR(45) CHARACTER SET 'utf8' COLLATE 'utf8_turkish_ci' NOT NULL, PRIMARY KEY (`club_id`)) ENGINE = InnoDB DEFAULT CHARACTER SET = utf8mb4 COLLATE = utf8mb4_turkish_ci """)
            #test leagues
            cur.execute("""CREATE TABLE IF NOT EXISTS `innodb`.`test_leagues` (`league_id` INT(11) NOT NULL AUTO_INCREMENT, `name` VARCHAR(45) CHARACTER SET 'latin5' NOT NULL, `country` VARCHAR(45) CHARACTER SET 'latin5' NOT NULL, `type` VARCHAR(45) CHARACTER SET 'latin5' NOT NULL, `total_value` VARCHAR(45) CHARACTER SET 'latin5' NOT NULL, PRIMARY KEY (`league_id`)) ENGINE = InnoDB AUTO_INCREMENT = 2 DEFAULT CHARACTER SET = utf8mb4 COLLATE = utf8mb4_turkish_ci""")
            #test club has test leagues
            cur.execute("""CREATE TABLE IF NOT EXISTS `innodb`.`test_Clubs_has_test_leagues` (`club_ID` INT(11) NOT NULL, `league_ID` INT(11) NOT NULL, PRIMARY KEY (`club_ID`, `league_ID`), INDEX `fk_test_Clubs_has_test_leagues_test_leagues1_idx` (`league_ID` ASC), INDEX `fk_test_Clubs_has_test_leagues_test_Clubs1_idx` (`club_ID` ASC), CONSTRAINT `fk_test_Clubs_has_test_leagues_test_Clubs1` FOREIGN KEY (`club_ID`) REFERENCES `innodb`.`test_Clubs` (`club_id`) ON DELETE NO ACTION ON UPDATE NO ACTION, CONSTRAINT `fk_test_Clubs_has_test_leagues_test_leagues1` FOREIGN KEY (`league_ID`) REFERENCES `innodb`.`test_leagues` (`league_id`) ON DELETE NO ACTION ON UPDATE NO ACTION) ENGINE = InnoDB DEFAULT CHARACTER SET = utf8mb4 COLLATE = utf8mb4_turkish_ci""")
            # test players
            cur.execute("""CREATE TABLE IF NOT EXISTS `innodb`.`test_Players` (`player_id` INT(11) NOT NULL AUTO_INCREMENT, `full_name` VARCHAR(50) CHARACTER SET 'utf8' COLLATE 'utf8_turkish_ci' NOT NULL, `bday` DATE NOT NULL, `bplace` VARCHAR(45) CHARACTER SET 'utf8' COLLATE 'utf8_turkish_ci' NOT NULL, `hight` FLOAT NOT NULL, `age` INT(11) NOT NULL, `nationality` VARCHAR(45) CHARACTER SET 'utf8' COLLATE 'utf8_turkish_ci' NOT NULL, `position` VARCHAR(45) CHARACTER SET 'utf8' COLLATE 'utf8_turkish_ci' NOT NULL, `leg` VARCHAR(45) CHARACTER SET 'utf8' COLLATE 'utf8_turkish_ci' NOT NULL, `counselar` VARCHAR(50) CHARACTER SET 'utf8' COLLATE 'utf8_turkish_ci' NOT NULL, `joined_date` DATE NOT NULL, `end_of_cont_date` VARCHAR(45) CHARACTER SET 'utf8' COLLATE 'utf8_turkish_ci' NOT NULL, `club_ID` INT(11) NOT NULL, PRIMARY KEY (`player_id`), INDEX `fk_test_Players_test_Clubs1_idx` (`club_ID` ASC), CONSTRAINT `fk_test_Players_test_Clubs1` FOREIGN KEY (`club_ID`) REFERENCES `innodb`.`test_Clubs` (`club_id`) ON DELETE NO ACTION ON UPDATE NO ACTION) ENGINE = InnoDB DEFAULT CHARACTER SET = utf8mb4 COLLATE = utf8mb4_turkish_ci""")
            #test_transfer
            cur.execute("""CREATE TABLE IF NOT EXISTS `innodb`.`test_Transfers` (`transfer_id` INT(11) NOT NULL AUTO_INCREMENT, `season` VARCHAR(20) CHARACTER SET 'utf8' COLLATE 'utf8_turkish_ci' NOT NULL, `date` DATE NOT NULL, `old_team` VARCHAR(45) CHARACTER SET 'utf8' COLLATE 'utf8_turkish_ci' NOT NULL, `new_team` VARCHAR(45) CHARACTER SET 'utf8' COLLATE 'utf8_turkish_ci' NOT NULL, `player_ID` INT(11) NOT NULL, PRIMARY KEY (`transfer_id`), INDEX `fk_test_Transfers_test_Players1_idx` (`player_ID` ASC), CONSTRAINT `fk_test_Transfers_test_Players1` FOREIGN KEY (`player_ID`) REFERENCES `innodb`.`test_Players` (`player_id`) ON DELETE NO ACTION ON UPDATE NO ACTION) ENGINE = InnoDB DEFAULT CHARACTER SET = utf8mb4 COLLATE = utf8mb4_turkish_ci """)
            self.connection.commit()
            cur.close()

    def dropTables(self):
         with self.connection.cursor() as cur:
            cur.execute("""DROP TABLE `innodb`.`test_Clubs_has_test_leagues`;""")
            cur.execute("""DROP TABLE `innodb`.`test_leagues`;""")
            cur.execute("""DROP TABLE `innodb`.`test_Transfers`;""")
            cur.execute("""DROP TABLE `innodb`.`test_Players`;""")
            cur.execute("""DROP TABLE `innodb`.`test_Clubs`;""")

            self.connection.commit()
            cur.close()



        

