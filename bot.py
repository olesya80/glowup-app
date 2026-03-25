#!/usr/bin/env python3
"""
Glow Up Bot 🌱
Telegram-бот с напоминаниями, мотивацией и кнопкой для Mini App.
Запуск: python3 bot.py
"""

import asyncio
import random
import logging
from datetime import datetime, time

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    WebAppInfo,
)
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
    JobQueue,
)

# ============================================================
# НАСТРОЙКИ
# ============================================================
BOT_TOKEN = "8628622666:AAHEEPHTB1gD9eAKWhy0-IOyfeeKRM2MlGM"
WEB_APP_URL = "https://olesya80.github.io/glowup-app/"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ============================================================
# ТЕКСТЫ
# ============================================================
MORNING_MESSAGES = [
    "🌅 Доброе утро! Какой сегодня квест?\n\nОткрой приложение и отметь первое действие ✨",
    "☀️ Новый день — новая возможность!\n\nДаже 5 минут движения — это уже победа 🌿",
    "🌸 Привет! Сегодня отличный день, чтобы сделать что-то для себя.\n\nОткрой Glow Up и начни с малого 💫",
    "🦋 Утро! Тело ждёт заботы.\n\nВода, движение, внимание к себе — всё считается ✨",
    "🌊 Доброе утро! Помни: нет неправильных шагов.\n\nЛюбое движение — это прогресс 🌱",
]

EVENING_MESSAGES = [
    "🌙 Как прошёл день?\n\nОткрой приложение и запиши, что ты сегодня сделала для себя 🤍",
    "✨ Вечер! Время подвести итоги.\n\nЧто бы ты ни сделала сегодня — это уже достаточно 💫",
    "🌿 День заканчивается. Ты молодец!\n\nЗагляни в Glow Up и отметь свои действия 🌸",
    "💜 Вечер! Не забудь записать свои достижения.\n\nКаждый шаг имеет значение ✨",
    "🕯 Время для себя. Что было хорошего сегодня?\n\nОткрой приложение и отметь 🦋",
]

MOTIVATION_MESSAGES = [
    "💪 Ты сильнее, чем думаешь",
    "🌱 Маленькие шаги ведут к большим переменам",
    "✨ Ты уже на пути — и это главное",
    "🌊 Каждый день — новый шанс позаботиться о себе",
    "🦋 Ты становишься лучшей версией себя",
    "🔥 Твоя энергия растёт с каждым действием",
    "🌸 Забота о теле — это забота о душе",
    "💫 Ты выбираешь себя — и это прекрасно",
    "🤍 Нет провалов — есть только путь",
    "🌿 Движение — это любовь к себе",
]

STREAK_MESSAGES = {
    3: "🔥 3 дня подряд! Ты набираешь ритм! +10 XP бонус 💪",
    5: "⚡ 5 дней подряд! Вот это сила воли! Ты невероятная ✨",
    7: "🏆 НЕДЕЛЯ подряд! Ты — легенда! +20 XP бонус 🔥🔥🔥",
    14: "💎 2 недели без перерыва! Это уже привычка! Ты сияешь ✨",
    21: "👑 3 недели! Ты абсолютная королева движения 🌟",
    30: "🌟 МЕСЯЦ! Невероятно! Ты полностью преобразилась 💫",
}

# Хранилище ID пользователей для рассылки
USER_IDS_FILE = "users.txt"


def load_users():
    try:
        with open(USER_IDS_FILE, "r") as f:
            return set(int(line.strip()) for line in f if line.strip())
    except FileNotFoundError:
        return set()


def save_user(user_id):
    users = load_users()
    users.add(user_id)
    with open(USER_IDS_FILE, "w") as f:
        for uid in users:
            f.write(f"{uid}\n")


# ============================================================
# КНОПКА ОТКРЫТЬ ПРИЛОЖЕНИЕ
# ============================================================
def app_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(
            text="🌱 Открыть Glow Up",
            web_app=WebAppInfo(url=WEB_APP_URL),
        )],
    ])


