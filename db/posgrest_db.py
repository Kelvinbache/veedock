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
                    AND table_name IN ('test', 'user', 'login', 'user_test')
                    );
                    """)
         
         response = cur.fetchone()

         if response[0]:
            print("table is exit")                 
         
         else:
            cur.execute("""
                create table IF NOT EXISTS users (
                id bigint primary key generated always as identity,
                nombre text not null,
                apellido text not null,
                telefono text not null,
                correo text not null unique
            );""")   

            cur.execute("""
                create table IF NOT EXISTS login (
                id bigint primary key generated always as identity,
                usuario_id bigint not null,
                password text not null,
                foreign key (usuario_id) references usuario (id)
            );""")

            cur.execute("""
                CREATE TABLE IF NOT EXISTS test (
                id serial PRIMARY KEY,
                num integer,
                data text)
            """) 
             
            cur.execute("""
                create table IF NOT EXISTS users_test (
                usuario_id bigint not null,
                test_id bigint not null,
                primary key (usuario_id, test_id),
                foreign key (usuario_id) references usuario (id),
                foreign key (test_id) references test (id)
            );""") 

        conn.commit()
   
   
     except Exception as error:
        print (f"this error:{error}")         


