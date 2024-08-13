import asyncio
import logging
import os

import dotenv

from app.tgbot.tgbot import main

dotenv.load_dotenv()

logging.basicConfig(
    level=logging.getLevelName(str(os.getenv("LOG_LEVEL"))),
    format="[%(asctime)s] #%(levelname)-8s %(filename)s:%(lineno)d - %(name)s - %(message)s",
)

if __name__ == "__main__":
    asyncio.run(main())
