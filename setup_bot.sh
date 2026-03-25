#!/bin/bash
# ============================================
# Glow Up — настройка Telegram Mini App бота
# ============================================
#
# КАК ПОЛУЧИТЬ ТОКЕН:
# 1. Открой Telegram
# 2. Найди @BotFather
# 3. Напиши /newbot
# 4. Дай имя: Glow Up
# 5. Дай username (любой свободный, например: glowup_fit_123_bot)
# 6. Скопируй токен, который BotFather отправит
# 7. Вставь сюда и запусти скрипт
#
# Запуск:  bash setup_bot.sh
# ============================================

WEB_APP_URL="https://olesya80.github.io/glowup-app/"

echo ""
echo "✨ Glow Up — Настройка Telegram Mini App"
echo "========================================="
echo ""
echo "Вставь токен бота от @BotFather:"
read -r BOT_TOKEN

if [ -z "$BOT_TOKEN" ]; then
  echo "❌ Токен не может быть пустым"
  exit 1
fi

API="https://api.telegram.org/bot${BOT_TOKEN}"

echo ""
echo "⏳ Проверяю бота..."

# Check bot
RESULT=$(curl -s "${API}/getMe")
BOT_NAME=$(echo "$RESULT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('result',{}).get('first_name',''))" 2>/dev/null)

if [ -z "$BOT_NAME" ]; then
  echo "❌ Не удалось подключиться к боту. Проверь токен."
  exit 1
fi

echo "✅ Бот найден: $BOT_NAME"
echo ""

# Set menu button to open web app
echo "⏳ Настраиваю кнопку меню (откроет приложение)..."
curl -s -X POST "${API}/setChatMenuButton" \
  -H "Content-Type: application/json" \
  -d "{\"menu_button\":{\"type\":\"web_app\",\"text\":\"🌱 Glow Up\",\"web_app\":{\"url\":\"${WEB_APP_URL}\"}}}" > /dev/null

echo "✅ Кнопка меню установлена"

# Set bot description
echo "⏳ Устанавливаю описание..."
curl -s -X POST "${API}/setMyDescription" \
  -H "Content-Type: application/json" \
  -d '{"description":"Фитнес-квест с XP 🌱⚡💪🔥\nОтмечай движение, набирай очки, прокачивай тело без стресса"}' > /dev/null

curl -s -X POST "${API}/setMyShortDescription" \
  -H "Content-Type: application/json" \
  -d '{"short_description":"Фитнес-трекер с геймификацией ✨"}' > /dev/null

echo "✅ Описание установлено"

# Set commands
echo "⏳ Добавляю команды..."
curl -s -X POST "${API}/setMyCommands" \
  -H "Content-Type: application/json" \
  -d '{"commands":[{"command":"start","description":"Открыть Glow Up"},{"command":"stats","description":"Мои результаты"}]}' > /dev/null

echo "✅ Команды добавлены"

# Set welcome message via webhook-less approach: just print instructions
echo ""
echo "========================================="
echo "🎉 ВСЁ ГОТОВО!"
echo "========================================="
echo ""
echo "Теперь открой своего бота в Telegram:"
echo "  → Найди @$(echo "$RESULT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('result',{}).get('username',''))" 2>/dev/null)"
echo ""
echo "Внизу чата будет кнопка \"🌱 Glow Up\""
echo "Нажми её — откроется приложение прямо в Telegram!"
echo ""
echo "📱 Или отправь боту ссылку друзьям — у них тоже откроется"
echo ""
