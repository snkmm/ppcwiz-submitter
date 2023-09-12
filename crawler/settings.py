import os
from os.path import join, dirname

from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

AMAZON_LWA_CLIENT_ID = os.getenv('AMAZON_LWA_CLIENT_ID')
AMAZON_LWA_CLIENT_SECRET = os.getenv('AMAZON_LWA_CLIENT_SECRET')
REFRESH_TOKEN = os.getenv('REFRESH_TOKEN')

DATABASE_URL = os.getenv('DATABASE_URL')
LOG_LEVEL = os.getenv('LOG_LEVEL')
