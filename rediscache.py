import redis

class RedisCacheLibrary:
    __instance = None

    def __init__(self,config):
        if RedisCacheLibrary.__instance != None:
            raise Exception("Class is Singleton.")
        else:
            config = config.get('redis')
            self.redis = redis.StrictRedis(host=config.get('host'), port=config.get('port'),
                                           password=config.get('password'))
            RedisCacheLibrary.__instance = self

    @staticmethod
    def getInstance(config):

        if RedisCacheLibrary.__instance == None:
            RedisCacheLibrary(config)
        return RedisCacheLibrary.__instance

    def set(self, key, value):
        return self.redis.set(key, value)

    def get(self, key):
        return self.get(key)
    # Redis add list data
    def push(self, key, value):
        self.redis.delete(key)
        if type(value) is list:
            pipeline = self.redis.pipeline()
            for item in value:
                pipeline.lpush(key, ','.join(item))
            pipeline.execute()
