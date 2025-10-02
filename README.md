# Telegram Finance Bot (aiogram)

Простий трекер доходів/витрат у Telegram на `aiogram==2.25.1` з SQLite.

## Можливості
- Додавання доходів `+1000 зарплата` і витрат `-200 їжа`
- Періодична статистика: `/week`, `/month`, `/all`
- Загальний баланс: `/balance`

## Вимоги
- Python 3.9+
- Токен бота від `@BotFather`

## Налаштування середовища
Змінні оточення (див. файл `Environment`):
- `API_TOKEN` — обовʼязково
- `DB_PATH` — опційно, шлях до SQLite (за замовчуванням `/var/tmp/finance.db`)
- Для вебхука на Render: `WEBHOOK_BASE` — базова URL вебсервісу, наприклад `https://<service>.onrender.com`

## Локальний запуск
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
export API_TOKEN="<your_token>"
# за бажанням: export DB_PATH="./finance.db"
python -u bot.py
```

## Деплой на Render як Background Worker (long polling)
1. Пуш коду в GitHub/GitLab (у корені мають бути `bot.py`, `db.py`, `requirements.txt`, `Procfile`).
2. На Render: New → Background Worker → підключи репозиторій.
3. Build Command:
   ```
   pip install --upgrade pip && pip install -r requirements.txt
   ```
4. Start Command:
   ```
   python -u bot.py
   ```
5. Environment (Render → Settings → Environment):
   - Додай `API_TOKEN=<твій_токен>`
   - (Опційно) Додай Persistent Disk і встанови `DB_PATH=/data/finance.db`

Після запуску в логах побачиш `Start polling.`

## Деплой на Render як Web Service (webhook)
1. Додай файл `webhook_app.py` (в репозиторії вже є) — він піднімає вебсервер і реєструє вебхук.
2. На Render: New → Web Service → підключи репозиторій.
3. Root Directory: якщо код у корені — `.` (за замовчуванням). Якщо у підпапці, вкажи її назву.
4. Build Command:
   ```
   pip install --upgrade pip && pip install -r requirements.txt
   ```
5. Start Command:
   ```
   python -u webhook_app.py
   ```
6. Environment:
   - `API_TOKEN=<твій_токен>`
   - `WEBHOOK_BASE=https://<service>.onrender.com` (після створення сервісу Render покаже домен)
   - (опційно) `DB_PATH=/data/finance.db` та додай Persistent Disk (Mount path `/data`) для збереження БД

Після старту в логах зʼявиться `Webhook set to https://<service>.onrender.com/webhook/<TOKEN>`. Надішли `/start` у бота.

## Оновлення
- Після змін у коді: пуш → Render автоматично перебілдить і перезапустить сервіс/воркер.

## Примітки
- Без диска SQLite-файл може пропадати при перезапусках. Для постійної історії додай Persistent Disk або використай зовнішню БД. 