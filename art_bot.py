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
        await message.reply("💀 Напиши запрос, не трать моё время!")
        return

    wait_msg = await message.answer("🔮 Визуализирую твою фантазию... Погоди...")

    # Кодируем запрос
    safe_prompt = urllib.parse.quote(prompt)
    seed = random.randint(1, 999999999)
    image_url = f"https://pollinations.ai{safe_prompt}?seed={seed}&width=1024&height=1024&model=flux&enhance=true&nologo=true"

    try:
        # Скачиваем картинку в память бота
        async with aiohttp.ClientSession() as session:
            async with session.get(image_url) as response:
                if response.status == 200:
                    image_data = await response.read()
                    # Создаем файл из байтов
                    photo = BufferedInputFile(image_data, filename="result.jpg")
                    
                    await message.answer_photo(
                        photo=photo, 
                        caption=f"🔥 **Твой шедевр готов:** \n_{prompt}_",
                        parse_mode="Markdown"
                    )
                    await wait_msg.delete()
                else:
                    await wait_msg.edit_text("💥 Нейросеть занята. Попробуй через минуту.")
                    
    except Exception as e:
        await wait_msg.edit_text(f"💥 Ошибка в матрице: {e}")

async def main():
    print("🚀 Бот запущен через метод скачивания!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
