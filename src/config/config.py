import os
import dotenv

dotenv.load_dotenv()
TOKEN = os.getenv("TOKEN")
BASE_URL = os.getenv("BASEURL")
GROUP_ID = os.getenv("GROUP_ID")