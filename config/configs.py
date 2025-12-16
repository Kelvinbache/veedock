from dotenv import load_dotenv
import os

load_dotenv()

config_postgres = {
"dbname": os.getenv("DBNAME"),
"user":os.getenv("USER_POSTGRES"),
"password":os.getenv("PASSWORD_POSTGRES"),
"host":os.getenv("HOST_POSTGRES"),
"port":os.getenv("PORT_POSTGRES")
}

redis_config = {
"host":os.getenv("HOST_REDIS"),
"port":os.getenv("PORT_REDIS"),
"username": os.getenv("USERNAMME"),
"password":os.getenv("PASSWORD_REDIS")
}
