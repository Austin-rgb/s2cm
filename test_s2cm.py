import random
import string
from threading import Thread
from time import sleep

from s2cm.client import SCMessenger


def random_str(length=10):
    return "".join(random.choices(string.ascii_lowercase, k=10))


print("Testing register")
stop_register = False


def register():
    success = 0
    while not stop_register:
        username = random_str()
        SCMessenger.register("http://localhost:5000", username, username)
        success += 1
    print(f"tested register: {success} completions per second")


t_register = Thread(target=register)
t_register.start()
sleep(1)
stop_register = True
sleep(1)
