from .client import SCMessenger
import random, string
rs = lambda :''.join(random.choices(string.ascii_letters,k=10))

u1 = rs()
u2 = rs()
p1 = rs()
p2 = rs()

token1=SCMessenger.register('http://localhost:5000',u1,p1)
if token1:
    print('registration works')
SCMessenger.register('http://localhost:5000',u2,p2)

s1 = SCMessenger(token=token1)
print('token login works')
s2 = SCMessenger(username=u2,password=p2)
print('username/password login works')

msg = rs()
def on_message(message):
    if message==msg:
        print('peer to peer messaging works')

    else:
        print('peer to peer messaging failed')

conv1=s2.conversation(u1)
conv2=s1.conversation(u2)
conv2.on_message=on_message
conv1.send(msg)

s1.sio.wait()

