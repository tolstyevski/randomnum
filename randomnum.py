import telegram
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import random

# Your bot token obtained from BotFather
TOKEN = '6169116451:AAFZFEYSp_jkWgQs2tGUrYaWVa0BgCP5ARA'

# Create bot instance
bot = telegram.Bot(token=TOKEN)

# Create updater and dispatcher instances
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

def start(update, context):
    update.message.reply_text('Por favor, envíame dos valores numéricos separados por un espacio para generar un número aleatorio entre ellos.')

def generate_number(update, context, from_callback=False):
    # Obtener los dos valores numéricos enviados por el usuario
    if not from_callback:
        values = update.message.text.split()
        num1 = int(values[0])
        num2 = int(values[1])
    else:
        num1, num2 = context.chat_data["last_numbers"]

    # Generar un número aleatorio entre los dos valores numéricos
    number = random.randint(num1, num2)

    # Agregar el número generado a la lista de números generados
    if "numbers_generated" not in context.chat_data:
        context.chat_data["numbers_generated"] = []
    numbers_generated = context.chat_data["numbers_generated"]
    while number in numbers_generated:
        number = random.randint(num1, num2)
    numbers_generated.append(number)

    # Ordenar la lista de números generados de mayor a menor
    numbers_generated.sort(reverse=True)

    # Crear la lista de números generados para enviar al usuario
    numbers_list = "\n".join(str(n) for n in numbers_generated)

    # Crear el botón para generar un nuevo número
    button = InlineKeyboardButton("Generar", callback_data="generate")

    # Crear el mensaje a enviar al usuario con el número generado y la lista de números generados
    message = f"El número generado es: {number}\n\nNúmeros generados:\n{numbers_list}"

    # Crear el teclado con el botón
    keyboard = [[button]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Enviar el mensaje al usuario con el teclado
    if not from_callback:
        update.message.reply_text(message, reply_markup=reply_markup)
    else:
        context.bot.edit_message_text(chat_id=update.effective_chat.id, message_id=update.callback_query.message.message_id, text=message, reply_markup=reply_markup)

def button_callback(update, context):
    query = update.callback_query
    query.answer()
    generate_number(update, context, from_callback=True)

# Add handlers to dispatcher
start_handler = CommandHandler('start', start)
generate_handler = CommandHandler('generate', generate_number)
button_handler = CallbackQueryHandler(button_callback, pattern='generate')
dispatcher.add_handler(start_handler)
dispatcher.add_handler(generate_handler)
dispatcher.add_handler(button_handler)

# Start the bot
updater.start_polling()
