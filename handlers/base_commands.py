from aiogram import Router, F
from aiogram.filters import Command 
from aiogram.types import Message

from data import texts, keyboards

router = Router()

@router.message(Command("start"))
async def start(message: Message):
    await message.answer(texts.start.format(name=message.from_user.first_name), reply_markup=keyboards.start)

@router.message(F.text == "📋 Инфа")
async def info_button(message: Message):
    await message.answer(texts.info_text)

@router.message(F.text == "💳 Карты")
async def cards_button(message: Message):
    await message.answer(texts.cards, parse_mode="Markdown")

@router.message(F.text == "❓ Помощь")
async def help_button(message: Message):
    await message.answer(texts.help)

@router.message(F.text == "📑 Мануалы")
async def manuals_button(message: Message):
    await message.answer(texts.manuals, disable_web_page_preview=True) #images

@router.message(F.text == "👩 Паки с девушками")
async def packs_button(message: Message):
    await message.answer(texts.packs, disable_web_page_preview=True)