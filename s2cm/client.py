import socketio

# Create a Socket.IO client
sio = socketio.Client()


@sio.event
def connect():
    print("Connected to the server!")


@sio.event
def disconnect():
    print("Disconnected from the server.")


@sio.event
def response(data):
    print(f"Received from server: {data}")


class SCMessenger:
    def __init__(self, host="localhost", port=5000):
        # Connect to the server
        sio.connect(f"http://{host}:{port}")

    def send(self, message):
        sio.emit("message", message)

    def send_to_user(self, username, message):
        sio.emit("message_user", dict(username=username, message=message))
