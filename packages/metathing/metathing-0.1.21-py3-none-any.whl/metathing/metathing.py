#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from metathing.service import Service
from metathing.logger import logger
import socket, time
import struct

MCAST_GRP = '239.1.2.3'
MCAST_PORT = 34567
RECV_MCAST_PORT = 34568

class MetaThing():
    def __init__(self, config: object, srv_name: str):
        self.srv = Service(config, srv_name)
        self.addr = None

    def Bind(self, app:object):
        self.srv.mqtt.connect()
        self.srv.Bind(app)
        app.LoadModel()

    def Run(self):
        self.srv.http.Run()
        
    def OpenIPBroadcast(self):
        import threading
        t = threading.Thread(target=MetaThing.MTNodeIPSend)
        logger.info('[Auth]: Starting IP broadcast thread...')
        t.start()

    @staticmethod
    def KillProcessWithSameIpAndPort(ip, port):
        import psutil
        current_pid = psutil.Process().pid 
        for conn in psutil.net_connections():
            if conn.laddr.ip == ip and conn.laddr.port == port and conn.pid != current_pid:
                pid = conn.pid
                psutil.Process(pid).kill()
                logger.warning(f"Killed conflicted process with pid {pid}")
        
    @staticmethod
    def MTNodeIPRequest():
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
        req_msg = 'MTNode_IP_REQUEST'

        sock_recv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock_recv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock_recv.bind(('', RECV_MCAST_PORT))
        mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
        sock_recv.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        sock_recv.settimeout(5)
        while True:
            sock.sendto(req_msg.encode(), (MCAST_GRP, MCAST_PORT))
            try:
                logger.info('Requesting MTNode IP...')
                data, address = sock_recv.recvfrom(1024)
                data = data.decode()
                logger.info(f'Success: {data}')
                sock.close()
                sock_recv.close()
                return data
            except socket.timeout:
                logger.info('Timeout, retrying...')
        
    @staticmethod        
    def MTNodeIPSend():
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('', MCAST_PORT))
        mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        sock_sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock_sender.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
        csock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        csock.connect(('8.8.8.8', 80))
        (addr, port) = csock.getsockname()
        csock.close()
        while True:
            data, address = sock.recvfrom(1024)
            if data == b'MTNode_IP_REQUEST':
                logger.info(f'Received request from: {address}')
                logger.info(f'Sending my address: {addr}')
                sock_sender.sendto(addr.encode(), (MCAST_GRP, RECV_MCAST_PORT))
                
# if __name__ == '__main__':
#     # Open a thread to run MetaThing.MTNodeIPSend()
#     import threading
#     t = threading.Thread(target=MetaThing.MTNodeIPSend)
#     t.start()
    
#     MetaThing.MTNodeIPRequest()     