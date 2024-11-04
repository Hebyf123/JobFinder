import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

def send_telegram_id_to_server(telegram_id, telegram_token):
    url = 'https://your-site.com/social_auth/telegram/bind-telegram/'  
    headers = {
        'Content-Type': 'application/json',
    }
    data = {
        'telegram_id': telegram_id,
        'telegram_token': telegram_token,
    }
    
    response = requests.post(url, headers=headers, json=data)
    return response.json()

def start(update: Update, context: CallbackContext) -> None:
    telegram_id = update.message.chat_id
    telegram_token = context.args[0] if context.args else None  
    
    if not telegram_token:
        update.message.reply_text("Введите одноразовый токен для привязки Telegram. Используйте команду в формате: /start <токен>")
        return

    response = send_telegram_id_to_server(telegram_id, telegram_token)
    
    if response.get("message") == "Telegram ID успешно привязан.":
        update.message.reply_text(f"Ваш Telegram ID: {telegram_id}. Аккаунт успешно привязан.")
    else:
        update.message.reply_text(f"Ошибка: {response.get('error')}")

def contact_manager(update: Update, context: CallbackContext) -> None:
    manager_chat_url = "https://t.me/your_manager_chat"  # Ссылка на чат менеджера
    update.message.reply_text(f"Связаться с менеджером: {manager_chat_url}")

def main():
    bot_token = 'YOUR_BOT_TOKEN'
    updater = Updater(bot_token, use_context=True)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))

    dispatcher.add_handler(CommandHandler('manager', contact_manager))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
