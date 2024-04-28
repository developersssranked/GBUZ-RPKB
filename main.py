from aiogram import Bot, Dispatcher
import asyncio

from config import BOT_TOKEN
from bot.routers import start_router
from dotenv import load_dotenv


async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_routers(
            start_router.router,
        )


    await dp.start_polling(bot)

if __name__ == '__main__':
    load_dotenv()
    asyncio.run(main())

 