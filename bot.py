import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor

logging.basicConfig(level=logging.INFO)

API_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

if not API_TOKEN:
    raise RuntimeError("BOT_TOKEN is not set")
if ADMIN_ID == 0:
    raise RuntimeError("ADMIN_ID is not set")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

menu = ReplyKeyboardMarkup(resize_keyboard=True)
menu.add(KeyboardButton("📅 Записаться"))
menu.add(KeyboardButton("💈 Цены"))
menu.add(KeyboardButton("📍 Адрес"))

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer("Добро пожаловать в Barbershop 💈", reply_markup=menu)

@dp.message_handler(lambda m: m.text == "💈 Цены")
async def prices(message: types.Message):
    await message.answer("Стрижка — 100 000 сум\nБорода — 50 000 сум")

@dp.message_handler(lambda m: m.text == "📍 Адрес")
async def addr(message: types.Message):
    await message.answer("г. Ташкент, ул. Пример 10")

@dp.message_handler(lambda m: m.text == "📅 Записаться")
async def book(message: types.Message):
    await message.answer("Напиши: Имя + время\nПример: Aziz 18:00")

@dp.message_handler()
async def any_text(message: types.Message):
    username = message.from_user.username
    who = f"@{username}" if username else f"id:{message.from_user.id}"
    await bot.send_message(ADMIN_ID, f"💈 Новая запись:\n{message.text}\nОт: {who}")
    await message.answer("✅ Запись принята! Мы свяжемся с вами.")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
