"""
Python client module for s2cm.server
"""

import socketio
import requests

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


def callback():
    print("callback called")


class SCMessenger:
    def __init__(
        self, server="http://localhost:5000", token=None, username=None, password=None
    ):
        self.server = server
        self.http_session = requests.Session()
        self.token = token
        if self.token:
            sio.connect(server, headers={"Authorization": self.token})

        elif self.login(username, password):
            sio.connect(server, headers={"Authorization": self.token})

    def send(self, message):
        sio.emit("message", message)

    def login(self, username, password):
        res = self.http_session.post(
            f"{self.server}/login", {"username": username, "password": password}
        )
        json_res = res.json()
        self.token = json_res.get("token")
        return self.token

    @staticmethod
    def register(server: str, username: str, password):
        res = requests.post(
            f"{server}/register",
            {"username": username, "password": password},
            timeout=30,
        )
        json_res = res.json()
        if token := json_res.get("token"):
            return token

        else:
            print("registration failed")

    def send_to_user(self, username, message):
        sio.emit("message_user", {"username": username, "message": message})

    def resume(self):
        """
        Resume session using a session id stored locally, if you had logged in
        """
        sio.emit("login", {"long_session": long_session})
