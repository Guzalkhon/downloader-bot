import os

from aiogram import Router, Bot
from aiogram.types import Message, FSInputFile
from aiogram.filters import CommandStart
from yt_dlp import YoutubeDL


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


@router.message(CommandStart())
async def start_command(message: Message):
    await message.reply("Hello! Send me the link of the video")


@router.message()
async def handle_url(message: Message, bot: Bot):
    url = message.text.strip()
    if "youtube.com" in url or "youtu.be" in url or "instagram.com" in url or "tiktok.com" in url:
        await message.reply("Downloading...")
        try:
            path = await download_video(url)
            video = FSInputFile(path)
            await bot.send_video(message.chat.id, video=video)
            os.remove(path)
        except Exception as e:
            await message.reply(f"Error: {e}")
    else:
        await message.reply("Link is not defined. Check it and try again")
