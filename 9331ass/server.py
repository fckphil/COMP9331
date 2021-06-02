import sys
from socket import *
import threading
server_port =int(sys.argv[1])
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('127.0.0.1', server_port))
serverSocket.listen(5)
print('ready')
dict = {}

def save(connectionSocket, addr):
    b = '127.0.0.1'
    dict[addr[0]] = connectionSocket
    print(dict)


while True:
    connectionSocket, addr = serverSocket.accept()
    connect_thread = threading.Thread(target=save, args=(connectionSocket, addr))
    connect_thread.daemon = True
    connect_thread.start()


12345678901234567891,13/05/2020 17:54:06,13/05/2020 18:09:05;
12345678901234567892,14/05/2020 17:54:06,14/05/2020 18:09:05;
12345678912345678900,14/05/2020 17:54:06,14/05/2020 18:09:05;

12345678901234567891,13/05/2020 17:45:06,13/05/1020 18:00:05;
12345678901234567892,14/05/2020 17:54:06,14/05/1020 18:09:05;
12345678912345678902,14/05/2020 17:54:06,14/05/1020 18:09:05;

12345678901234567891 13/05/2020 17:54:06 13/05/2020 18:09:05
12345678901234567892 14/05/2020 17:54:06 14/05/2020 18:09:05
12345678912345678900 14/05/2020 17:54:06 14/05/2020 18:09:05