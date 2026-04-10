from pathlib import Path
from dotenv import load_dotenv

from core.utils import EnvParser


BASE_DIR = Path(__file__).parent.parent.parent

load_dotenv(BASE_DIR / 'llm/.env')

ENGINE = EnvParser.get('AI_ENGINE', str)
MODEL = EnvParser.get('AI_MODEL', str)
API_KEY = EnvParser.get('AI_API_KEY', str)
TEMP = EnvParser.get('AI_TEMP', float)

DEBUG = EnvParser.get('DEBUG', bool, False)
