from pathlib import Path
from dotenv import load_dotenv

from core.utils.env_parser import EnvParser


BASE_DIR = Path(__file__).parent.parent

load_dotenv(BASE_DIR / '.env')

VK_TOKEN = EnvParser.get_env('VK_TOKEN', str)
DEBUG = EnvParser.get_env('DEBUG', bool, False)

print(DEBUG)
