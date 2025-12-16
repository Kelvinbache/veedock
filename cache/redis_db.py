import redis
import sys 
import os 

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

if project_root not in sys.path:
    sys.path.append(project_root)

from config.configs import redis_config

class Db_redis(object):
     def __init__(self, config:dict, decode_responses):
         self.host = config.get("host")
         self.port = config.get("port")
         self.username = config.get("username")
         self.password = config.get("password")
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

db = Db_redis(redis_config, True)

r = db.connect()


