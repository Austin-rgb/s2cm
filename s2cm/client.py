"""
Python client module for s2cm.server
"""

import requests
import socketio

# Create a Socket.IO client

long_session = None

def callback():
    print("callback called")


class SCMessenger:
    def __init__(
        self, server="http://localhost:5000", token=None, username=None, password=None
    ):
        self.sio=socketio.Client()
        self.sio.on('connect',self.on_connect)
        self.sio.on('disconnect',self.on_disconnected)
        self.server = server
        self.http_session = requests.Session()
        self.token = token
        if self.token:
            self.sio.connect(server, headers={"Authorization": self.token},transports=['websocket'])

        elif token := SCMessenger.login(self.server, username, password):
            self.sio.connect(server, headers={"Authorization": token},transports=['websocket'])

    def send(self, message):
        self.sio.emit("message", message)

    def conversation(self,peer):
        return Conversation(self.sio,peer)

    @staticmethod
    def login(server_url: str, username: str, password: str) -> str | None:
        res = requests.post(
            f"{server_url}/login",
            {"username": username, "password": password},
            timeout=30,
        )
        
        json_res = res.json()
        token = json_res.get("token")
        error = json_res.get('error')
        if token:
            return token
        else:
            raise RuntimeError(error)

    @staticmethod
    def register(server: str, username: str, password) -> str | None:
        res = requests.post(
            f"{server}/register",
            {"username": username, "password": password},
            timeout=30,
        )
        json_res = res.json()
        if token := json_res.get("token"):
            return token
        else:
            raise RuntimeError(json_res.get('error'))


    def send_to_user(self, username, message):
        self.sio.emit("message_user", {"username": username, "message": message})

    def resume(self):
        """
        Resume session using a session id stored locally, if you had logged in
        """
        self.sio.emit("login", {"long_session": long_session})

    def on_connect(self):
        print('connected')

    def on_disconnected(self):
        print('disconnected')
        
class Conversation:
    def __init__(self,sio:socketio.Client,peer):
        self.peer = peer
        self.sio = sio
        self.sio.on('private_message',self.on_msg)

    def send(self,message):
        self.sio.emit('message_user',{'username':self.peer,'message':message})
    
    def on_message(self,message):
        print('received',message)

    def on_msg(self,data):
        peer = data['from']
        message = data['message']
        print('received',message)
        if peer==self.peer:
            self.on_message(message)

