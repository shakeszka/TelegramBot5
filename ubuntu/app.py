import asyncio

from aiogram import executor

from load_all import bot
from config import admin_id

async def on_shutdown(dp):
    await bot.close()


async def on_startup(dp):
    await bot.send_message(admin_id, "Я запущен!\n\n/start")


if __name__ == '__main__':
    from handlers import dp

    executor.start_polling(dp, on_shutdown=on_shutdown, on_startup=on_startup)