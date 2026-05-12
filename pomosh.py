import asyncio
import random
from datetime import timedelta
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ChatPermissions

# --- КОНФИГУРАЦИЯ ---
# Вставь сюда свой токен от BotFather
BOT_TOKEN = "8761763990:AAG9Fs3Umzzqt9zMwSZAbqIaGt8ZTMeMu8M" 
# ---------------------

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Функция проверки прав админа
async def is_user_admin(message: types.Message):
    member = await bot.get_chat_member(message.chat.id, message.from_user.id)
    return member.status in ['creator', 'administrator']

# --- КОМАНДА БАН ---
@dp.message(Command("ban"))
async def ban_user(message: types.Message):
    if not message.reply_to_message:
        await message.reply("⚠️ Ты в воздух стреляешь? Ответь на сообщение того, кого хочешь выставить за дверь!")
        return

    if not await is_user_admin(message):
        await message.reply("🤣 Слышь, ты куда лезешь? У тебя прав не хватит тут командовать!")
        return

    user = message.reply_to_message.from_user
    try:
        await bot.ban_chat_member(message.chat.id, user.id)
        responses = [
            f"🚀 {user.first_name} отправляется в полет... в бан!",
            f"👋 Поздравляю, {user.first_name}, ты договорился. Проваливай!",
            f"🗑 Порядок наведен. {user.first_name}, не возвращайся.",
            f"🤡 Минус один. {user.first_name} больше нас не побеспокоит."
        ]
        await message.answer(random.choice(responses))
    except Exception:
        await message.answer("🔧 Не могу забанить, прав админа не хватает!")

# --- КОМАНДА МУТ ---
@dp.message(Command("mute"))
async def mute_user(message: types.Message):
    if not message.reply_to_message:
        await message.reply("⚠️ Укажи на того, кому пора помолчать!")
        return

    if not await is_user_admin(message):
        await message.reply("🤫 Тс-с-с... Твой голос здесь ничего не решает. Админа позови.")
        return

    # Парсим время мута
    args = message.text.split()
    mute_time = 10 
    if len(args) > 1 and args[1].isdigit():
        mute_time = int(args[1])

    user = message.reply_to_message.from_user
    permissions = ChatPermissions(can_send_messages=False)

    try:
        await bot.restrict_chat_member(
            message.chat.id, 
            user.id, 
            permissions=permissions, 
            until_date=timedelta(minutes=mute_time)
        )
        await message.answer(
            f"🤐 {user.first_name}, твой микрофон отключен на {mute_time} мин.\n"
            f"Посиди в тишине, подумай над своим поведением."
        )
    except Exception:
        await message.answer("🔧 Ошибка при выдаче мута. Проверь настройки моих прав!")

# --- КОМАНДА УНБАН / АНМУТ ---
@dp.message(Command("unban"))
async def unban_user(message: types.Message):
    if not message.reply_to_message:
        await message.reply("⚠️ Кого амнистировать? Ответь на сообщение.")
        return

    if not await is_user_admin(message):
        return

    user = message.reply_to_message.from_user
    try:
        await bot.unban_chat_member(message.chat.id, user.id)
        await message.answer(f"😇 Ладно, {user.first_name}, сегодня день прощения. Можешь вернуться, но веди себя тихо.")
    except Exception:
        await message.answer("🔧 Не получается разблокировать. Проверь права бота.")

# Запуск бота
async def main():
    print("Бот запущен и готов наводить порядок...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот выключен.")