def motivation_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(
            text="🌱 Открыть Glow Up",
            web_app=WebAppInfo(url=WEB_APP_URL),
        )],
        [InlineKeyboardButton(
            text="✨ Ещё мотивация",
            callback_data="motivation",
        )],
    ])


# ============================================================
# ОБРАБОТЧИКИ КОМАНД
# ============================================================
async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    save_user(user.id)
    name = user.first_name or "солнце"

    text = (
        f"✨ Привет, {name}!\n\n"
        f"Добро пожаловать в **Glow Up** — твой фитнес-квест!\n\n"
        f"🌱 Отмечай движение\n"
        f"⚡ Набирай XP\n"
        f"💪 Прокачивай тело\n"
        f"🔥 Без давления и стресса\n\n"
        f"Нажми кнопку ниже, чтобы начать 👇"
    )

    await update.message.reply_text(
        text,
        parse_mode="Markdown",
        reply_markup=app_keyboard(),
    )


async def cmd_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.effective_user.first_name or "солнце"
    msg = random.choice(MOTIVATION_MESSAGES)

    text = (
        f"📊 {name}, твоя статистика — внутри приложения!\n\n"
        f"Открой Glow Up, чтобы увидеть:\n"
        f"• Общий XP и уровень\n"
        f"• Серию дней подряд 🔥\n"
        f"• Историю за 7 дней\n"
        f"• Прогресс по тренировкам\n\n"
        f"_{msg}_"
    )

    await update.message.reply_text(
        text,
        parse_mode="Markdown",
        reply_markup=app_keyboard(),
    )


async def cmd_motivation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = random.choice(MOTIVATION_MESSAGES)
    await update.message.reply_text(
        msg,
        reply_markup=motivation_keyboard(),
    )


async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🌱 **Glow Up — команды:**\n\n"
        "/start — начать\n"
        "/open — открыть приложение\n"
        "/motivation — получить мотивацию\n"
        "/stats — моя статистика\n"
        "/help — эта справка\n\n"
        "Просто нажми кнопку Menu внизу чата — "
        "и приложение откроется! 💫"
    )
    await update.message.reply_text(text, parse_mode="Markdown")


async def cmd_open(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👇 Нажми, чтобы открыть Glow Up",
        reply_markup=app_keyboard(),
    )


# ============================================================
# ОТВЕТ НА ЛЮБОЕ ТЕКСТОВОЕ СООБЩЕНИЕ
# ============================================================
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    save_user(update.effective_user.id)
    text = (update.message.text or "").lower().strip()

    # Реагируем на ключевые слова
    greetings = ["привет", "хай", "hello", "hi", "здравствуй", "прив", "ку"]
    if any(g in text for g in greetings):
        name = update.effective_user.first_name or "солнце"
        msg = random.choice([
            f"Привет, {name}! 🌸 Готова к действию?",
            f"Хей, {name}! ✨ Как ты сегодня?",
            f"Привет! 🦋 Рада тебя видеть!",
        ])
        await update.message.reply_text(msg, reply_markup=app_keyboard())
        return

    mood_words = ["устала", "тяжело", "плохо", "грустно", "лень", "не хочу", "сложно"]
    if any(w in text for w in mood_words):
        msg = random.choice([
            "🤍 Всё ок. Не нужно быть идеальной.\nДаже стакан воды — это действие. Ты достаточно.",
            "🌿 Слушай своё тело. Отдых — тоже забота о себе.\nЕсли хочешь — отметь хотя бы воду 💧",
            "💜 Бывают такие дни. Ты не обязана.\nНо если сделаешь хоть что-то маленькое — будешь гордиться собой ✨",
            "🦋 Нежно к себе. Без давления.\nМожет, просто 5 минут движения? Только если хочется.",
        ])
        await update.message.reply_text(msg, reply_markup=app_keyboard())
        return

    good_words = ["хорошо", "отлично", "супер", "класс", "круто", "ура", "сделала", "потренировалась"]
    if any(w in text for w in good_words):
        msg = random.choice([
            "🔥 Вот это да! Ты молодец!",
            "✨ Горжусь тобой! Продолжай в том же духе!",
            "💪 Это заслуживает XP! Открой приложение и отметь!",
            "🌟 Круто! Каждое действие делает тебя сильнее!",
        ])
        await update.message.reply_text(msg, reply_markup=app_keyboard())
        return

    # По умолчанию — мотивация + кнопка
    msg = random.choice(MOTIVATION_MESSAGES)
    await update.message.reply_text(
        f"{msg}\n\n👇 Открой приложение",
        reply_markup=app_keyboard(),
    )


