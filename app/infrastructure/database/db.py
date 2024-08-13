from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.infrastructure.models.base import Base
from app.tgbot.config import load_config, Config

config: Config = load_config()

engine = create_engine("sqlite:///" + config.db.name)
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)
