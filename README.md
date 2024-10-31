# s2cm
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
messager = SCMessenger(server_url)

# register
messager.register("username1","password1")

# login
messenger.login("username1","password1")
```

- connecting client two
```python
from s2cm.client import SCMessenger

server_url = "http://localhost:5000" # replace with the address of your server 
messager = SCMessenger(server_url)

# register
messager.register("username2","password2")

# login
messenger.login("username2","password2")

# once client 1 is connected client 2 can message her
messenger.send("username1","hi")
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
