"""
S2cm
Server to client messenger 
A small python code to help you notify or message your clients from the server
"""

import os
import secrets
import traceback
import pathlib

import bcrypt
from flask import Flask, request, render_template, redirect
from flask_socketio import SocketIO, emit, join_room, leave_room
from peewee import SqliteDatabase, Model, CharField, DoesNotExist


# Initialize the SQLite database (replace 'db.sqlite3' with your DB path if needed)
S2CM_HOME = os.sep.join([str(pathlib.Path.home()), ".s2cm"])
os.makedirs(S2CM_HOME, exist_ok=True)
db = SqliteDatabase(os.sep.join([S2CM_HOME, "s2cm.sqlite3"]))


class BaseModel(Model):
    """
    Base class for providing the database instance
    """

    class Meta:
        """Expose the database instance to be used"""

        database = db


class User(BaseModel):
    """Orm class for s2cm user"""

    username = CharField(unique=True, max_length=50)
    password = CharField(
        max_length=100,
    )
    session = CharField(max_length=32, null=True)
    long_session = CharField(max_length=64, null=True)

    @staticmethod
    def set_password(raw_password: str):
        """Hash the password and store it."""
        # Generate a salt and hash the password
        return bcrypt.hashpw(raw_password.encode("utf-8"), bcrypt.gensalt()).decode(
            "utf-8"
        )

    def check_password(self, raw_password: str):
        """Check a plain password against the stored hashed password."""
        return bcrypt.checkpw(
            raw_password.encode("utf-8"), bytes(self.password, "utf-8")
        )


# Create the tables
db.connect()
db.create_tables(
    [
        User,
    ]
)


def _using_default(name: str, value):
    print(
        f"""
using default {name}: {value}
You can modify by doing "export {name.capitalize()}=[your.prefered.{name}]"'
  
"""
    )


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
    """Adds user to a room"""
    username = active_users.get(request.sid)
    room = data["room"]
    join_room(room)
    emit("message", {"msg": f"{username} has joined the room."}, room=room)


# Event for leaving a room
@socketio.on("leave")
def handle_leave(data):
    """Remove user from a room"""
    username = data["username"]
    room = data["room"]
    leave_room(room)
    emit("message", {"msg": f"{username} has left the room."}, room=room)


@app.route("/")
def index():
    """S2cm http home page"""
    return render_template("index.html")


@app.route("/register", methods=["POST"])
def set_username():
    """Register user"""
    username = request.form.get("username")
    password = request.form.get("password")
    try:
        user = User.create(username=username, password=User.set_password(password))
        user.save()
        return {'registered':True}

    except DoesNotExist as e:
        print(e)


@app.route("/login", methods=["POST"])
def login():
    """Create a session for user"""
    username = request.form.get("username")
    password = request.form.get("password")

    if username and password:
        try:
            user = User.get(username=username)
            if user.check_password(password):
                generated_session = secrets.token_hex(96)
                user.long_session = generated_session
                user.save()
                print(user.username, "logged in successfully")
                return {"token": generated_session}
            else:
                print(username, "login password failed")

        except DoesNotExist as e:
            emit("error", str(e))
            traceback.print_exception(e)

    else:
        if password:
            print("login failed with no-username")

        else:
            print(f"login failed with username: {username}")

        return "Failed"


@socketio.on("message_user")
def send(msg):
    """Send a message from one user to another"""
    username = msg.get("username")
    message = msg.get("message")
    payload = {}
    payload["message"] = message
    this_user = User.get(session=request.sid)
    payload["from"] = this_user.username
    try:
        user = User.get(username=username)
        socketio.emit("response", payload, to=user.session)
        print(f"sent message: {message}, to: {username}")
    except DoesNotExist as e:
        emit("error", str(e))


@socketio.on("message_group")
def message_group(data):
    """Message a group of users"""
    group = data.get("group")
    msg = data.get("message")
    emit("message", msg, to=group)


@socketio.on("connect")
def handle_connect():
    """Called when a user is connect"""
    long_session = request.headers.get("Authorization")
    print("token:", long_session)
    if long_session:
        try:
            user = User.get(long_session=long_session)
            user.session = request.sid
            user.save()
            print(user.username, "logged in successfully")

        except DoesNotExist as e:
            emit("error", str(e))
            traceback.print_exception(e)


@socketio.on("message")
def handle_message(msg):
    """Handle 'message' event"""
    emit("message", msg)


@socketio.on("disconnect")
def handle_disconnect():
    """TODO"""


if __name__ == "__main__":
    HOST = os.environ.get("HOST")
    if not HOST:
        HOST = "127.0.0.1"
        _using_default("host", HOST)

    PORT = os.environ.get("PORT")
    if not PORT:
        PORT = 5000
        _using_default("port", PORT)

    socketio.run(app, host=HOST, port=PORT)
