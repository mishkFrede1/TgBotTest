<<<<<<< HEAD
import asyncio
import os
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from aiogram.client.bot import DefaultBotProperties

from handlers import base_commands

async def main():
    load_dotenv()
    bot = Bot(os.getenv('TOKEN'), default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher(bot=bot)
    
    dp.include_routers(
        base_commands.router
    )

    await dp.start_polling(bot)

if __name__ == "__main__":
=======
import asyncio
import os
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from aiogram.client.bot import DefaultBotProperties

from handlers import base_commands

async def main():
    load_dotenv()
    bot = Bot(os.getenv('TOKEN'), default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher(bot=bot)
    
    dp.include_routers(
        base_commands.router
    )

    await dp.start_polling(bot)

if __name__ == "__main__":
>>>>>>> c016f4ad8c783d9d2330cedc356225695b705df7
    asyncio.run(main())