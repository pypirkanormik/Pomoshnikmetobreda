import asyncio
import random
import urllib.parse
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import URLInputFile

# --- КОНФИГУРАЦИЯ ---
TOKEN = "8761763990:AAG9Fs3Umzzqt9zMwSZAbqIaGt8ZTMeMu8M"
# ---------------------

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("gen"))
async def generate_img(message: types.Message):
    prompt = message.text.replace("/gen", "").strip()
    
    if not prompt:
        await message.reply("💀 Напиши хоть слово, художник!")
        return

    wait_msg = await message.answer("🔮 Рисую... Если через 20 сек не придет — значит нейросеть приуныла.")

    # Кодируем текст так, чтобы в нем не было кривых символов
    safe_prompt = urllib.parse.quote(prompt)
    # Используем максимально простую ссылку без лишних наворотов
    seed = random.randint(1, 999999)
    image_url = f"https://pollinations.ai{safe_prompt}?seed={seed}&width=1024&height=1024&nologo=true"

    try:
        # Отправляем просто ссылку. Telegram сам попробует её скачать.
        photo = URLInputFile(image_url)
        await message.answer_photo(
            photo=photo, 
            caption=f"🔥 **Материя сформирована:** \n_{prompt}_",
            parse_mode="Markdown"
        )
        await wait_msg.delete()
                    
    except Exception as e:
        await wait_msg.edit_text(f"💥 Ошибка: {str(e)}")

async def main():
    print("🚀 Бот запущен в лайт-режиме!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
