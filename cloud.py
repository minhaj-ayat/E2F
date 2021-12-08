import socket


#PROXY_IP = '127.0.0.1'
#PROXY_PORT = 22998

PROXY_IP = '103.94.135.96'
PROXY_PORT = 2000

#CLOUD_IP = ''
#CLOUD_PORT = 11000

CLOUD_IP = '127.0.0.1'
CLOUD_PORT = 33333

clientID_receiving_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientID_receiving_socket.bind((CLOUD_IP, CLOUD_PORT))
clientID_receiving_socket.listen()
while True:
    conn, addr = clientID_receiving_socket.accept()
    print('Connected to client ', addr)

    data = conn.recv(500)
    data = data.decode()
    print('Received data ', data)
    #conn.close()
    userDatabase = open("userDB.txt", "r")
    # 1 for valid 0 for invalid
    #validity_sending_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #validity_sending_socket.connect((PROXY_IP, PROXY_PORT))
    for x in userDatabase:
        print(data ,  "and " , x)
        if x.strip() == data:
            print("Match found")
            conn.send("Valid".encode())
            print("Valid sent")
            break
        else:
            print("No match")
            conn.send("Invalid".encode())
            print("Invalid sent")
