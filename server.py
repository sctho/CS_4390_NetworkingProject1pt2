from socket import *
serverPort = 11235
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
print ("The server is ready to receive")

ackNumber = 0
TimeoutCalls = 0
while True:
  # implement reliablity in this loop, the below commands are for reference only on how to send and receive using UDP
  message, clientAddress = serverSocket.recvfrom(1024)
  packet = message.decode()
  if packet == "ResetVal":
    ackNumber = 0
  else:
    pktNum = packet[-4]

    checkSum = sum([ord(c) for c in packet[:-4]])
    checkSum = checkSum % 256
  
    if checkSum <= 9:
      checkSumComp = '00' + f"{checkSum}"
    elif checkSum <= 99:
      checkSumComp = '0' + f"{checkSum}"
    else:
      checkSumComp = f"{checkSum}"

    checkSumFromPacket = packet[-3:]

    if checkSumFromPacket == checkSumComp:
 
      if ackNumber == int(pktNum):
        modifiedMessage = f"ACK{ackNumber}"
        print(packet[:-4], end = '')
        serverSocket.sendto(modifiedMessage.encode(), clientAddress)
        ackNumber = 1 - ackNumber
        if message != b'':
          message = b''
      else:
        print("Packet sent out of order")
        TimeoutCalls = TimeoutCalls + 1
        if TimeoutCalls == 3:
          break
    else:
      print('Check Sum Not Same')
      break

