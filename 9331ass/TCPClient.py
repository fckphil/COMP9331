# coding: utf-8
from socket import *
import sys

# Define connection (socket) parameters
# Address + Port no
# Server would be running on the same host as Client
server_IP = sys.argv[1]
server_port = int(sys.argv[2])
# clinet_udp_port = int(sys.argv[3])


clientSocket = socket(AF_INET, SOCK_STREAM)

clientSocket.connect((server_IP, server_port))

UserID = input("Username: ")
password = input("Password: ")
sentence = UserID + ' ' + password

clientSocket.send(sentence.encode())

auth = clientSocket.recv(1024).decode()
if auth == "success":
    print("Welcome to the BlueTrace Simulator!")
    sentence = "done"
    clientSocket.send(sentence.encode())

else:
    while (auth != "success"):
        if auth == "fail":
            print("Invalid Password. Please try again")
            password = input("Password: ")
            sentence = UserID + ' ' + password
            clientSocket.send(sentence.encode())
            auth = clientSocket.recv(1024).decode()
        elif auth == "exceed":
            print("Invalid Password. Your account has been blocked. Please try again later")
            sentence = "done"
            clientSocket.send(sentence.encode())
            clientSocket.close()
            break
        elif auth == "waiting":
            print("Your account is blocked due to multiple login failures. Please try again later")
            sentence = "done"
            clientSocket.send(sentence.encode())
            clientSocket.close()
            break
    if auth == "success":
        print("Welcome to the BlueTrace Simulator!")
        sentence = "done"
        clientSocket.send(sentence.encode())

while True:
    command = input("Please input a command: ")
    command_sentence = command + ' ' + UserID

    if command == 'Download_tempID':
        clientSocket.send(command_sentence.encode())
        tempID = clientSocket.recv(1024).decode()
        print("TempID:")
        print(tempID)


    elif command == 'Upload_contact_log':
        clientSocket.send(command_sentence.encode())
        log = ""
        print("Please type your contact_log below. Type \'done\' to finish your input.")
        while (1):
            string = input()
            if string == 'done':
                break
            string += '\n'
            log += string
        clientSocket.send(log.encode())





    elif command == 'logout':
        clientSocket.send(command_sentence.encode())


    else:
        print("Invalid command.\n")



