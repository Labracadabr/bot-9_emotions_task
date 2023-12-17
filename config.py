from dataclasses import dataclass
from environs import Env

@dataclass
class Config:
    BOT_TOKEN: str = None   # телеграм бот
    TOLOKA: str = None      # толока


# загрузить конфиг из переменных окружения
env = Env()
env.read_env()
config = Config(BOT_TOKEN=env('BOT_TOKEN'),
                TOLOKA=env('TOLOKA'),
                )
