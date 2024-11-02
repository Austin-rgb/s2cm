# s2cm
[![Dependabot Updates](https://github.com/Austin-rgb/s2cm/actions/workflows/dependabot/dependabot-updates/badge.svg)](https://github.com/Austin-rgb/s2cm/actions/workflows/dependabot/dependabot-updates)

![logo](https://github.com/Austin-rgb/s2cm/blob/main/Screenshot_20241030_213712_Chrome.jpg)

Server to client messenger for notifying users in a client server model
## Installation 
you can install latest stable via pip
```sh
pip install s2cm
```

For latest release, you can install from github
```sh
git clone https://github.com/Austin-rgb/s2cm.git
cd s2cm
pip install .
```

## Usage
### start the server
```python
from s2cm.server import socketio, app
socketio.run(app,port=5000)
```
### connect from client 
For demonstration we connect 2 python clients
- connecting client one
```python
from s2cm.client import SCMessenger

server_url = "http://localhost:5000" # replace with the address of your server 

# register
SCMessenger.register("username1","password1")

# login
messenger = SCMessenger(server_url, username="username1",password="password1")

# Message user2
messenger.send("username2", "hi")
```

- connecting client two
```python
from s2cm.client import SCMessenger

server_url = "http://localhost:5000" # replace with the address of your server 

# register
SCMessenger.register("username2","password2")

# login
messenger = SCMessenger(server_url, username="username2",password="password2")

# once client 1 is connected client 2 can message her
messenger.send("username1","hi too")
```

### Usage in javascript (web page) 
s2cm can be accessed with javascript in a web page 
Once your server is running 
```html
<script src="http://localhost:5000/static/s2cm.client.min.js"></script>
<script>
const client=s2cm_client("http://localhost:5000")
client.emit("register",{"username":"username1","password":"password1"}
client.emit("login",{"username":"username1","password":"password1"}
client.emit("message_user",{"username":"username2","message":"Hi there"}) 
</script>
```
