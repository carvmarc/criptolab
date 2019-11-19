#Socket client 
# connect to mutiple servers
#outbound 
import socket
import threading
import time
from bitcoin.messages import msg_version, msg_verack, msg_addr, MsgSerializable, msg_getaddr, msg_addr
import messages

SLEEP_TIME = 2
MY_IP='172.31.16.27'
#Manage mutiple outbound connections
class SocketClientManager:
    def __init__(self):
        self.outbound_connections = set([])
        
 
    def connect(self, destIp, destPort):
        sc = socket.socket()
        sc.connect((destIp,destPort))
       
        t = threading.Thread(target=self.messageHandler,args=(sc,))
        t.start()
    
    def messageHandler(self, sSocket):
        serverAddr= sSocket.getpeername()[0]
        serverPort=sSocket.getpeername()[1]
        sSocket.send(messages.version_pkt(MY_IP, serverAddr,serverPort).to_bytes())
        
        
        while True:
            dataReceived = sSocket.recv(1024)
            if not dataReceived:
                #will close the socket
                break;
            msg = MsgSerializable().from_bytes(dataReceived)
            print('on_new_server')
            print('received ',msg)
            if isinstance(msg,msg_version):
                self.outbound_connections.add(serverAddr)
                sSocket.send(msg_verack().to_bytes())
                print('sent verack')
                sSocket.send(msg_getaddr().to_bytes())
                print('sent msg_getaddr')
            if isinstance(msg,msg_addr):
                for peer in msg.addrs:
                    if peer.ip not in self.outbound_connections and peer.ip != MY_IP:
                        print('new peer found'+peer.ip)
                        self.connect(peer.ip, peer.port)
                    
            time.sleep(SLEEP_TIME)
        sSocket.close()
        