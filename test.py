
import pyowm
import telebot
import math
from flask import Flask, request
import os

server = Flask(__name__)
owm = pyowm.OWM('ef16c91feb6e48f02903e6769e2a1ebc', language = "ru")
bot = telebot.TeleBot("845338292:AAHk3_Fkyqpn4v-g28zoINnYmaSrX_WOblw")

TOKEN = "845338292:AAHk3_Fkyqpn4v-g28zoINnYmaSrX_WOblw"
@bot.message_handler(content_types=['text'])
def send_welcome(message):
	observation = owm.weather_at_place( message.text )
	w = observation.get_weather()
	temp = w.get_temperature('celsius')["temp"]

	answer = message.text + " Գոռըդում " + "հմի " + w.get_detailed_status() + "\n"
	lome = "ջերմաստիճանը մոտ " + str(round(temp)) + " աստիճան է" + "\n\n"
	if temp < 20:
		lome += "շատ ա ցուրտ տաք կ հագնվես"
	elif temp < 15:
		lome += "ըտենց շատ չի ցուրտ բայց տաք կ հագնվես"
	
		
	bot.send_message(message.chat.id, answer + str(lome))

bot.polling( none_stop = True)	
@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
	bot.process_new_updates([telebot.types.Updates.de_json(request.stream.read().decode("utf-8"))])
	return "!", 200

@server.route("/")
def webhook():
	bot.remove_webhook()
	bot.set_webhook(url='https://agile-scrubland-73104.herokuapp.com/' + TOKEN)	
	return "!", 200
if __name__ == "__main__":
server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))	