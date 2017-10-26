import os, sys
from flask import Flask, request
from utils import wit_response
from pymessenger import Bot

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
				
				# Names
				sender_name = messaging_event['sender']
				
				if messaging_event.get('message'):
					if 'text' in messaging_event['message']:
						messaging_text = messaging_event['message']['text']
					else:
						messaging_text = 'no text'
					
					response = None
					entity, value = wit_response(messaging_text)
					
					if entity == 'greeting_keys':
						response = "გამარჯობა {}!".format(sender_name)
						
					if response == None:
						response = "{} ბოდიში, ვერ გავიგე?".format(sender_name)
					bot.send_text_message(sender_id, response)
	
	return "ok", 200
	
def log(message):
	print(message)
	sys.stdout.flush()

if __name__ == "__main__":
	app.run(debug = True, port = 80)
