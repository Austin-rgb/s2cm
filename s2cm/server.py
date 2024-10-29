from flask import Flask, request
from flask_socketio import SocketIO, emit
import os
import secrets


def _using_default(name, value):
    print(
        f'using default {name}: {value}\n You can modify by doing "export {name}=[your.prefered.{name}]"'
    )


HOST = os.environ.get("HOST")
if not HOST:
    HOST = "127.0.0.1"
    _using_default("host", HOST)

PORT = os.environ.get("PORT")
if not PORT:
    PORT = 5000
    _using_default("port", PORT)

SECRET_KEY = os.environ.get("SECRET_KEY")
if not SECRET_KEY:
    SECRET_KEY = secrets.token_hex(32)


app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY

http_sessions = {}
ws_sessions = {}
socketio = SocketIO(app, cors_allowed_origins="*")


@app.route("/")
def index():
    return "WebSocket Server is Running"


@app.route("/send", methods=["POST"])
def send():
    user = request.form.get("username")
    message = request.form.get("message")
    user_http_session = http_sessions.get(user)
    user_sess = ws_sessions.get(user_http_session)
    socketio.emit("message", message, to=user_sess)
    return "True"


@socketio.on("connect")
def handle_connect():
    username = request.args.get("username")

    print(f"WebSocket connected: {username} with session ID: {request.sid}")
    emit(
        "response",
        {"message": f"Connected to the WebSocket server! Your username is {username}"},
    )


@socketio.on("message")
def handle_message(msg):
    print(f"Received message from {request.sid}: {msg}")


@socketio.on("set_ws")
def set_http_sess(data):
    http_sess = data.get("http_sess")
    ws_sessions[http_sess] = request.sid
    print(f"set_ws; {http_sess}:{request.sid}")


@app.route("/set_username", methods=["POST"])
def set_username():
    username = request.form.get("username")
    http_sess = request.form.get("session")
    http_sessions[username] = http_sess
    result = f"username:{username},http_sess:{http_sess}"
    print(result)
    return result


@socketio.on("disconnect")
def handle_disconnect():
    # Remove the session ID from user_sessions if needed
    print(f"WebSocket disconnected: {request.sid}")


def run(host=HOST, port=PORT):
    socketio.run(app, host=host, port=port)


if __name__ == "__main__":
    run()
