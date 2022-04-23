from aiogram import Bot, Dispatcher, executor, types
from backend import users
from keyboards import keyboards as kb
from keyboards import buttons as bt
from backend import cache
from main import bot

async def my_profile(message: types.Message):
    info = users.find_one({'_id': message.chat.id})
    await message.answer(info)

async def my_settings(message: types.Message):
    text = 'Выберите, что хотите изменить'
    await message.answer(text, reply_markup=kb.setting_keyboard)

async def change_uid(message: types.Message):
    text = 'Напишите свой UID:'
    await message.answer(text, reply_markup=kb.rm_kb)


async def change_nickname(message: types.Message):
    text = 'Напишите свой Nick:'
    await message.answer(text, reply_markup=kb.rm_kb)


async def change_message(message: types.Message):
    text = 'Напишите новое сообщение:'
    await message.answer(text, reply_markup=kb.rm_kb)

async def change_ar_wl(message: types.Message):
    text = 'Напишите AR и WL через пробел:'
    await message.answer(text, reply_markup=kb.rm_kb)

async def lets_search(message: types.Message):
    needs = cache.keys("*")
    text = f'Игроки, которым нужна помощь: {len(needs)}\nВажно: перед началом использования поиска' \
    'полностью заполнить профиль'

    await message.answer(text, reply_markup=kb.search_inline_kb)

async def start_search(query: types.InlineQuery, data: list):
    await bot.send_message(query.from_user.id, 'Нажмите Следующий', reply_markup=kb.players_inline_kb)


# async def playes_who_need_help(data: dict):
#
#     new_kb = types.InlineKeyboardMarkup().add(bt.inline_prev).add(types.InlineKeyboardButton('')).add(bt.inline_p)
