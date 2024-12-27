from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Video', callback_data='mp4')],
    [InlineKeyboardButton(text='Audio', callback_data='mp3')]
])