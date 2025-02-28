from dataclasses import dataclass
from environs import Env


@dataclass
class DatabaseConfig:
    url_db: str


@dataclass
class DatabaseRedisConfig:
    host: str
    port: int
    db: int


@dataclass
class TgBot:
    token: str  # Токен для доступа к телеграм-боту
    developer_id: int  # id администратора


@dataclass
class Config:
    tg_bot: TgBot
    db: DatabaseConfig
    db_redis: DatabaseRedisConfig


# Создаем экземпляр класса Env
env: Env = Env()

# Добавляем в переменные окружения данные, прочитанные из файла .env
env.read_env()

# Создаем экземпляр класса Config и наполняем его данными из переменных окружения
config = Config(
    tg_bot=TgBot(token=env("BOT_TOKEN"), developer_id=env("DEVELOPER_ID")),
    db=DatabaseConfig(url_db=env("DB_URL")),
    db_redis=DatabaseRedisConfig(
        host=env("REDIS_HOST"), port=env("REDIS_PORT"), db=env("REDIS_DB")
    ),
)
