import redis

redis_host = "localhost"
redis_port = 6379
redis_password = ""


class RedisCacheLibrary:
    __instance = None

    def __init__(self,config):
        if RedisCacheLibrary.__instance != None:
            raise Exception("Class is Singleton.")
        else:
            self.redis = redis.StrictRedis(host=config.get('redis').host, port=config.get('redis').port,
                                           password=config.get('redis').password)
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
        if type(value) is list:
            pipeline = self.redis.pipeline()
            for item in value:
                pipeline.lpush(key, item)
            pipeline.execute()
