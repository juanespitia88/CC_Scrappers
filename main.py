import telebot
import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()
tok = os.environ.get('bot_env')
api_key = os.environ.get('api_key')  # Asegúrate de que tu clave API esté en las variables de entorno
bot = telebot.TeleBot(tok)

@bot.message_handler(commands=['start'])
def cmds(message):
    bot.reply_to(message, text='Welcome. Hit /cmds or /help for available commands')

@bot.message_handler(commands=['help', 'cmds'])
def cmds(message):
    bot.reply_to(message, text=''' 
command - usage
/scr <username> <post_number> - Get contents of a specific post
/scrsk <username> <post_number> - Get sk contents (implementación de ejemplo)
    ''')

@bot.message_handler(commands=['scr'])
def scrape_post(message):
    try:
        parts = message.text.split()
        if len(parts) != 3:
            bot.reply_to(message, text='Usage: /scr <username> <post_number>')
            return
        
        username = parts[1]  # Nombre de usuario del canal
        post_number = parts[2]  # Número de publicación

        # Llamar a la API para obtener el contenido de la publicación
        api_url = f'https://apibot.ir/api/telegram-scraper/getContents'
        params = {
            'key': api_key,
            'username': username,
            'post_number': post_number
        }

        retries = 3  # Intentos máximos
        for attempt in range(retries):
            try:
                response = requests.get(api_url, params=params, timeout=10)
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

        # Manejo de la respuesta
        if 'error' in raw:
            bot.reply_to(message, text=raw['error'])
        else:
            content = raw.get('content', 'No content available')
            found = post_number  # Usando el número de publicación como identificador
            file = f'x{found} Scrapped.txt'

            if content is not None:
                with open(file, "w+") as f:
                    f.write(content)
                with open(file, "rb") as f:
                    cap = '<b>Scrapped Successfully ✅\nTarget -» <code>' + username.upper() + '</code>\nFound -» <code>' + str(found) + '</code>\nREQ BY -» <code>' + message.from_user.first_name + '</code></b>'
                    bot.send_document(chat_id=message.chat.id, document=f, caption=cap, parse_mode='HTML')
                    os.remove(file)
            elif content is None:
                bot.reply_to(message, text='No cards were found.')

    except Exception as e:
        bot.reply_to(message, text=f"Ocurrió un error: {str(e)}")

@bot.message_handler(commands=['scrsk'])
def scrape_sk(message):
    try:
        parts = message.text.split()
        if len(parts) != 3:
            bot.reply_to(message, text='Usage: /scrsk <username> <post_number>')
            return

        username = parts[1]
        post_number = parts[2]

        # Aquí podrías implementar la lógica para obtener información sobre el "sk", similar a scrape_post.
        # Este es un ejemplo que necesitaría ser ajustado según tus necesidades.
        bot.reply_to(message, text='Función /scrsk no implementada todavía.')

    except Exception as e:
        bot.reply_to(message, text=f"Ocurrió un error: {str(e)}")

bot.polling()
