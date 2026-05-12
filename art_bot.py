import asyncio
import random
import urllib.parse
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import BufferedInputFile

# --- КОНФИГУРАЦИЯ ---
TOKEN = "8761763990:AAG9Fs3Umzzqt9zMwSZAbqIaGt8ZTMeMu8M"
# ---------------------

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("gen"))
async def generate_img(message: types.Message):
    prompt = message.text.replace("/gen", "").strip()
    
    if not prompt:
        await message.reply("💀 Пустой запрос? Я не читаю мысли, пиши текстом!")
        return

    wait_msg = await message.answer("🔮 Матрица генерирует ваш код... Ждите.")

    # Кодируем текст
    safe_prompt = urllib.parse.quote(prompt)
    # Используем альтернативный стабильный источник (Unsplash/Source) для теста или Pollinations без параметров
    image_url = f"https://pollinations.ai{safe_prompt}?nologo=true&private=true"

    try:
        # Увеличиваем таймаут и добавляем User-Agent (чтобы сайт не блокировал бота)
        headers = {"User-Agent": "Mozilla/5.0"}
        timeout = aiohttp.ClientTimeout(total=40)
        
        async with aiohttp.ClientSession(timeout=timeout, headers=headers) as session:
            async with session.get(image_url) as response:
                if response.status == 200:
                    image_data = await response.read()
                    
                    if len(image_data) < 100: # Если пришел пустой файл
                        raise Exception("Получен пустой файл от нейросети")

                    photo = BufferedInputFile(image_data, filename="art.jpg")
                    await message.answer_photo(
                        photo=photo, 
                        caption=f"🔥 **Материя сформирована:** \n_{prompt}_",
                        parse_mode="Markdown"
                    )
                    await wait_msg.delete()
                else:
                    await wait_msg.edit_text(f"🛑 Нейросеть выдала ошибку {response.status}. Попробуй позже.")
                    
    except Exception as e:
        # ТУТ ВАЖНО: Бот напишет причину ошибки
        await wait_msg.edit_text(f"💥 Ошибка: {str(e)}")
        print(f"DEBUG: {e}")

async def main():
    print("🚀 Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
