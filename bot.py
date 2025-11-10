import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import FSInputFile
from osr2mp4 import Osr2mp4

API_TOKEN = "8598748891:AAF5RveKX5HuLlhY-dgMRLFcfTwtLSFEvCI"

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Папки для файлов
os.makedirs("replays", exist_ok=True)
os.makedirs("renders", exist_ok=True)

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Привет! Отправь мне .osr файл, и я сделаю тебе видео 🎥")

@dp.message()
async def handle_file(message: types.Message):
    if not message.document:
        await message.answer("Пришли .osr файл!")
        return

    file = message.document
    if not file.file_name.endswith(".osr"):
        await message.answer("Это не .osr файл 😅")
        return

    # Сохраняем файл
    path = f"replays/{file.file_name}"
    await bot.download(file, destination=path)
    await message.answer("Рендерю видео, подожди немного... ⏳")

    # Рендерим с помощью osr2mp4
    video_path = f"renders/{file.file_name[:-4]}.mp4"
    osr2mp4 = Osr2mp4(replay_path=path, output_path=video_path)
    osr2mp4.startall()

    # Отправляем видео обратно
    await message.answer_video(FSInputFile(video_path), caption="Готово ✅")

if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))
