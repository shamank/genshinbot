from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup
import keyboards.buttons as bt

rm_kb = ReplyKeyboardRemove()

main_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(bt.profile_button).add(bt.search_button).add(bt.settings_button)

setting_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(bt.change_uid, bt.change_nickname).add(bt.change_message, bt.change_ar_wl).add(bt.back_button)

search_inline_kb = InlineKeyboardMarkup().add(bt.inline_need_help, bt.inline_want_help)

players_inline_kb = InlineKeyboardMarkup().add(bt.inline_prev, bt.inline_next)