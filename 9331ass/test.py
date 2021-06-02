# coding: utf-8
from socket import *
import sys
import threading
import re
import time
import datetime


# Define connection (socket) parameters
# Address + Port no
# Server would be running on the same host as Client

class client:
    clientSocket = None
    p2pclient = None
    iflogin = 0
    auth = "Unkonwn"
    tempID = ""
    UserID = ""
    log = ""
    contact_dict = {}
    Lock = None
    temp_array = []

    def __init__(self, server_IP, server_port, p2p_port):
        try:
            self.clientSocket = socket(AF_INET, SOCK_STREAM)
            self.clientSocket.connect((server_IP, server_port))
            print("Success to connect to the server.")
        except:
            print("Fail to connect to the server.")
            exit()
        try:
            self.p2pclient = socket(AF_INET, SOCK_DGRAM)
            self.p2pclient.bind(("127.0.0.1", p2p_port))
            print("Success to create p2p connection.")
        except:
            print("P2P connection fails.")
            exit()

    def login(self):
        self.UserID = input("Username: ")
        password = input("Password: ")
        sentence = self.UserID + ' ' + password
        self.clientSocket.send(sentence.encode())
        auth = self.clientSocket.recv(1024).decode()

        if auth == "success":
            print("Welcome to the BlueTrace Simulator!")
            sentence = "done"
            self.clientSocket.send(sentence.encode())
            self.iflogin = 1

        else:
            while (auth != "success"):
                if auth == "fail":
                    print("Invalid Password. Please try again")
                    password = input("Password: ")
                    sentence = self.UserID + ' ' + password
                    self.clientSocket.send(sentence.encode())
                    auth = self.clientSocket.recv(1024).decode()
                elif auth == "exceed":
                    print("Invalid Password. Your account has been blocked. Please try again later")
                    sentence = "done"
                    self.clientSocket.send(sentence.encode())
                    self.clientSocket.close()
                    self.iflogin = 3
                    break
                elif auth == "waiting":
                    print("Your account is blocked due to multiple login failures. Please try again later")
                    sentence = "done"
                    self.iflogin = 3
                    self.clientSocket.send(sentence.encode())
                    self.clientSocket.close()
                    break
            if auth == "success":
                print("Welcome to the BlueTrace Simulator!")
                sentence = "done"
                self.clientSocket.send(sentence.encode())
                self.iflogin = 1

    def get_tempID(self, command_sentence):
        self.clientSocket.send(command_sentence.encode())
        self.tempID = self.clientSocket.recv(1024).decode()
        print("TempID:")
        print(self.tempID)

    def upload_log(self, command_sentence):
        self.clientSocket.send(command_sentence.encode())
        self.log = ""
        print("Please type your contact_log below. Type \'done\' to finish your input.")
        while (1):
            string = input()
            if string == 'done':
                break
            string += '\n'
            self.log += string
        self.clientSocket.send(self.log.encode())
        string_list = self.log.replace(';', '').split('\n')
        self.temp_array = []  ##id in the input
        for item in string_list:
            id = item.split(',')[0]
            self.temp_array.append(id)
        with open('z5235242_contactlog.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()
            print(lines)
            for line in lines:
                if line:
                    if line.split(' ')[0] in self.temp_array:
                        lines.remove((line)
                        with open('z5235242_contactlog.txt', 'w', encoding='utf-8') as fw:
                            for
                        line in lines:
                        if line:
                            fw.write(line)
                        with open('z5235242_contactlog.txt', 'a', encoding='utf-8') as fa:
                            for
                        record in string_list: \
                            fa.write(record.replace(',', ' ') + '\n')

                        #        with open('z5235242_contactlog.txt','a',encoding='utf-8') as fa:
                        #            for record in string_list:
                        #                fa.write(record.replace(',',' ')+'\n')

    def process_command(self, command, command_sentence):
        if command == 'Download_tempID':
            self.get_tempID(command_sentence)
        elif command == 'Upload_contact_log':
            self.upload_log(command_sentence)
        elif command == 'logout':
            self.clientSocket.send(command_sentence.encode())
            print("Logout from the server.\n")
            self.iflogin = 0
        else:
            print("Invalid command.\n")

    def send_beacon(self, destIP, destPort):
        c_time = datetime.datetime.now()
        start_time = c_time.strftime("%d/%m/%Y %H:%M:%S")
        end_time = (c_time + datetime.timedelta(minutes=15) - datetime.timedelta(seconds=1)).strftime(
            "%d/%m/%Y %H:%M:%S")
        version = 1.0
        message = self.tempID + ',' + start_time + ',' + end_time + ',' + str(version)
        print(self.tempID + ',' + start_time + ',' + end_time + '.')
        print("p2p send: ", message)
        self.p2pclient.sendto(message.encode(), (destIP, destPort))

    def get_beacon(self):
        while True:
            message, p2p_addr = self.p2pclient.recv(1024)
            message = message.decode()
            c_time = datetime.datetime.now()
            start_time = message.split(',')[1]
            end_time = message.split(',')[2]
            print("recevied beacon:")
            print(message)
            print("Current time is:")
            print(c_time.strftime("%d/%m/%Y %H:%M:%S"))
            if c_time > start_time.strptime("%d/%m/%Y %H:%M:%S") and c_time <= end_time.strptime("%d/%m/%Y %H:%M:%S"):
                print("The beacon is valid.")
                self.contact_dict[message.split(',')[0]] = start_time + ',' + end_time
                self.Lock.acquire()
                with open('z5235242_contactlog.txt', 'a') as f:
                    f.write(message + '\n')
                    self.Lock.release()
            else:
                print("The beacon is invalid.")

    def del_beacon(self):
        c_time = datetime.datetime.now()
        self.Lock.acquire()
        with open('z5235242_contactlog.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines
        with open('z5235242_contactlog.txt', 'w', encoding='utf-8') as fw:
            for line in lines:
                if line:
                    end_time = line.split(' ')[-2] + ' ' + line.split(' ')[-1].replace('\n', '')
                    start_time = line.split(' ')[-4] + ' ' + line.split(' ')[-3].replace('\n', '')
                    if c_time < datetime.datetime.strptime(end_time,
                                                           "%d/%m/%Y %H:%M:%S") or c_time > datetime.datetime.strptime(
                            start_time, "%d/%m/%Y %H:%M:%S"):
                        continue
                    fw.write(line)
                    self.Lock.release()

    def main(self):
        p2p_client_thread = threading.Thread(target=self.get_beacon)
        p2p_client_thread.daemon = True
        p2p_client_thread.start()
        self.login()
        while (self.iflogin == 1):
            command = input()
            command_sentence = command + ' ' + self.UserID
            if command.split(' ')[0] == 'Beacon':
                if re.match(r"Beacon (\d+\.\d+\.\d+\.\d+) (\d+)", command):
                    destIP = command.split(' ')[1]
                    destPort = command.split(' ')[2]
                    self.send_beacon(destIP, destPort)
                else:
                    print("Invalid command.\n")
            else:
                self.process_command(command, command_sentence)
        self.clientSocket.close()


server_IP = sys.argv[1]
server_port = int(sys.argv[2])
p2p_port = int(sys.argv[3])
client(server_IP, server_port, p2p_port).main()















