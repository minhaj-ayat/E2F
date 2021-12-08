
import datetime
from socket import *
import os
import django
import random
import string

data = '320230100000166'
with socket(AF_INET, SOCK_STREAM) as client_for_mediator:
    if len(data) == 15 and data.isdigit():
        IMSI = int(data)
        client_for_mediator.connect(("34.131.18.106", 20000))
        print("test sent connection request")
        data = client_for_mediator.recv(500)
        print(data.decode())