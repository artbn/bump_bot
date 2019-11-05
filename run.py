import praw
import json
import websocket
import threading
import time

import bump_class
import config




for i in range(len(config.threads)):
	bumper = bump_class.Bumper(config.threads[i])

	# Run connect in a separate thread
	stack = threading.Thread(target=bumper.connect)
	stack.start()

	time.sleep(7.5)
	bumper.post()

	stack.join()

print("Cycled through all!")