import asyncio
import random
import urllib.parse
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

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

    # Пафосное уведомление
    wait_msg = await message.answer("🔮 Матрица генерирует твой запрос... Погоди.")

    # Кодируем текст для ссылки
    safe_prompt = urllib.parse.quote(prompt)
    seed = random.randint(1, 999999)
    
    # Ссылка на картинку
    image_url = f"https://pollinations.ai{safe_prompt}?seed={seed}&width=1024&height=1024&nologo=true"

    try:
        # Вместо отправки фото (которое блокирует хостинг), 
        # мы отправляем ТЕКСТ со ссылкой. ТГ сам подтянет картинку.
        await message.answer(
            f"🔥 **Твой шедевр готов!**\n\n"
            f"Запрос: _{prompt}_\n\n"
            f"[⠀]({image_url})" # Это невидимая ссылка, которая заставит ТГ показать картинку
        )
        await wait_msg.delete()
                    
    except Exception as e:
        await wait_msg.edit_text(f"💥 Ошибка: {str(e)}")

async def main():
    print("🚀 Бот запущен в режиме обхода блокировок!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
