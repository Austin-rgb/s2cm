import json
import os
import secrets
import traceback

import bcrypt
from flask import Flask, request, render_template
from flask_socketio import SocketIO, emit, join_room, leave_room
from peewee import *

# Initialize the SQLite database (replace 'db.sqlite3' with your DB path if needed)
db = SqliteDatabase("db.sqlite3")


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    username = CharField(unique=True, max_length=50)
    password = CharField(
        max_length=100,
    )
    session = CharField(max_length=32, null=True)
    long_session = CharField(max_length=64, null=True)

    @staticmethod
    def set_password(raw_password:str):
        """Hash the password and store it."""
        # Generate a salt and hash the password
        return bcrypt.hashpw(raw_password.encode("utf-8"), bcrypt.gensalt()).decode(
            "utf-8"
        )

    def check_password(self, raw_password:str):
        """Check a plain password against the stored hashed password."""
        return bcrypt.checkpw(raw_password.encode('utf-8'), bytes(self.password,'utf-8'))



# Create the tables
db.connect()
db.create_tables(
    [
        User,
    ]
)


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


active_users = {}
socketio = SocketIO(app, cors_allowed_origins="*")


# Event for joining a room
@socketio.on("join")
def handle_join(data):
    username = active_users.get(request.sid)
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
    return render_template('index.html')


@socketio.on("register")
def set_username(msg):
    username = msg.get("username")
    password = msg.get("password")
    try:
        user = User.create(username=username, password=User.set_password(password))
        user.save()

    except Exception as e:
        print(e)


@socketio.on("login")
def login(msg):
    username = msg.get("username")
    password = msg.get("password")
    long_session = msg.get('long_session')

    if username and password:
        try:
            user = User.get(username=username)
            if user.check_password(password):
                user.session = request.sid
                generated_session = secrets.token_hex(96)
                user.long_session = generated_session
                user.save()
                emit('long_session',generated_session)
                print(user.username,'logged in successfully')
            else:
                print(username,'login password failed')

        except Exception as e:
            emit("error", str(e))
            traceback.print_exception(e)

    elif long_session:
        try:
            user = User.get(long_session=long_session)
            user.session = request.sid
            user.save()
            print(user.username,'logged in successfully')

        except Exception as e:
            emit("error", str(e))
            traceback.print_exception(e)
    
    else:
        if password:
            print(f'login failed with no-username')

        else:
            print(f'login failed with username: {username}')


@socketio.on("message_user")
def send(msg):
    username = msg.get("username")
    message = msg.get("message")
    payload = {}
    payload["message"] = message
    this_user = User.get(session=request.sid)
    payload["from"] = this_user.username
    try:
        user = User.get(username=username)
        socketio.emit("response", payload, to=user.session)
        print(f'sent message: {message}, to: {username}')
    except Exception as e:
        emit("error", str(e))


@socketio.on("messag_group")
def message_group(data):
    group = data.get("group")
    msg = data.get("message")
    emit("message", msg, to=group)


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
    emit('message',msg)


@socketio.on("disconnect")
def handle_disconnect():
    # Remove the session ID from user_sessions if needed
    print(f"WebSocket disconnected: {request.sid}")


def run(host=HOST, port=PORT):
    """
    Run s2cm server
    """
    socketio.run(app, host=host, port=port, debug=True)


if __name__ == "__main__":
    run()
