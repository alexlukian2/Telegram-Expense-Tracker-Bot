import os
import logging
from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.utils.executor import start_webhook
from db import init_db, add_record, get_stats

# Environment
API_TOKEN = os.getenv("API_TOKEN")
if not API_TOKEN:
    raise RuntimeError("API_TOKEN is not set")

# WEBHOOK_BASE must be like: https://your-service.onrender.com
WEBHOOK_BASE = os.getenv("WEBHOOK_BASE")
if not WEBHOOK_BASE:
    raise RuntimeError("WEBHOOK_BASE is not set (e.g. https://your-service.onrender.com)")

# Use token as part of path for simple protection
WEBHOOK_PATH = f"/webhook/{API_TOKEN}"
WEBHOOK_URL = f"{WEBHOOK_BASE}{WEBHOOK_PATH}"

# Render provides PORT to bind web server
WEBAPP_HOST = "0.0.0.0"
WEBAPP_PORT = int(os.getenv("PORT", "8000"))

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
init_db()

HELP_TEXT = (
    "Я фінансовий трекер 🤖\n"
    "Доступні команди:\n"
    "/help - допомога\n"
    "/week - статистика за тиждень\n"
    "/month - статистика за місяць\n"
    "/all - статистика за весь час\n"
    "/balance - показати загальний баланс\n\n"
    "Щоб додати витрату:\n-200 їжа\n\n"
    "Щоб додати дохід:\n+15000 зарплата\n"
)

@dp.message_handler(commands=["start", "help"])
async def send_welcome(message: types.Message):
    await message.reply(HELP_TEXT)

@dp.message_handler(commands=["balance"])
async def balance(message: types.Message):
    _, income, expense = get_stats(message.from_user.id, "all")
    await message.reply(
        f"📈 Загальний баланс: {income - expense:.2f} грн\n"
        f"💵 Дохід: {income:.2f} грн\n"
        f"💸 Витрати: {expense:.2f} грн"
    )

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

async def on_startup(dispatcher: Dispatcher):
    await bot.set_webhook(WEBHOOK_URL)
    logging.info(f"Webhook set to {WEBHOOK_URL}")

async def on_shutdown(dispatcher: Dispatcher):
    logging.info("Shutting down... deleting webhook")
    await bot.delete_webhook()

# Optional health check
async def healthcheck(request: web.Request) -> web.Response:
    return web.Response(text="OK")

# Aiohttp application factory (not strictly needed with start_webhook, but handy for extra routes)
def create_app() -> web.Application:
    app = web.Application()
    app.router.add_get("/health", healthcheck)
    return app

if __name__ == "__main__":
    # start_webhook will create and run aiohttp server and register webhook handler at WEBHOOK_PATH
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
        skip_updates=True,
    ) 