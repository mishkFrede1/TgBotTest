#!/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
import os
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from aiogram.client.bot import DefaultBotProperties

from handlers import base_commands, applications

async def main():
    load_dotenv()
    bot = Bot(os.getenv('TOKEN'), default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher(bot=bot)
    
    dp.include_routers(
        base_commands.router,
        applications.router
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