# ============================================================
# CALLBACK КНОПКИ
# ============================================================
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "motivation":
        msg = random.choice(MOTIVATION_MESSAGES)
        await query.edit_message_text(
            msg,
            reply_markup=motivation_keyboard(),
        )


# ============================================================
# УТРЕННИЕ И ВЕЧЕРНИЕ НАПОМИНАНИЯ
# ============================================================
async def send_morning(context: ContextTypes.DEFAULT_TYPE):
    users = load_users()
    msg = random.choice(MORNING_MESSAGES)
    for uid in users:
        try:
            await context.bot.send_message(
                chat_id=uid,
                text=msg,
                reply_markup=app_keyboard(),
            )
        except Exception as e:
            logger.warning(f"Не удалось отправить утреннее сообщение {uid}: {e}")


async def send_evening(context: ContextTypes.DEFAULT_TYPE):
    users = load_users()
    msg = random.choice(EVENING_MESSAGES)
    for uid in users:
        try:
            await context.bot.send_message(
                chat_id=uid,
                text=msg,
                reply_markup=app_keyboard(),
            )
        except Exception as e:
            logger.warning(f"Не удалось отправить вечернее сообщение {uid}: {e}")


async def send_midday_motivation(context: ContextTypes.DEFAULT_TYPE):
    """Дневная мотивация — отправляется только иногда (30% шанс)"""
    if random.random() > 0.3:
        return
    users = load_users()
    msg = random.choice(MOTIVATION_MESSAGES)
    for uid in users:
        try:
            await context.bot.send_message(
                chat_id=uid,
                text=f"💌 Напоминание о себе:\n\n{msg}",
                reply_markup=app_keyboard(),
            )
        except Exception as e:
            logger.warning(f"Не удалось отправить мотивацию {uid}: {e}")


# ============================================================
# MAIN
# ============================================================
def main():
    print("🌱 Glow Up Bot запускается...")
    print(f"📱 Web App: {WEB_APP_URL}")
    print("━" * 40)

    app = Application.builder().token(BOT_TOKEN).build()

    # Команды
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("stats", cmd_stats))
    app.add_handler(CommandHandler("motivation", cmd_motivation))
    app.add_handler(CommandHandler("help", cmd_help))
    app.add_handler(CommandHandler("open", cmd_open))

    # Кнопки
    app.add_handler(CallbackQueryHandler(handle_callback))

    # Текстовые сообщения
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    # Расписание напоминаний (UTC+3 для Москвы)
    # Утро 8:00 MSK = 5:00 UTC
    # День 13:00 MSK = 10:00 UTC
    # Вечер 21:00 MSK = 18:00 UTC
    job_queue = app.job_queue
    if job_queue:
        job_queue.run_daily(send_morning, time=time(5, 0, 0))  # 8:00 MSK
        job_queue.run_daily(send_midday_motivation, time=time(10, 0, 0))  # 13:00 MSK
        job_queue.run_daily(send_evening, time=time(18, 0, 0))  # 21:00 MSK
        print("⏰ Напоминания настроены:")
        print("   🌅 08:00 — утреннее")
        print("   ☀️  13:00 — мотивация (30% шанс)")
        print("   🌙 21:00 — вечернее")

    print("━" * 40)
    print("✅ Бот запущен! Нажми Ctrl+C чтобы остановить.")
    print("")

    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
