import os

from aiogram import Router, Bot
from aiogram.types import Message, FSInputFile, CallbackQuery
from aiogram.filters import CommandStart
from yt_dlp import YoutubeDL

from app.keyboards import keyboard


router = Router()


async def download_video(url: str, output_format="mp4"):
    output_filename = f"{url.split('/')[-1]}.{output_format}"
    options = {
        'format': 'best',
        'outtmpl': f"./downloads/{output_filename}"
    }
    with YoutubeDL(options) as ydl:
        ydl.download([url])
    
    path = f"./downloads/{output_filename}"
    path = path.replace('?', '#')
    
    return path



async def download_audio(url: str, output_format="mp3"):
    output_filename = f"{url.split('/')[-1]}.{output_format}"
    options = {
        'format': 'bestaudio/best',
        'outtmpl': f"./downloads/{output_filename}"
    }
    with YoutubeDL(options) as ydl:
        ydl.download([url])

    path = f"./downloads/{output_filename}"
    path = path.replace('?', '#')

    return path


@router.message(CommandStart())
async def start_command(message: Message):
    await message.reply("Hello! Send me the link of the video")


@router.message()
async def handle_url(message: Message):
    global url
    url = message.text.strip()

    if "youtube.com" in url or "youtu.be" in url or "instagram.com" in url or "tiktok.com" in url:
        await message.reply("Choose format:", reply_markup=keyboard)
    else:
        await message.reply("Link is not defined. Check it and try again")



@router.callback_query()
async def handle_format_selection(callback_query: CallbackQuery, bot:Bot):
    format_choice = callback_query.data

    await bot.answer_callback_query(callback_query.id)

    if format_choice == "mp3":
        try:
            path = await download_audio(url)
            audio = FSInputFile(path)
            await bot.send_audio(callback_query.from_user.id, audio=audio)
            os.remove(path)
        except Exception as e:
            await bot.send_message(callback_query.from_user.id, f"Error: {e}")

    elif format_choice == "mp4":
        try:
            path = await download_video(url)
            video = FSInputFile(path)
            await bot.send_video(callback_query.from_user.id, video=video)
            os.remove(path)
        except Exception as e:
            await bot.send_message(callback_query.from_user.id, f"Error: {e}")