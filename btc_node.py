from btc_socket_client import SocketClientManager
from btc_socket_server import SocketServerManager
import threading

HOST = ''  
PORT = 65442

DNS_SEED = '172.31.20.33'




try:
    
    clientManager = SocketClientManager()
    serverManager = SocketServerManager(HOST,PORT)
    
    threading.Thread(target=serverManager.start)
    
    
    clientManager.connect(DNS_SEED,PORT)


except Exception as ex:
    print(ex)

