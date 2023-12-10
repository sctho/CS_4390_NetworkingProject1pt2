from socket import *
import time

serverName = 'localhost'
serverPort = 11235

#long message for testing
longMsg = """
If debugging is the process of removing software bugs, 
then programming must be the process of putting them in.
― Edsger W. Dijkstra

Your obligation is that of active participation. 
You should not act as knowledge-absorbing sponges, 
but as whetstones on which we can all sharpen our wits 
― Edsger W. Dijkstra

Sometimes it pays to stay in bed on Monday, 
rather than spending the rest of the week debugging Monday’s code.
― Dan Salomon

If carpenters made buildings the way programmers make programs, 
the first woodpecker to come along would destroy all of civilization.
― Unknown
"""
#general test case
#longMsg = """ 
#The quick brown fox jumped over the lazy dog.
#"""
#checksum test case
#longMsg = """ 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#"""
#checksum test case
#longMsg = """ 
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#"""

packetSize = 10
packets = []

for i in range(0, len(longMsg), packetSize):
    subStr = longMsg[i:i+packetSize]
    packets.append(subStr)

clientSocket = socket(AF_INET, SOCK_DGRAM)

clientSocket.settimeout(2)
sequenceNumber = 0

for t in range(0, len(packets)):

    checkSum = sum([ord(c) for c in packets[t]])
    checkSum = checkSum % 256
    packets[t] = packets[t] + f"{sequenceNumber}"

    if checkSum <= 9:
        packets[t] = packets[t] + '00' + f"{checkSum}"
    elif checkSum <= 99:
        packets[t] = packets[t] + '0' + f"{checkSum}"
    else:
        packets[t] = packets[t] + f"{checkSum}"

    clientSocket.sendto(packets[t].encode(), (serverName, serverPort))
    ack_confirm = False
    while not ack_confirm:
        try:
            ack, _ = clientSocket.recvfrom(1000)
            if ack == f'ACK{sequenceNumber}'.encode():
                ack_confirm = True
                sequenceNumber = 1 - sequenceNumber
        except timeout:
            clientSocket.sendto(packets[t].encode(), (serverName, serverPort))
            print("Timeout")

# implement reliability here, the below commands are for reference only on how to send and receive using UDP
if sequenceNumber == 1:
    resetMessage = "ResetVal"
    clientSocket.sendto(resetMessage.encode(), (serverName, serverPort))
clientSocket.close()