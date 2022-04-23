from aiogram.types import KeyboardButton, InlineKeyboardButton

back_button = KeyboardButton('🔙 Назад')

profile_button = KeyboardButton('🚻 Мой профиль')
settings_button = KeyboardButton('⚙ Настройки')
search_button = KeyboardButton('🔎 Начать поиск')

change_uid = KeyboardButton('🆔 Изменить UID')
change_nickname = KeyboardButton('🧍Изменить nickname')
change_ar_wl = KeyboardButton('🆔 Изменить AR&WL')
change_message = KeyboardButton('✍ Изменить сообщение')


inline_need_help = InlineKeyboardButton('Мне нужна помощь!', callback_data='button_need_help')
inline_want_help = InlineKeyboardButton('Хочу помочь!', callback_data='button_want_help')

inline_next = InlineKeyboardButton('Вперед', callback_data='button_next:1')
inline_prev = InlineKeyboardButton('Назад', callback_data='button_prev:-1')

