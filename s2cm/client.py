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
        self.server = server
        self.http_session = requests.Session()
        self.token = token
        if self.token:
            self.sio.connect(server, headers={"Authorization": self.token})

        elif token := SCMessenger.login(self.server, username, password):
            self.sio.connect(server, headers={"Authorization": token})

    def send(self, message):
        self.sio.emit("message", message)

    @staticmethod
    def login(server_url: str, username: str, password: str) -> str | None:
        res = requests.post(
            f"{server_url}/login",
            {"username": username, "password": password},
            timeout=30,
        )
        json_res = res.json()
        token = json_res.get("token")
        return token

    @staticmethod
    def register(server: str, username: str, password) -> str | None:
        res = requests.post(
            f"{server}/register",
            {"username": username, "password": password},
            timeout=30,
        )
        json_res = res.json()
        if token := json_res.get("registered"):
            return token

        print("registration failed")

    def send_to_user(self, username, message):
        self.sio.emit("message_user", {"username": username, "message": message})

    def resume(self):
        """
        Resume session using a session id stored locally, if you had logged in
        """
        self.sio.emit("login", {"long_session": long_session})
        
