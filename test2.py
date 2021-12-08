from socket import *

with socket(AF_INET, SOCK_STREAM) as fog_serverSocket:
    fog_serverSocket.bind(("0.0.0.0", 20000))
    fog_serverSocket.listen()

    print('Waiting for connection from test...')
    conn_proxy, addr_proxy = fog_serverSocket.accept()
    with conn_proxy:
        print('Connected to client by ', addr_proxy)
        conn_proxy.send("Hello".encode())
        print("Sent hello to client")
