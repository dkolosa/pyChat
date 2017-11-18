import socket
import threading
import sys
import time
from random import randint


class Server():
    # Using IPV4 and TCP
    connections = []
    peers = []

    def __init__(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('0.0.0.0', 10000))
        sock.listen(1)
        print("server running...")
        while True:
            c, a = sock.accept()

            # Create a thread to handle multiple connections
            cthread = threading.Thread(target=self.handler, args=(c,a))
            # Close the program regardless if program is still running
            cthread.daemon = True
            cthread.start()
            self.peers.append(a[0])
            self.connections.append(c)
            print(str(a[0]) + ':' + str(a[1]) + 'connected')
            self.send_peers()

    def handler(self,c,a):
        while True:
            data = c.recv(1024)
            for connection in self.connections:
                connection.send(bytes(data))
            if not data:
                print(str(a[0]) + ':' + str(a[1]) + 'disconnected')
                self.connections.remove(c)
                self.peers.remove(a[0])
                c.close()
                self.send_peers()
                break

    def send_peers(self):
        p = ""

        for peer in self.peers:
            p += peer + ","

        # Send the list to all of the peers
        for connection in self.connections:
            connection.send(b'\x11' + bytes(p, "utf-8"))


class Client:

    def send_message(self, sock):
        while True:
            sock.send(bytes(input(""), 'utf-8'))

    def __init__(self, address):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        sock.connect((address, 10000))

        input_thread = threading.Thread(target=self.send_message, args=(sock,))
        input_thread.daemon = True
        input_thread.start()

        while True:
            data = sock.recv(1024)
            if not data:
                break
            if data[0:1] == b'\x11':
                self.update_peers(data[1:])
            else:
                print(str(data, 'utf-8'))

    def update_peers(self, peer_data):
        p2p.peers = str(peer_data, "utf-8").split(",")[:-1]


class p2p:
    # First value set as default peer
    peers = ['192.168.1.8']


while True:
    try:
        print("Trying to connect...")
        time.sleep(randint(1, 5))

        for peer in p2p.peers:
            try:
                client = Client(peer)
            except KeyboardInterrupt:
                sys.exit(0)
            except:
                pass
            try:
                server = Server()
            except KeyboardInterrupt:
                sys.exit(0)
            except:
                print("Couldn't start the server...")

    except KeyboardInterrupt:
        sys.exit(0)

