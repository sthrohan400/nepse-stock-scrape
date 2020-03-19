import redis

redis_host = "localhost"
redis_port = 6379
redis_password = ""


class RedisCacheLibrary:
    __instance = None

    def __init__(self):
        if RedisCacheLibrary.__instance != None:
            raise Exception("Class is Singleton.")
        else:
            self.redis = redis.StrictRedis(host = redis_host, port = redis_port, password= redis_password)
            RedisCacheLibrary.__instance = self

    @staticmethod
    def getInstance(self):
        if RedisCacheLibrary.__instance == None:
            RedisCacheLibrary()
        return RedisCacheLibrary.__instance

    def set(self, key, value):
        return self.redis.set(key, value)

    def get(self, key):
        return self.get(key)