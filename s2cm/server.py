import os
import secrets

from flask import Flask, request
from flask_socketio import SocketIO, emit, join_room, leave_room
import json
import bcrypt

from peewee import *
from datetime import datetime

# Initialize the SQLite database (replace 'db.sqlite3' with your DB path if needed)
db = SqliteDatabase("db.sqlite3")


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    username = CharField(unique=True, max_length=50)
    password = CharField(max_length=100)
    sessions = IntegerField(default=0)  # To track the number of sessions for each user

    def set_password(self, raw_password):
        """Hash the password and store it."""
        # Generate a salt and hash the password
        self.password = bcrypt.hashpw(
            raw_password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

    def check_password(self, raw_password):
        """Check a plain password against the stored hashed password."""
        return bcrypt.checkpw(
            raw_password.encode("utf-8"), self.password.encode("utf-8")
        )


class Session(BaseModel):
    sessionId = AutoField()
    created_at = DateTimeField(default=datetime.now)
    user = ForeignKeyField(User, backref="user_sessions", on_delete="CASCADE")


# Create the tables
db.connect()
db.create_tables([User, Session])


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
users = {}
socketio = SocketIO(app, cors_allowed_origins="*")


# Event for joining a room
@socketio.on("join")
def handle_join(data):
    username = data["username"]
    room = data["room"]
    join_room(room)
    emit("message", {"msg": f"{username} has joined the room."}, room=room)


# Event for leaving a room
@socketio.on("leave")
def handle_leave(data):
    username = data["username"]
    room = data["room"]
    leave_room(room)
    emit("message", {"msg": f"{username} has left the room."}, room=room)


# Event for sending a message
@socketio.on("send_message")
def handle_send_message(data):
    room = data["room"]
    message = data["message"]
    emit("message", {"msg": message}, room=room)


@app.route("/")
def index():
    return "WebSocket Server is Running"


@socketio.on("set_username")
def set_username(msg):
    username = msg.get("username")
    password = msg.get("password")
    user = User.create(
        username=username,
    )


@app.route("/send", methods=["POST"])
def send():
    user = request.form.get("username")
    message = request.form.get("message")
    payload = {}
    payload["message"] = message
    payload["user"] = users[request.sid]
    user_http_session = http_sessions.get(user)
    user_sess = ws_sessions.get(user_http_session)
    message = json.dumps(payload)
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
