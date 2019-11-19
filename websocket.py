
from simple_websocket_server import WebSocketServer, WebSocket
import json
import threading

class BtcWebScoket(WebSocket):
    def handle(self):
        try:
           print(self.data)
           msg = json.loads(self.data)
           msgType = msg['MsgType']
           if msgType == 'PEER_INFO':
               self.send_message('peer_info')
                # self.send_message(json.dumps({
                #     'PEERS_IN':PEERS_IN,
                #     'PEERS_OUT':PEERS_OUT
                    
                # }))
        except Exception as ex:
            print(ex)

    def connected(self):
        print(self.address, 'connected')

    def handle_close(self):
        print(self.address, 'closed')


ws = WebSocketServer('', 9675, BtcWebScoket)
wst = threading.Thread(target=ws.serve_forever)
wst.start()