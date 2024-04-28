from dotenv import load_dotenv
import os


DOTENV_PATH='.env'     

load_dotenv(dotenv_path=DOTENV_PATH)
BOT_TOKEN = str(os.getenv('BOT_TOKEN'))
ADMIN= str(os.getenv('ADMINS'))
API_DOMAIN_NAME=str(os.getenv('API_DOMAIN_NAME'))