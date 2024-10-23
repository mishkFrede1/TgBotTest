from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📋 Инфа")],
        [KeyboardButton(text="📑 Мануалы"), KeyboardButton(text="👩 Паки с девушками")],
        [KeyboardButton(text="💳 Карты"), KeyboardButton(text="❓ Помощь")],
    ], resize_keyboard=True
)
# 🆘 📑 