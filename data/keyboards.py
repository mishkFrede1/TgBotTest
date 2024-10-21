from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="info")],
        [KeyboardButton(text="cards")],
        [KeyboardButton(text="help")],
    ], resize_keyboard=True
)