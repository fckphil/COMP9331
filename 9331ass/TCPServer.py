# coding: utf-8
from socket import *
import sys
import time
import threading
import random
import datetime

# using the socket module

# Define connection (socket) parameters
# Address + Port no
# Server would be running on the same host as Client
# change this port number if required
server_port = int(sys.argv[1])
block_duration = int(sys.argv[2])
check = []
block = {}
array_of_user = []

with open("credentials.txt", "r", encoding="utf-8") as f:
    for line in f:
        check.append(line.replace('\n', ''))
        array_of_user.append(line.replace('\n', '').split(' ')[0])

serverSocket = socket(AF_INET, SOCK_STREAM)
# This line creates the server’s socket. The first parameter indicates the address family; in particular,AF_INET indicates that the underlying network is using IPv4.The second parameter indicates that the socket is of type SOCK_STREAM,which means it is a TCP socket (rather than a UDP socket, where we use SOCK_DGRAM).

serverSocket.bind(('127.0.0.1', server_port))
# The above line binds (that is, assigns) the port number 12000 to the server’s socket. In this manner, when anyone sends a packet to port 12000 at the IP address of the server (localhost in this case), that packet will be directed to this socket.

serverSocket.listen(3)
# The serverSocket then goes in the listen state to listen for client connection requests.

print("The server is ready to receive")


def login(connectionSocket, addr):
    global check
    global array_of_user
    global block
    wrong_time = 0

    sentence = connectionSocket.recv(1024).decode()
    auth = "unknown"
    UserID = sentence.split(' ')[0]
    password = sentence.split(' ')[1]
    while (sentence != "done"):
        if UserID in block.keys():
            time_now = time.time()
            if (time_now - int(block[UserID])) < block_duration:
                auth = "waiting"
            else:
                del block[UserID]
                auth = "unknown"
        if auth != "waiting":
            if UserID not in array_of_user:
                with open('credentials.txt', 'a', encoding='utf-8') as f:
                    f.write("\n" + sentence)
                    f.close
                check.append(sentence)
                array_of_user.append(UserID)
                auth = "success"
            else:
                if sentence in check:
                    auth = "success"
                    wrong_time = 0
                else:
                    wrong_time += 1
                    if wrong_time < 3:
                        auth = "fail"
                    else:
                        auth = "exceed"
                        block[UserID] = time.time()
                        wrong_time = 0

        connectionSocket.send(auth.encode())
        sentence = connectionSocket.recv(1024).decode()

        ##12345678901234567891,13/05/2020 17:54:06,13/05/2020 18:09:05;
        ##12345678901234567892,14/05/2020 17:54:06,14/05/2020 18:09:05;
    while True:
        command_sentence = connectionSocket.recv(1024).decode()
        command = command_sentence.split(' ')[0]
        command_id = command_sentence.split(' ')[1]
        if command == 'logout':
            print(command_id, ' logout.\n')
            break;
        else:
            id_dict = {}
            update_tid()
            tid_exist = []
            with open("tempIDs.txt", "r", encoding="utf-8") as f:
                for line in f:
                    if line:
                        id_dict[line.split(' ')[0]] = line.split(' ')[1]  ##key:uid value:tempid
                        tid_exist.append(line.split(' ')[1])
            if command_id not in id_dict.keys():
                with open("tempIDs.txt", "a", encoding="utf-8") as f:
                    id = command_id
                    while 1:
                        tid = ''.join(str(random.choice(range(10))) for _ in range(20))
                        if tid not in tid_exist:
                            tid_exist.append(tid)
                            id_dict[command_id] = tid
                            break
                    start_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    end_time = (datetime.datetime.now() + datetime.timedelta(minutes=15) - datetime.timedelta(
                        seconds=1)).strftime("%d/%m/%Y %H:%M:%S")
                    sentence = id + ' ' + tid + ' ' + start_time + ' ' + end_time + '\n'
                    f.write(sentence)

            if command == "Download_tempID":
                print("user: ", command_id)
                print("TempID:", id_dict[command_id])
                connectionSocket.send(id_dict[command_id].encode())
            elif command == "Upload_contact_log":
                rev_id_dict = {v: k for k, v in id_dict.items()}  ##key:tempid value:uid
                print(rev_id_dict)
                new_log = connectionSocket.recv(1024).decode()
                new_log = new_log.split('\n')

                print("received contact log from ", command_id)
                for i in new_log:
                    if i:
                        print(i)

                print("\nContact log checking")

                for i in new_log:
                    if i:
                        i = i.split(',')
                        if i[0] in rev_id_dict.keys():
                            print(rev_id_dict[i[0]], ", ", i[1], ", ", i[0], ";")
                        else:
                            print("UserID not found, ", i[1], ",", i[0], ";")


def update_tid():
    c_time = datetime.datetime.now()
    with open('tempIDs.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    with open('tempIDs.txt', 'w', encoding='utf-8') as fw:
        for line in lines:
            if line:
                end_time = line.split(' ')[-2] + ' ' + line.split(' ')[-1].replace('\n', '')
                if c_time > datetime.datetime.strptime(end_time, "%d/%m/%Y %H:%M:%S"):
                    continue
                fw.write(line)


while True:
    connectionSocket, addr = serverSocket.accept()
    connect_thread = threading.Thread(target=login, args=(connectionSocket, addr))
    connect_thread.daemon = True
    connect_thread.start()

