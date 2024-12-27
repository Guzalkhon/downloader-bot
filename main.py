from aiogram import Bot, Dispatcher

import asyncio
import os

from app.config import *
from app.handlers import router

bot = Bot(token=TOKEN)
dp = Dispatcher()


async def main():
    dp.include_router(router)
    if not os.path.exists('./downloads'):
        os.mkdir('./downloads')
    print("Started")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Finished')