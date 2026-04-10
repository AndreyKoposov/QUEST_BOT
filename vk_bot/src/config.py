from pathlib import Path

from core.utils import EnvParser, SecretStr


BASE_DIR = Path(__file__).parent.parent.parent

VK_TOKEN = EnvParser.get('VK_TOKEN', SecretStr)

M_USER = EnvParser.get('MONGO_INITDB_ROOT_USERNAME', str)
M_PSWRD = EnvParser.get('MONGO_INITDB_ROOT_PASSWORD', SecretStr)
M_DB = EnvParser.get('MONGO_INITDB_DATABASE', str)

R_PSWRD = EnvParser.get('R_PSWRD', SecretStr)

DEBUG = EnvParser.get('DEBUG', bool, False)
