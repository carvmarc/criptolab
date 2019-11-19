    
from bitcoin.messages import msg_version, msg_verack, msg_addr, MsgSerializable, msg_getaddr, msg_addr


def version_pkt(client_ip, server_ip, port):
    msg = msg_version()
    msg.nVersion = 70002
    msg.addrTo.ip = server_ip
    msg.addrTo.port = port
    msg.addrFrom.ip = client_ip
    msg.addrFrom.port = port

    return msg