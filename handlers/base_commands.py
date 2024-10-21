from aiogram import Router, F
from aiogram.filters import Command 
from aiogram.types import Message

from data import texts, keyboards

router = Router()

@router.message(Command("start"))
async def start(message: Message):
    await message.answer(texts.start.format(name=message.from_user.first_name), reply_markup=keyboards.start)

@router.message(F.text == "info")
async def info_button(message: Message):
    await message.answer(texts.info)

@router.message(F.text == "cards")
async def cards_button(message: Message):
    await message.answer(texts.cards)

@router.message(F.text == "help")
async def help_button(message: Message):
    await message.answer(texts.help)