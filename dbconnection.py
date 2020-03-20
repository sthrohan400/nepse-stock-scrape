import mysql.connector
class MysqlConnectionManager:
    __instance = None
    def __init__(self,config):
        if MysqlConnectionManager.__instance != None:
            raise Exception("Class is Singleton.")
        else:
            # config = config.get('mysql')
            try:
                self.connection = mysql.connector.connect(host=config.get('host'), user=config.get('username'),
                                           passwd=config.get('password'),database=config.get('database'))
            except mysql.connector.Error as e:
                print(e)
            MysqlConnectionManager.__instance = self

    @staticmethod
    def getInstance(config):
        if MysqlConnectionManager.__instance == None:
            MysqlConnectionManager(config)
        return MysqlConnectionManager.__instance
