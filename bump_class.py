import praw
import json
import websocket
import time

import config
import web_socket

ws = None;

def bot_login():
	print("Logging In...")
	login = praw.Reddit(username = config.username,
				password = config.password,
				client_id = config.client_id,
				client_secret = config.client_secret,
				user_agent = "Bumps threads from being deleted v0.6")
	print("Logged in!")
	return login

login = bot_login()


class Bumper():
	def __init__(self,thread):
		self.thread = thread

	def thread_about(self):
		#Returns the live thread's about.json data, including the WebSocket (wss) URL, sidebar (resources) contents, etc.
		this_thread = self.thread
		print("Connecting to " + this_thread)
		# Get websocket_url from about.json
		response = login.request(
			method = 'GET',
			path = 'live/' +this_thread+ '/about',
			params = { 'raw_json': 1 }
		);

		# Return websocket_url from response
		return response

	on_open = lambda self, ws: print('WebSocket connection opened')
	def on_close(self,ws): 
		print('WebSocket connection closed\n')
	def on_message(self,ws,data): 
		request = json.loads(data) # converts from string to array
		if request['type'] != 'update': return; #if not update, send it back
		if request['payload']['data']['author'] != 'LiveBumpBot': return #if not from bot, send it back
		ID = request['payload']['data']['name']

		self.delete(ID)
		global close
		close = True
		
		ws.close()


	def connect(self):
		websocket_url = (self.thread_about())['data']['websocket_url'];
		print("Found url: " + websocket_url)

		# Now connect to the websocket
		ws = websocket.WebSocketApp(
		    websocket_url,
		    on_open = self.on_open,
		    on_close = self.on_close,
		    on_message = self.on_message
		)
		ws.run_forever()



	def post(self):
		try:
			this_thread = self.thread
			print("Posting message on: " + this_thread)
			login.request(
			method = 'POST',
			path = 'api/live/' + this_thread + '/update',
			data = {
				'api_type': 'json',
				'body': "**You should not see this**\n If you do there has been an error."
			}
			)
		except prawcore.exceptions.Forbidden:
			print("Forbidden! Probably archived: " + this_thread)


	def delete(self, update_id):
		print("Deleting " + update_id)
		this_thread = self.thread
		print("Deleting message on: " + this_thread)
		login.request(
			method = 'POST',
			path = 'api/live/' + this_thread + '/delete_update',
			data = {
				'api_type': 'json',
				'id': update_id
			}
		)

