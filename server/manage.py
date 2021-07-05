import os
from dotenv import load_dotenv

from filex import create_app

load_dotenv()
app = create_app(os.environ['APP_SETTINGS'])
