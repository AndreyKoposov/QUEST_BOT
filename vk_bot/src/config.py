from pathlib import Path
from dotenv import load_dotenv

from core.utils import EnvParser


BASE_DIR = Path(__file__).parent.parent.parent

load_dotenv(BASE_DIR / 'vk_bot/.env')
load_dotenv(BASE_DIR / 'mongo/.env')
load_dotenv(BASE_DIR / 'storage/.env')

VK_TOKEN = EnvParser.get('VK_TOKEN', str)

M_USER = EnvParser.get('MONGO_INITDB_ROOT_USERNAME', str)
M_PSWRD = EnvParser.get('MONGO_INITDB_ROOT_PASSWORD', str)
M_DB = EnvParser.get('MONGO_INITDB_DATABASE', str)

R_PSWRD = EnvParser.get('R_PSWRD', str)

DEBUG = EnvParser.get('DEBUG', bool, False)
