import os

from dotenv import load_dotenv

load_dotenv(override=True)

bind = '127.0.0.1:8000'
workers = 2
user = os.environ.get('USER')
timeout = 120
