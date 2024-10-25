from aiogram import Bot, Router, F
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext 
import dotenv
import os

from data import texts, keyboards
from db_manager import Manager
from utils.get_age_ending import getAgeEnding

router = Router()
manager = Manager()

class reg(StatesGroup):
    first_name = State()
    last_name = State()
    age = State()
    gender_female = State()
    want_work = State()

# Функция отправки заявки модератору
async def send_registration_request(user_id: int, moderator_id: int, bot, first_name: str, last_name: str, age: int, gender: str, username: str):
    buttons = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='✅ Принять', callback_data=f'app_accept_{user_id}_{moderator_id}_{username}'), InlineKeyboardButton(text='❌ Отклонить', callback_data=f'app_reject_{user_id}_{moderator_id}_{username}')]
    ])

    await bot.send_message(
        moderator_id,
        texts.application_info.format(username=username, user_id=user_id, first_name=first_name, last_name=last_name, age=f"{age} {getAgeEnding(age)}", gender=gender),
        reply_markup=buttons,

    )

# Обработка нажатия кнопки модерации
@router.callback_query(F.data.startswith("app_"))
async def process_moderation(callback_query: CallbackQuery, bot: Bot):
    splitted = callback_query.data.split("_")
    moderator_id = int(splitted[3])
    user_id = int(splitted[2])
    action = splitted[1]
    username = splitted[4]
    
    if action == 'accept':
        # Логика подтверждения регистрации пользователя
        manager.update_app_status(user_id, "accepted", True)
        await bot.send_message(moderator_id, f"✅ Заявка пользователя @{username} принята")
        await bot.send_message(user_id, "✅ <b>Ваша заявка принята.</b> Добро пожаловать в команду!", reply_markup=keyboards.menu)

    elif action == 'reject':
        # Логика отклонения и блокировки пользователя
        manager.update_app_status(user_id, "rejected", True)
        await bot.send_message(moderator_id, f"❌ Заявка пользователя @{username} отклонена")
        await bot.send_message(user_id, "❌ <b>Ваша заявка была отклонена.</b>")


    # Удаляем сообщение с кнопками у модератора
    await callback_query.message.delete()

async def send_application(user_id: int, bot: Bot, first_name: str, last_name: str, age: int, gender_female: bool, username: str):
    dotenv.load_dotenv()
    moderator_id = os.getenv('MODERATOR_ID')  # Укажите ID модератора (863400079), Head_ofAdministrations - 6603647116
    manager.new_user(user_id, first_name, last_name, age, gender_female)

    gender = "Мужской"
    if gender_female:
        gender = "Женский"

    await send_registration_request(user_id, moderator_id, bot, first_name, last_name, age, gender, username)

def isItFirstApp(user_id: int) -> bool:
    if manager.user_exists(user_id):
        return False
    else: return True

@router.message(F.text == "📝 Отправить заявку")
async def register(message: Message, state: FSMContext):
    if isItFirstApp(message.from_user.id):
        await state.set_state(reg.first_name)
        await message.answer("⚙️ <b>Как вас зовут?</b>")
    else:
        user = manager.get_user(message.from_user.id)
        if user[7]:
            await message.answer(texts.application_accepted_error)
        else:
            await message.answer(texts.application_repeat_error)

@router.message(reg.first_name)
async def register1(message: Message, state: FSMContext):
    await state.update_data(first_name=message.text)
    await state.set_state(reg.last_name)
    await message.answer("⚙️ <b>Что на счет фамилии?</b>")

@router.message(reg.last_name)
async def register2(message: Message, state: FSMContext):
    await state.update_data(last_name=message.text)
    await state.set_state(reg.age)
    await message.answer("⚙️ <b>Сколько вам полных лет?</b>")

@router.message(reg.age)
async def register3(message: Message, state: FSMContext):
    try:
        age = int(message.text)
        await state.update_data(age=age)
        await state.set_state(reg.gender_female)
        await message.answer("⚙️ <b>Выберите ваш пол:</b>", reply_markup=keyboards.gender_choice)
    except:
        await message.answer("❌ <b>Ошибка!</b> Вы должны ввести ваш возраст числами, не буквами или символами!")

@router.message(reg.gender_female)
async def register4(message: Message, state: FSMContext):
    if message.text != "👨 Мужской" and message.text != "👩 Женский":
        await message.answer("❌ <b>Ошибка!</b> Вы должны выбрать вариант из ниже приведенных!")
    else:
        gender_female = True
        if message.text == "👨 Мужской": gender_female = False
        await state.update_data(gender_female=gender_female)

        await state.set_state(reg.want_work)
        await message.answer("⚙️ <b>Готовы ли вы работать? Или же вы зашли сюда поинтересоваться?</b>", reply_markup=keyboards.want_work)

@router.message(reg.want_work)
async def register5(message: Message, bot: Bot, state: FSMContext):
    if message.text == "✅ Я намерен работать":
        await message.answer(texts.application_send, reply_markup=keyboards.start)
        
        data = await state.get_data()
        await send_application(message.from_user.id, bot, data["first_name"], data["last_name"], data["age"], data["gender_female"], message.from_user.username)
        await state.clear()

    elif message.text == "❌ Я зашел поинтересоваться":
        await message.answer("❌ <b>Вы нам не подходите!</b> ", reply_markup=keyboards.start)
        
        data = await state.get_data()
        manager.new_user(message.from_user.id, data["first_name"], data["last_name"], data["age"], data["gender_female"], rejected=True)
        await state.clear()

    else:
        await message.answer("❌ <b>Ошибка!</b> Вы должны выбрать вариант из ниже приведенных!")
    


@router.message(Command("reg"))
async def register_command(message: Message, state: FSMContext):
    if isItFirstApp(message.from_user.id):
        await state.set_state(reg.first_name)
        await message.answer("⚙️ <b>Как вас зовут?</b>")
    else:
        user = manager.get_user(message.from_user.id)
        if user[7]:
            await message.answer(texts.application_accepted_error)
        else:
            await message.answer(texts.application_repeat_error)
