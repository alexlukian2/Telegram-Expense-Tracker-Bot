import logging
import os
from aiogram import Bot, Dispatcher, executor, types
from db import init_db, add_record, get_stats

# 🔑 Токен читаємо з оточення
API_TOKEN = os.getenv("API_TOKEN")
if not API_TOKEN:
    raise RuntimeError("API_TOKEN is not set. Please provide it via environment variable.")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# ініціалізація бази
init_db()

HELP_TEXT = """
Я фінансовий трекер 🤖
Доступні команди:
/help - допомога
/week - статистика за тиждень
/month - статистика за місяць
/all - статистика за весь час
/balance - показати загальний баланс

Щоб додати витрату:
-200 їжа

Щоб додати дохід:
+15000 зарплата
"""

@dp.message_handler(commands=["start", "help"])
async def send_welcome(message: types.Message):
    await message.reply(HELP_TEXT)

@dp.message_handler(commands=["balance"])
async def balance(message: types.Message):
    _, income, expense = get_stats(message.from_user.id, "all")
    await message.reply(f"📈 Загальний баланс: {income - expense:.2f} грн\n💵 Дохід: {income:.2f} грн\n💸 Витрати: {expense:.2f} грн")

@dp.message_handler(commands=["week", "month", "all"])
async def stats(message: types.Message):
    period = message.text.strip("/").lower()
    expenses, income, expense = get_stats(message.from_user.id, period)

    text = f"📊 Статистика ({period}):\n\n"
    for cat, total in expenses:
        text += f"• {cat}: {total:.2f} грн\n"

    text += f"\n💵 Дохід: {income:.2f} грн"
    text += f"\n💸 Витрати: {expense:.2f} грн"
    text += f"\n📈 Баланс: {income - expense:.2f} грн"

    await message.reply(text)

@dp.message_handler()
async def add_record_handler(message: types.Message):
    text = message.text.strip()

    if text.startswith("+"):  # дохід
        try:
            parts = text[1:].split(" ", 1)
            amount = float(parts[0])
            category = parts[1] if len(parts) > 1 else "Інше"
            add_record(message.from_user.id, amount, category, "income")
            await message.reply(f"✅ Дохід {amount} грн додано (категорія: {category})")
        except:
            await message.reply("⚠️ Формат: +1000 зарплата")
    elif text.startswith("-"):  # витрата
        try:
            parts = text[1:].split(" ", 1)
            amount = float(parts[0])
            category = parts[1] if len(parts) > 1 else "Інше"
            add_record(message.from_user.id, amount, category, "expense")
            await message.reply(f"✅ Витрата {amount} грн додана (категорія: {category})")
        except:
            await message.reply("⚠️ Формат: -200 їжа")
    else:
        await message.reply("Не розпізнаю. Використай + або - для доходу/витрати.")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
