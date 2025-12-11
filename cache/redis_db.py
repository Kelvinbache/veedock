import redis
from config import redis_config

class Db_redis(object):
     def __init__(self, config:dict,decode_responses):
         self.host = config.get("HOST_REDIS")
         self.port = config.get("PORT_REDIS")
         self.username = config.get("USERNAMME")
         self.password = config.get("PASSWORD_REDIS")
         self.decode_responses = decode_responses
         
     def connect(self):
        try:     
           r_client = redis.Redis(
           host= self.host,
           port=self.port,
           decode_responses= self.decode_responses,
           username=self.username,
           password=self.password   
         )
           
           r_client.ping()
           return r_client
              
        except Exception as error:
            print(f"this error: {error}")   




db = Db_redis(**redis_config)

r = db.connect()

if r:
   try:
     success = r.set('foo', 'bar')
     result = r.get('foo')
     print(result)

   except Exception as err:
       print(f" this is : {err}")    


