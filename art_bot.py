import asyncio
import random
import urllib.parse
import os
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import FSInputFile

# --- КОНФИГУРАЦИЯ ---
# Твой токен уже здесь
TOKEN = "8761763990:AAG9Fs3Umzzqt9zMwSZAbqIaGt8ZTMeMu8M"
# ---------------------

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "👁 **Добро пожаловать в визуализатор реальности.**\n\n"
        "Я превращаю твои мысли в реальные файлы. Пиши `/gen` и свой запрос.\n"
        "👉 *Пример: /gen неоновый волк в лесу*"
    )

@dp.message(Command("gen"))
async def generate_img(message: types.Message):
    # Извлекаем текст запроса
    prompt = message.text.replace("/gen", "").strip()
    
    if not prompt:
        await message.reply("💀 Ты пришел в храм искусства и молчишь? Напиши запрос после команды!")
        return

    # Пафосные фразы для ожидания
    loading_phrases = [
        "🌌 Считываю твои мысли из ноосферы...",
        "🎨 Смешиваю пиксели твоих безумных идей...",
        "⚡️ Нейроны перегружены, но я справлюсь...",
        "🔮 Визуализирую то, что другие боятся даже представить...",
        "🏗 Строю твой личный мир из цифровой пыли..."
    ]
    
    wait_msg = await message.answer(random.choice(loading_phrases))

    # ПРАВИЛЬНОЕ кодирование ссылки (с /prompt/ и корректными слэшами)
    safe_prompt = urllib.parse.quote(prompt)
    seed = random.randint(1, 99999999)
    image_url = f"https://pollinations.ai{safe_prompt}?seed={seed}&width=1024&height=1024&model=flux&nologo=true"
    
    # Имя временного файла для этого пользователя
    file_path = f"art_{message.from_user.id}.jpg"

    try:
        # Скачиваем картинку (ждем до 60 секунд)
        response = requests.get(image_url, timeout=60)
        
        if response.status_code == 200:
            # Сохраняем картинку на диск хостинга
            with open(file_path, "wb") as f:
                f.write(response.content)
            
            # Отправляем именно ФАЙЛ в чат
            photo = FSInputFile(file_path)
            
            success_phrases = [
                f"🖼 **Смирись с величием этого образа:** \n_{prompt}_",
                f"👑 **Твой шедевр готов, смертный:** \n_{prompt}_",
                f"✨ **Я вытащил это из бездны специально для тебя:** \n_{prompt}_",
                f"🔥 **Наслаждайся плодом нашего союза:** \n_{prompt}_"
            ]
            
            await message.answer_photo(
                photo=photo, 
                caption=random.choice(success_phrases),
                parse_mode="Markdown"
            )
            await wait_msg.delete()
            
            # Удаляем временный файл, чтобы не занимать место
            if os.path.exists(file_path):
                os.remove(file_path)
        else:
            await wait_msg.edit_text(f"💥 Ошибка нейросети: Код {response.status_code}. Попробуй позже.")
            
    except Exception as e:
        # Выводим ошибку, если она случится
        await wait_msg.edit_text(f"💥 Ошибка в матрице: {str(e)[:100]}")
        print(f"DEBUG ERROR: {e}")
        # На всякий случай пытаемся удалить файл при ошибке
        if os.path.exists(file_path):
            os.remove(file_path)

async def main():
    print("🚀 Бот-художник в режиме ФАЙЛОВ запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот выключен.")
