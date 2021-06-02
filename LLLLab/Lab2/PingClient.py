#python version: python 3.7
import time
from socket import *
import sys

serverName = sys.argv[1]
serverPort = int(sys.argv[2])
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(0.6)
l_rtt=[]
sum_rtt=0
num_rtt=0
for i in range(3331,3346):
    sendtime = time.time()
    message = ('PING %d %s\r\n' % (i, time.asctime(time.localtime(sendtime)))).encode()
    try:
        clientSocket.sendto(message, (serverName, serverPort))
        modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
        rtt = (time.time()-sendtime)*1000
        l_rtt.append(int(rtt))
        sum_rtt+=rtt
        num_rtt+=1
        print('ping to %s, seq = %d, rtt = %d ms' % (serverName, i, rtt))
    except Exception as e:
        print('ping to %s, seq = %d, time out' % (serverName, i))

print('rtt min/avg/max = %d/%d/%d ms' % (min(l_rtt), (sum_rtt/num_rtt),max(l_rtt)))


clientSocket.close()
