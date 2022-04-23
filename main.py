import logging

import aiogram.contrib.fsm_storage.redis
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage


import backend
import keyboards.keyboards as kb
import defs
from config import BOT_TOKEN

API_TOKEN = BOT_TOKEN

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
storage = aiogram.contrib.fsm_storage.redis.RedisStorage2()

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)



@dp.message_handler(state='*', commands=['start'])
async def start_command(message: types.Message):
    user = message.from_user.id
    state = dp.current_state(user=user)
    await state.finish()

    if backend.users.find_one({'_id': user}):
        await message.answer('Рад снова видеть!', reply_markup=kb.main_keyboard)
    else:
        await backend.add_user(user)
        await message.answer('Добро пожаловать!', reply_markup=kb.main_keyboard)
#
#     #
#     # if not backend.cursor.execute(f'SELECT user_id FROM users WHERE user_id="{user}";').fetchall():
#     #     backend.cursor.execute(f'INSERT INTO users(user_id) VALUES ({user});')
#     #     backend.sqlite_connection.commit()
#     #     await message.answer(f'Добрый день, {user}', reply_markup=kb.main_keyboard)
#     # else:
#     #     await message.answer(f'Вы уже в бд', reply_markup=kb.main_keyboard)
#
#
@dp.message_handler()
async def echo(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    if message.text == '🚻 Мой профиль':
        await defs.my_profile(message)

    if message.text == '⚙ Настройки':
        await state.set_state('in settings')
        await defs.my_settings(message)

    if message.text == '🔎 Начать поиск':
        await defs.lets_search(message)


@dp.message_handler(state='in settings')
async def in_settings(message: types.Message):
    state = dp.current_state(chat=message.chat.id)
    if message.text == '🔙 Назад':
        await state.finish()
        await message.answer('Главное меню', reply_markup=kb.main_keyboard)

    if message.text == '🆔 Изменить UID':
        await state.set_state('change uid')
        await defs.change_uid(message)

    if message.text == '🧍Изменить nickname':
        await state.set_state('change nickname')
        await defs.change_nickname(message)

    if message.text == '✍ Изменить сообщение':
        await state.set_state('change message')
        await defs.change_message(message)

    if message.text == '🆔 Изменить AR&WL':
        await state.set_state('change ar n wl')
        await defs.change_ar_wl(message)


@dp.message_handler(state='change uid')
async def chg_uid(message: types.Message):
    state = dp.current_state(chat=message.chat.id)
    if message.text.isdigit():
        backend.users.find_one_and_update({'_id': message.chat.id}, {'$set': {'uid': message.text}})
        await state.set_state('in settings')
        await message.answer('UID успешно изменен!', reply_markup=kb.setting_keyboard)


@dp.message_handler(state='change nickname')
async def chg_name(message: types.Message):
    state = dp.current_state(chat=message.chat.id)
    if message.text:
        backend.users.find_one_and_update({'_id': message.chat.id}, {'$set': {'nickname': message.text}})
        # backend.cursor.execute(f'UPDATE users SET nickname = "{message.text}" WHERE user_id = {message.chat.id};')
        # backend.sqlite_connection.commit()
        await state.set_state('in settings')
        await message.answer('Nickname успешно изменен!', reply_markup=kb.setting_keyboard)


@dp.message_handler(state='change message')
async def chg_msg(message: types.Message):
    state = dp.current_state(chat=message.chat.id)
    if message.text:
        backend.users.find_one_and_update({'_id': message.chat.id}, {'$set': {'message': message.text}}, upsert=True)
        #
        # backend.cursor.execute(f'UPDATE users SET message = "{message.text}" WHERE user_id = {message.chat.id};')
        # backend.sqlite_connection.commit()
        await state.set_state('in settings')
        await message.answer('Сообщение успешно изменено!', reply_markup=kb.setting_keyboard)

@dp.message_handler(state='change ar n wl')
async def chg_msg(message: types.Message):
    state = dp.current_state(chat=message.chat.id)

    ar, wl = message.text.split()

    if ar.isdigit() and wl.isdigit():
        backend.users.find_one_and_update({'_id': message.chat.id}, {'$set': {'adventure_rank': ar, 'world_level': wl}}, upsert=True)
        #
        # backend.cursor.execute(f'UPDATE users SET message = "{message.text}" WHERE user_id = {message.chat.id};')
        # backend.sqlite_connection.commit()
        await state.set_state('in settings')
        await message.answer('AR и WL успешно изменен!', reply_markup=kb.setting_keyboard)


@dp.callback_query_handler(lambda c: c.data == 'button_need_help')
async def button_need_help(query: types.InlineQuery):
    await backend.add_user_queue(query.from_user.id)
    await bot.send_message(query.from_user.id, 'Вы добавлены!')



@dp.callback_query_handler(lambda c: c.data == 'button_want_help')
async def button_need_help(query: types.InlineQuery):
 #   data = [backend.users.find_one({'_id': 207756013}) for i in backend.cache.keys('*')].sort(key=lambda x: x['likes'])
    await bot.send_message(query.from_user.id, 'Идет поиск!')

    await bot.send_message(query.from_user.id, backend.get_player_by_queue(0), reply_markup=kb.players_inline_kb)


@dp.callback_query_handler(lambda c: c.data.startswith("button_prev"))
async def prev_page(call: types.CallbackQuery):
    data_id = int(call.data.split(":")[1])

    markup = types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton("Назад", callback_data=f"button_prev:{data_id-1}"),
        types.InlineKeyboardButton("Вперед", callback_data=f"button_next:{data_id+1}"),
    )
    await call.message.edit_text(backend.get_player_by_queue(data_id), reply_markup=markup)


@dp.callback_query_handler(lambda c: c.data.startswith("button_next"))
async def next_page(call: types.CallbackQuery):
    data_id = int(call.data.split(":")[1])

    markup = types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton("Назад", callback_data=f"button_prev:{data_id-1}"),
        types.InlineKeyboardButton("Вперед", callback_data=f"button_next:{data_id+1}"),
    )
    await call.message.edit_text(backend.get_player_by_queue(data_id), reply_markup=markup)



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)