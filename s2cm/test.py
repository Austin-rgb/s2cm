from .client import SCMessenger
import random, string
rs = lambda :''.join(random.choices(string.ascii_letters,k=10))

u1 = rs()
u2 = rs()
p1 = rs()
p2 = rs()

SCMessenger.register('http://localhost:5000',u1,p1)
SCMessenger.register('http://localhost:5000',u2,p2)

s1 = SCMessenger(username=u1,password=p1)
s2 = SCMessenger(username=u2,password=p2)

msg = rs()
def handle(data):
    message = data['message']
    if message==msg:
        print('peer to peer messaging works')

    else:
        print('peer to peer messaging failed')
s1.sio.on('private_message',handle)
s2.send_to_user(u1,msg)
s2.sio.wait()
