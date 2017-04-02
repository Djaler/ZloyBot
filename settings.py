import os

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

TOKEN = os.environ["TOKEN"]
ADMIN_ID = int(os.environ["ADMIN_ID"])
CHAT_ID = int(os.environ["CHAT_ID"])

ENV = os.environ.get("ENV", "prod")

PORT = int(os.environ.get('PORT', '5000'))
URL = os.environ.get("URL")
DATABASE_URL = os.environ["DATABASE_URL"]
