from pathlib import Path

from core.utils import EnvParser, SecretStr


BASE_DIR = Path(__file__).parent.parent.parent

ENGINE = EnvParser.get('AI_ENGINE', str)
MODEL = EnvParser.get('AI_MODEL', str)
API_KEY = EnvParser.get('AI_API_KEY', SecretStr)
TEMP = EnvParser.get('AI_TEMP', float)

DEBUG = EnvParser.get('DEBUG', bool, False)
