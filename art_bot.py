import asyncio
import random
import urllib.parse
import os
import requests  # Библиотека для скачивания
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import FSInputFile

# --- КОНФИГУРАЦИЯ ---
TOKEN = "8761763990:AAG9Fs3Umzzqt9zMwSZAbqIaGt8ZTMeMu8M"
# ---------------------

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("gen"))
async def generate_img(message: types.Message):
    prompt = message.text.replace("/gen", "").strip()
    
    if not prompt:
        await message.reply("💀 Напиши запрос, художник!")
        return

    wait_msg = await message.answer("🔮 Материализую пиксели... Погоди немного.")

    # Готовим ссылку
    safe_prompt = urllib.parse.quote(prompt)
    seed = random.randint(1, 999999)
    image_url = f"https://pollinations.ai{safe_prompt}?seed={seed}&width=1024&height=1024&nologo=true"
    
    # Имя временного файла
    file_name = f"temp_art_{message.from_user.id}.jpg"

    try:
        # Скачиваем картинку через requests
        response = requests.get(image_url, timeout=60)
        
        if response.status_code == 200:
            # Сохраняем во временный файл
            with open(file_name, "wb") as f:
                f.write(response.content)
            
            # Отправляем файл из системы
            photo = FSInputFile(file_name)
            await message.answer_photo(
                photo=photo, 
                caption=f"🔥 **Твой шедевр готов:** \n_{prompt}_",
                parse_mode="Markdown"
            )
            await wait_msg.delete()
            
            # Удаляем файл после отправки
            os.remove(file_name)
        else:
            await wait_msg.edit_text("💥 Нейросеть недоступна. Попробуй позже.")
            
    except Exception as e:
        await wait_msg.edit_text(f"💥 Ошибка: {str(e)}")
        if os.path.exists(file_name):
            os.remove(file_name)

async def main():
    print("🚀 Бот запущен в режиме сохранения файлов!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
