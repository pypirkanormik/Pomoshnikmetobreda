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

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "👁 **Добро пожаловать в визуализатор реальности.**\n\n"
        "Я не просто бот, я — твоё воображение на стероидах. "
        "Пиши `/gen` и любой бред, который придет в твою голову.\n\n"
        "👉 *Пример: /gen неоновый самурай в кибер-Москве 2077*"
    )

@dp.message(Command("gen"))
async def generate_img(message: types.Message):
    # Достаем запрос
    prompt = message.text.replace("/gen", "").strip()
    
    if not prompt:
        await message.reply("💀 Ты пришел в храм искусства и молчишь? Напиши запрос после команды!")
        return

    # Пафосные фразы ожидания
    loading_phrases = [
        "🌌 Считываю твои мысли из ноосферы...",
        "🎨 Смешиваю пиксели твоих безумных идей...",
        "⚡️ Нейроны перегружены, но я справлюсь...",
        "🔮 Визуализирую то, что другие боятся даже представить...",
        "🏗 Строю твой личный мир из цифровой пыли..."
    ]
    
    wait_msg = await message.answer(random.choice(loading_phrases))

    # Кодируем запрос для URL (чтобы русский язык работал)
    safe_prompt = urllib.parse.quote(prompt)
    seed = random.randint(1, 999999999)
    
    # Ссылка на мощную модель Flux с авто-улучшением
    image_url = f"https://pollinations.ai{safe_prompt}?seed={seed}&width=1024&height=1024&model=flux&enhance=true&nologo=true"

    try:
        # Отправляем фото
        photo = URLInputFile(image_url)
        
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
        
    except Exception as e:
        await wait_msg.edit_text("💥 Вселенная схлопнулась! Ошибка в матрице. Попробуй еще раз.")
        print(f"Ошибка: {e}")

async def main():
    print("🚀 Бот-художник пробудился и готов творить историю!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
