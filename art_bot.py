import asyncio
import random
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import URLInputFile

# --- КОНФИГУРАЦИЯ ---
BOT_TOKEN = "8761763990:AAG9Fs3Umzzqt9zMwSZAbqIaGt8ZTMeMu8M"
# ---------------------

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "🎨 **Бот-художник готов!**\n\n"
        "Напиши `/gen` и через пробел любой бред, который хочешь увидеть.\n"
        "Пример: `/gen суровый челябинский мужик верхом на медведе в космосе`"
    )

@dp.message(Command("gen"))
async def generate_img(message: types.Message):
    # Получаем текст запроса
    prompt = message.text.replace("/gen", "").strip()
    
    if not prompt:
        await message.reply("⚠️ Слышь, а рисовать-то что? Напиши текст после команды!")
        return

    wait_msg = await message.answer("⏳ Так-с, включаю воображение... Погоди...")

    # Генерируем ссылку. Используем модель flux (она сейчас самая крутая и бесплатная)
    seed = random.randint(1, 999999)
    # Кодируем пробелы для ссылки
    safe_prompt = prompt.replace(" ", "%20")
    image_url = f"https://pollinations.ai{safe_prompt}?seed={seed}&width=1024&height=1024&model=flux&nologo=true"

    try:
        # Отправляем фото
        photo = URLInputFile(image_url)
        await message.answer_photo(
            photo=photo, 
            caption=f"🖼 **Запрос:** {prompt}\n✨ Модель: Flux.1"
        )
        await wait_msg.delete()
    except Exception as e:
        await wait_msg.edit_text(f"💩 Бля, что-то пошло не так. Нейронка устала. Ошибка: {e}")

async def main():
    print("🎨 Бот-художник запущен и ждет твоих фантазий!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
