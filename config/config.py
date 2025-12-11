from dotenv import load_dotenv
import os

load_dotenv()

config_postgres = {
"DBNAME": os.getenv("DBNAME"),
"USER_POSTGRES":os.getenv("USER_POSTGRES"),
"PASSWORD_POSTGRES":os.getenv("PASSWORD_POSTGRES"),
"HOST_POSTGRES":os.getenv("HOST_POSTGRES"),
"PORT_POSTGRES":os.getenv("PORT_POSTGRES")
}

redis_config = {
"HOST_REDIS":os.getenv("HOST_REDIS"),
"PORT_REDIS":os.getenv("PORT_REDIS"),
"USERNAMME": os.getenv("USERNAMME"),
"PASSWORD_REDIS":os.getenv("PASSWORD_REDIS")
}
