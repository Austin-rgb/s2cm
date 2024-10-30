"""
Python client module for s2cm.server
"""

import socketio

# Create a Socket.IO client
sio = socketio.Client()
long_session = None

@sio.event
def connect():
    print("Connected to the server!")


@sio.event
def disconnect():
    print("Disconnected from the server.")


@sio.event
def response(data):
    print(f"Received from server: {data}")


@sio.event
def error(data):
    print(f"Error: {data}")

@sio.on('long_session')
def update_ls(data):
    global long_session 
    long_session = data

def callback():
    print('callback called')

class SCMessenger:
    def __init__(self, server="localhost:5000"):
        sio.connect(server)

    def send(self, message):
        sio.emit("message", message)

    def login(self, username, password):
        sio.emit("login", {"username": username, "password": password},callback=callback)

    def register(self, username, password):
        sio.emit("register", {"username": username, "password": password})

    def send_to_user(self, username, message):
        sio.emit("message_user", {"username": username, "message": message})

    def resume(self):
        """
        Resume session using a session id stored locally, if you had logged in
        """
        sio.emit('login',{"long_session":long_session})