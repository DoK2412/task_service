import os
DataBase = {
        "user": "fp_db_admin",
        "password": "fp_db_admin",
        "host": "postgres",
        "port": 5432,
        "db_name": "db_task"
        }

RedisData = {
        "user": "admin",
        "password": "root",
        }

SECRET_KEY = ",jci?bCw0qyt-4sAe76P!gIn.NLruBol"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
REFRESH_TOKEN_EXPIRE_DAYS = 7

IGNOR_PATH = ["/auth/register", "/auth/login", "/auth/refresh", "/docs", "/openapi.json"]

LOG_FOLDER = '/log/'
LOG_FILE_NAME = os.path.dirname(os.path.realpath(__file__)) + f'{LOG_FOLDER}task_logger.log'