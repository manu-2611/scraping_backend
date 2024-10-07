import os
from dotenv import load_dotenv

load_dotenv()


REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = int(os.getenv("REDIS_PORT")) 
REDIS_DB = int(os.getenv("REDIS_DB")) 
TARGET_URL = "https://dentalstall.com/shop/"
RETRY_COUNT = 5
STATIC_TOKEN = os.getenv("STATIC_TOKEN") 
STORAGE_TYPE = "JSON"
FILE_PATH = os.getenv("JSON_FILE_PATH") 
HOST = os.getenv("HOST") 
SQL_PORT = os.getenv("SQL_PORT") 
DB_NAME = os.getenv("DB_NAME") 
USERNAME = os.getenv("USERNAME") 
PASSWORD = os.getenv("PASSWORD") 


