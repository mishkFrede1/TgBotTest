from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📋 Инфа")],
        [KeyboardButton(text="📑 Мануалы"), KeyboardButton(text="👩 Паки с девушками")],
        [KeyboardButton(text="💳 Карты"), KeyboardButton(text="❓ Помощь")],
    ], resize_keyboard=True
)

start = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📋 Инфа")],
        [KeyboardButton(text="📝 Отправить заявку")],
        [KeyboardButton(text="❓ Помощь")]
    ], resize_keyboard=True
)

want_work = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="✅ Я намерен работать"), KeyboardButton(text="❌ Я зашел поинтересоваться")]
    ], resize_keyboard=True
)

gender_choice = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="👨 Мужской"), KeyboardButton(text="👩 Женский")]
    ], resize_keyboard=True
)