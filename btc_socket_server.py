#Socket client 
# connect to mutiple servers
#outbound 
import socket
import threading
import time
from bitcoin.messages import msg_version, msg_verack, msg_addr, MsgSerializable, msg_getaddr, msg_addr
import messages
from bitcoin.net import CAddress

SLEEP_TIME = 2
MY_IP='172.31.16.27'
#Manage mutiple outbound connections
class SocketServerManager:
    def __init__(self, host, port):
        self.host=host
        self.port=port
        self.inbound_connections = set([])
        self.socket = socket.socket()
        self.socket.bind((host, port))
        self.socket.listen()
        
    def start(self):
        print('Server started')
        while True:
            print('Waiting connections')
            conn, addr = self.socket.accept()
            print('Connected by', addr)
            t = threading.Thread(target=self.messageHandler,args=(conn,addr))
            t.start()
            print('sleeping')
            time.sleep(SLEEP_TIME)
        
    def messageHandler(self, clientsocket, addr):
        while True:
            dataReceived = clientsocket.recv(1024)
            if not dataReceived:
                #will close the socket
                break;
            msg = MsgSerializable().from_bytes(dataReceived)
            print('received ',msg)
            print( isinstance(msg,msg_version))
            if isinstance(msg,msg_version):
                clientsocket.send(msg_verack().to_bytes())
                self.inbound_connections.add(addr[0])
                print('sent verack')
                clientsocket.send( messages.version_pkt(MY_IP, addr[0],self.port).to_bytes() )
                print('sent version_pkt')
            if isinstance(msg,msg_getaddr):
                perrAddrs = []
                for peer in self.inbound_connections:
                    perrAddr = CAddress()
                    perrAddr.port=self.port
                    perrAddr.nTime = int(time.time())
                    perrAddr.ip = peer
                    perrAddrs.append(perrAddr)
                rMsg= msg_addr()
                rMsg.addrs = perrAddrs
                print(rMsg)
                clientsocket.send(rMsg.to_bytes())
                print('sent msg_addr')
                
            time.sleep(SLEEP_TIME)
        clientsocket.close()
        