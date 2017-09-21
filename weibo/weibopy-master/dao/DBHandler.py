import MySQLdb


class DBHandler:
    connection = None
    HOST = 'localhost'
    USERNAME = 'root'
    PASSWORD = 'keepon'
    DB = 'weibo'

    @staticmethod
    def connect():
        DBHandler.connection = MySQLdb.connect(
            DBHandler.HOST,
            DBHandler.USERNAME,
            DBHandler.PASSWORD,
            DBHandler.DB)
        DBHandler.connection.set_character_set('utf8')

    @staticmethod
    def getConn():
        return DBHandler.connection

    @staticmethod
    def commit():
        DBHandler.connection.commit()

    @staticmethod
    def rollback():
        DBHandler.connection.rollback()

    @staticmethod
    def closeConn():
        DBHandler.connection.close()
