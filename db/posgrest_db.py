import psycopg
from config import config_postgress

class Db_prostgres(object):
   def __init__(self):
       self.conn = None

   def db(self):   

       try:
         self.conn = psycopg.connect(**config_postgress)
        
         return self.conn

       except Exception as error:
            print(f"this is erro:{error}")   
    
    # error 


db_connection = Db_prostgres()
conn = db_connection.db()

if conn:
     try:
        with conn.cursor() as cur:
         cur.execute("""
                CREATE TABLE test (
                id serial PRIMARY KEY,
                num integer,
                data text)
            """) 
   
         cur.execute( "INSERT INTO test (num, data) VALUES (%s, %s)",(100, "abc'def"))

         cur.execute("SELECT * FROM test")
       
         print(cur.fetchone())    
   
     except Exception as error:
        print (f"this error:{error}")         


