import psycopg
import sys 
import os 

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

if project_root not in sys.path:
    sys.path.append(project_root)

from config.configs import config_postgres

class Db_prostgres(object):
   def __init__(self):
       self.conn = None

   def db(self):   

       try:
         self.conn = psycopg.connect(**config_postgres)
        
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
                    SELECT EXISTS ( 
                    SELECT 1 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = 'test'
                    );
                    """)
         response = cur.fetchone()

         if response[0]:
            print("table is exit")                 
         
         else:
            cur.execute("""
                CREATE TABLE test (
                id serial PRIMARY KEY,
                num integer,
                data text)
            """) 

        conn.commit()
   
   
     except Exception as error:
        print (f"this error:{error}")         


