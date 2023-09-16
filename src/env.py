import os

from dotenv import load_dotenv

load_dotenv()
PORT = int(os.getenv('PORT'))
DB_CONNECTION = os.getenv('DB_CONNECTION')
DB_PROCES = os.getenv('DB_PROCES')
