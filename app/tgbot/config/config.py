import os
from dataclasses import dataclass

import dotenv


@dataclass
class DatabaseConfig:
    name: str


@dataclass
class TgBot:
    token: str
    admin_id: int


@dataclass
class Config:
    bot: TgBot
    db: DatabaseConfig


def load_config() -> Config:
    dotenv.load_dotenv()

    return Config(
        bot=TgBot(
            token=str(os.getenv("BOT_TOKEN")),
            admin_id=int(str(os.getenv("ADMIN_ID"))),
        ),
        db=DatabaseConfig(
            name=str(os.getenv("DATABASE")),
        ),
    )
