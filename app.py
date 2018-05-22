import os, sys
from flask import Flask, request
from utils import wit_response
from pymessenger import Bot
import urllib.request
from ast import literal_eval

app = Flask(__name__)

PAGE_ACCESS_TOKEN = "EAAFFJcj6snUBADU8srb5sifA0JHide7NFme7MUTVgFIf8yZCB4S3qFd9CD3TB3K4nTc9SmtD4otDCAA09CZAxzND87od5cBDRveZCrWnmu8bba6uoo2QmUgWCMbZAgaZCdRc5ihXZB0dbZBmZCatpwRaGQoPRNO1BBA4YmCPr8wAEsMRf3gZAaid6"

bot = Bot(PAGE_ACCESS_TOKEN)

@app.route('/', methods=['GET'])
def verify():
	#Webhook verification
	if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
		if not request.args.get("hub.verify_token") == "hello":
			return "Verification token mismatch", 403
		return request.args["hub.challenge"], 200
	return "OK", 200
	
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
					
					def getSenderName(sender_id):
						source = 'https://graph.facebook.com/v2.6/' + str(sender_id) + '?fields=first_name,last_name&access_token=' + PAGE_ACCESS_TOKEN
						r = urllib.request.urlopen(source)
						sender_n = r.read()
						sender_list = literal_eval(sender_n.decode('ascii'))
						sender_name = str(sender_list['first_name'])
						return sender_name
					
					sender_name = getSenderName(sender_id)
					response = "Hello {0}, {1}".format(sender_name,messaging_text)
					bot.send_text_message(sender_id, response)
					
					"""
					response = None
					entity, value = wit_response(messaging_text)
					
					sender_name = ''
					noresponse_text = ''
					
					if sender_id != '1928306037421083':
						# Names
						source = 'https://graph.facebook.com/v2.6/' + str(sender_id) + '?fields=first_name,last_name&access_token=' + PAGE_ACCESS_TOKEN
						r = urllib.request.urlopen(source)
						sender_n = r.read()
						#sender_na =  sender_n[1:]
						#sender_nam = sender_na.replace("'",'')
						#sender_nam1 = literal_eval(sender_nam)
						sender_nam1 = literal_eval(sender_n.decode('ascii'))
						sender_name = str(sender_nam1['first_name'])
						noresponse_text = messaging_event['message']['text']
						
					if entity == 'greeting_keys':
						response = "გამარჯობა {}!".format(sender_name)
						
					if response == None:
						response = "ბოდიში {}, '{}' ჯერ არ ვიცი რას ნიშნავს :)".format(sender_name,noresponse_text)
					bot.send_text_message(sender_id, response)
					"""
	
	return "ok", 200
	
def log(message):
	print(message)
	sys.stdout.flush()

if __name__ == "__main__":
	app.run(debug = True, port = 80)
