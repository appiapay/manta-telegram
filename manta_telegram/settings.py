import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.environ['BOT_TOKEN']
MANTA_APP_ID = os.environ['MANTA_APP_ID']
MANTA_APP_TOKEN = os.environ['MANTA_APP_TOKEN']
MANTA_HOST = os.environ['MANTA_HOST']
LOGO = os.getenv('LOGO', 'appia-circle.png')
