import os, sys
from flask import Flask, request
from utils import wit_response
from pymessenger import Bot
import urllib.request
from ast import literal_eval

app = Flask(__name__)

PAGE_ACCESS_TOKEN = "EAAFFJcj6snUBALL34ZAyKsJbxLydBfbCiOspvbkZBwAZCTRHTD4hOlTGBDLV5zISJnpeucdt0TVsw9rFxNImSMfal1y29nkzrQsomZA7iPHIEoGEVjI3fsficVtwaDoMZAJZCpK7FLzJj6hK1uZA78vlNwdlDBLzb4fR2Eat92QQ0z0JVtRIBgr"

bot = Bot(PAGE_ACCESS_TOKEN)

@app.route('/', methods=['GET'])
def verify():
	#Webhook verification
	if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
		if not request.args.get("hub.verify_token") == "hello":
			return "Verification token mismatch", 403
		return request.args["hub.challenge"], 200
	return "Hello world", 200
	
@app.route('/', methods=['POST'])
def webhook():
	data = request.get_json()
	log(data)
	
	if data['object'] == 'page':
		for entry in data['entry']:
			for messaging_event in entry['messaging']:
				
				# IDs
				sender_id = messaging_event['sender']['id']
				recipient_id = messaging_event['recipient']['id']
				
				if messaging_event.get('message'):
					if 'text' in messaging_event['message']:
						messaging_text = messaging_event['message']['text']
					else:
						messaging_text = 'no text'
					
					response = None
					entity, value = wit_response(messaging_text)
					
					# Names
					source = 'https://graph.facebook.com/v2.6/' + str(got_sender_id) + '?fields=first_name,last_name&access_token=' + PAGE_ACCESS_TOKEN
					r = urllib.request.urlopen(source)
					sender_n = str(r.read())
					sender_na =  sender_n[1:]
					sender_nam = sender_na.replace("'",'')
					sender_nam1 = literal_eval(sender_nam)
					sender_name = str(sender_nam1['first_name']) + " " + str(sender_nam1['last_name'])
					
					if entity == 'greeting_keys':
						response = "გამარჯობა {}!".format(sender_name)
						
					if response == None:
						response = "ბოდიში {}, ვერ გავიგე?".format(sender_name)
					bot.send_text_message(sender_id, response)
	
	return "ok", 200
	
def log(message):
	print(message)
	sys.stdout.flush()

if __name__ == "__main__":
	app.run(debug = True, port = 80)
