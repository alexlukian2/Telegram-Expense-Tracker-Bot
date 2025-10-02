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

## Деплой на Render (Background Worker)
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

## Оновлення
- Після змін у коді: пуш → Render автоматично перебілдить і перезапустить воркер.

## Примітки
- SQLite без Persistent Disk зберігається у тимчасовому сховищі і може очищатися під час перезапусків. Для збереження історії використовуй Persistent Disk або зовнішню БД. 