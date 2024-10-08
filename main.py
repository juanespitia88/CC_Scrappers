import telebot
import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()
tok = os.environ.get('bot_env')
bot = telebot.TeleBot(tok)

@bot.message_handler(commands=['start'])
def cmds(message):
    bot.reply_to(message, text='Welcome. Hit /cmds or /help for available commands')

@bot.message_handler(commands=['help', 'cmds'])
def cmds(message):
    bot.reply_to(message, text='''
command - usage
/scr - /scr placeholder 100
/scrsk - /scrsk placeholder 100
    ''')

@bot.message_handler(commands=['scr'])
def scrape_cc(message):
    try:
        parts = message.text.split()
        if len(parts) == 3:
            chat_id = parts[1]
            limit = parts[2]
            bin = 'All'
        elif len(parts) == 4:
            chat_id = parts[1]
            limit = parts[2]
            bin = parts[3]
        
        retries = 3  # Intentos máximos
        for attempt in range(retries):
            try:
                # Usar una URL de prueba funcional
                response = requests.get('https://jsonplaceholder.typicode.com/todos/1', timeout=10)
                if response.status_code == 200:
                    raw = response.json()
                    break
                else:
                    bot.reply_to(message, text=f"Error en la solicitud. Código: {response.status_code}")
                    return

            except requests.exceptions.RequestException as e:
                if attempt < retries - 1:
                    bot.reply_to(message, text="Intentando reconectar...")
                    time.sleep(5)
                    continue
                else:
                    bot.reply_to(message, text="Error de conexión. El servidor parece estar inactivo.")
                    return

        # Simulación de datos extraídos
        cards = "Simulated cards data from placeholder API"
        found = raw.get('id', 0)  # Usando el campo 'id' del JSON de prueba
        file = f'x{found} Scrapped.txt'

        if cards is not None:
            with open(file, "w+") as f:
                f.write(cards)
            with open(file, "rb") as f:
                cap = '<b>Scrapped Successfully ✅\nTarget -» <code>' + chat_id.upper() + '</code>\nFound -» <code>' + str(found) + '</code>\nBin -» <code>' + bin + '</code>\nREQ BY -» <code>' + message.from_user.first_name + '</code></b>'
                bot.send_document(chat_id=message.chat.id, document=f, caption=cap, parse_mode='HTML')
                os.remove(file)
        elif cards is None:
            bot.reply_to(message, text='No cards were found.')
    except Exception as e:
        bot.reply_to(message, text=f"Ocurrió un error: {str(e)}")

@bot.message_handler(commands=['scrsk'])
def scrape_sk(message):
    try:
        parts = message.text.split()
        chat_id = parts[1]
        limit = parts[2]
        
        retries = 3  # Intentos máximos
        for attempt in range(retries):
            try:
                # Usar una URL de prueba funcional
                response = requests.get('https://jsonplaceholder.typicode.com/todos/1', timeout=10)
                if response.status_code == 200:
                    raw = response.json()
                    break
                else:
                    bot.reply_to(message, text=f"Error en la solicitud. Código: {response.status_code}")
                    return

            except requests.exceptions.RequestException as e:
                if attempt < retries - 1:
                    bot.reply_to(message, text="Intentando reconectar...")
                    time.sleep(5)
                    continue
                else:
                    bot.reply_to(message, text="Error de conexión. El servidor parece estar inactivo.")
                    return

        # Simulación de datos extraídos
        cards = "Simulated sk data from placeholder API"
        found = raw.get('id', 0)  # Usando el campo 'id' del JSON de prueba
        file = f'x{found} Scrapped.txt'

        if cards is not None:
            with open(file, "w+") as f:
                f.write(cards)
            with open(file, "rb") as f:
                cap = '<b>Scrapped Successfully ✅\nTarget -» <code>' + chat_id.upper() + '</code>\nFound -» <code>' + str(found) + '</code>\nREQ BY -» <code>' + message.from_user.first_name + '</code></b>'
                bot.send_document(chat_id=message.chat.id, document=f, caption=cap, parse_mode='HTML')
                os.remove(file)
        elif cards is None:
            bot.reply_to(message, text='No sk were found.')
    except Exception as e:
        bot.reply_to(message, text=f"Ocurrió un error: {str(e)}")

bot.polling()
