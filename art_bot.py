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

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "👁 **Добро пожаловать в визуализатор реальности.**\n\n"
        "Я превращаю твои мысли в пиксели. Пиши `/gen` и свой запрос.\n"
        "👉 *Пример: /gen золотой дракон в неоновом городе*"
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

    # Подготовка ссылки
    safe_prompt = urllib.parse.quote(prompt)
    seed = random.randint(1, 999999)
    # Используем модель flux для лучшего качества
    image_url = f"https://pollinations.ai{safe_prompt}?seed={seed}&width=1024&height=1024&model=flux&nologo=true"

    try:
        # Устанавливаем таймаут в 60 секунд, чтобы дождаться генерации
        timeout = aiohttp.ClientTimeout(total=60)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(image_url) as response:
                if response.status == 200:
                    # Скачиваем картинку в память
                    image_data = await response.read()
                    photo = BufferedInputFile(image_data, filename="art.jpg")
                    
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
                else:
                    await wait_msg.edit_text(f"💥 Нейросеть капризничает (Код: {response.status}). Попробуй еще раз.")
                    
    except Exception as e:
        # Если возникла ошибка, выводим её часть для понимания причины
        error_text = str(e)[:50]
        await wait_msg.edit_text(f"💥 Ошибка в матрице: {error_text}...")
        print(f"Полная ошибка: {e}")

async def main():
    print("🚀 Бот-художник пробудился и готов творить историю!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
