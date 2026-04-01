from pathlib import Path
from dotenv import load_dotenv

from core.utils.env_parser import EnvParser


BASE_DIR = Path(__file__).parent.parent

load_dotenv(BASE_DIR / '.env')

VK_TOKEN = EnvParser.get_env('VK_TOKEN', str)

MONGO_USER = EnvParser.get_env('MONGO_USER', str)
MONGO_PSWRD = EnvParser.get_env('MONGO_PSWRD', str)
MONGO_DB = EnvParser.get_env('MONGO_DB', str)
MONGO_HOST = EnvParser.get_env('MONGO_HOST', str)
MONGO_PORT = EnvParser.get_env('MONGO_PORT', int)

DEBUG = EnvParser.get_env('DEBUG', bool, False)
