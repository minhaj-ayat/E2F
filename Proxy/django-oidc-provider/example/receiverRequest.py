import datetime
from socket import *
import os
import django
import random
import string
import requests

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

from django.contrib.auth.models import User

#MEDIATOR_IP = '127.0.0.1'
#MEDIATOR_SERVER_PORT = 33333

MEDIATOR_IP = '34.131.18.106'
MEDIATOR_SERVER_PORT = 11000

PROXY_IP = '127.0.0.1'
PROXY_SERVER_PORT = 11000

FOG_IP = '127.0.0.1'
FOG_SERVER_PORT = 21000  # the client_for_fog socket will connect at this port

IMSI = 320230100000025

def random_char(y):
    return ''.join(random.choice(string.ascii_letters) for x in range(y))


def deleteUser():
    userFile = open('myUser.txt', 'r')
    line = userFile.readline()
    line = line.split(' ')
    if User.objects.filter(username=line[0]).exists():
        user = User.objects.get(username=line[0])
        user.delete()
    userFile.close()


with socket(AF_INET, SOCK_STREAM) as server_for_fog:
    server_for_fog.bind((PROXY_IP, PROXY_SERVER_PORT))
    server_for_fog.listen()

    # Waiting for connection from Fog/OIDC client
    while True:
        print('Waiting to receive IMSI from fog...')
        conn_fog, addr_fog = server_for_fog.accept()
        with conn_fog:
            print('Connected to fog by ', addr_fog)
            while True:
                data = conn_fog.recv(200)
                if not data:
                    break
                else:
                    data = data.decode('utf-8')
                    print('Proxy received data from Foreign fog : ' + data + "-- at time : ")
                    print(datetime.datetime.now())
                    # Connect to mediator
                    compareResponse = ''
                    with socket(AF_INET, SOCK_STREAM) as client_for_mediator:
                        if len(data) == 15 and data.isdigit():
                            IMSI = int(data)
                            client_for_mediator.connect((MEDIATOR_IP, MEDIATOR_SERVER_PORT))
                            client_for_mediator.sendall(data.encode())
                            print("Proxy sent data to mediator at time : ")
                            print(datetime.datetime.now())

                            #client_for_mediator.close()
                            isvalid = client_for_mediator.recv(500)
                            print("Proxy received msg from mediator: ", isvalid.decode())
                            print("at time : ")
                            print(datetime.datetime.now())

                            deleteUser()
                            userName = random_char(3)
                            email = random_char(3) + "@" + random_char(5) + ".com"
                            password = random.randint(10000, 20000)
                            newUser = User.objects.create_superuser(userName, email, str(password))
                            print("Sending req at time:")
                            print(datetime.datetime.now())
                            req = requests.get(url='http://34.131.18.106:45999/clickCount',
                                               params={'imsi': IMSI})
                            print("Recieved json at time:")
                            print(datetime.datetime.now())
                            data = req.json()
                            print("Data---", data)
                            newUser.first_name = data['clicks']
                            newUser.save()
                            userFile = open('myUser.txt', 'w')
                            userFile.write(userName + ' ' + email + ' ' + str(password))
                            userFile.close()
                            compareResponse = '200 OK'
                        with socket(AF_INET, SOCK_STREAM) as client_for_fog:
                            client_for_fog.connect((FOG_IP, FOG_SERVER_PORT))
                            client_for_fog.sendall(compareResponse.encode())
                            print("Proxy sent response to Foreign fog at time : ")
                            print(datetime.datetime.now())
                            client_for_fog.close()

                        '''else:
                            vectorFile = open('authVectors.txt', 'r')
                            line = vectorFile.readline()
                            line = line.split(' ')
                            compareResponse = '404 Error'
                            #if data == line[0]:
                            deleteUser()
                            userName = random_char(3)
                            email = random_char(3) + "@" + random_char(5) + ".com"
                            password = random.randint(10000, 20000)
                            newUser = User.objects.create_superuser(userName, email, str(password))
                            print("Before req")
                            req = requests.get(url='http://34.131.18.106:45999/clickCount',
                                               params={'imsi': IMSI})
                            data = req.json()
                            print("Data---",data)
                            newUser.first_name = data['clicks']
                            newUser.save()
                            userFile = open('myUser.txt', 'w')
                            userFile.write(userName + ' ' + email + ' ' + str(password))
                            userFile.close()
                            compareResponse = '200 OK'
                        with socket(AF_INET, SOCK_STREAM) as client_for_fog:
                            client_for_fog.connect((FOG_IP, FOG_SERVER_PORT))
                            client_for_fog.sendall(compareResponse.encode())
                            print("Proxy sent response to Foreign fog at time : ")
                            print(datetime.datetime.now())
                            client_for_fog.close()'''
