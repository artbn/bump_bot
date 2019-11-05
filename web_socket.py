import praw
import json
import websocket
import bump_class

close = False
# Setup functions to print different things for different stages of connection
on_open = lambda ws: print('WebSocket connection opened')
def on_close(ws): 
	global close
	if close:
		print('WebSocket connection closed\n')
		close = False
	else:
		ws.run_forever()
def on_message(ws,data): 
	request = json.loads(data) # converts from string to array
	if request['type'] != 'update': return; #if not update, send it back
	if request['payload']['data']['author'] != 'LiveBumpBot': return #if not from bot, send it back
	ID = request['payload']['data']['name']

	bump_class.delete(ID)
	global close
	close = True
	
	ws.close()