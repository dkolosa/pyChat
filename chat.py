import socket
import threading
import sys



class Server():
    # Using IPV4 and TCP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connections = []

    def __init__(self):
        self.sock.bind(('0.0.0.0', 10000))
        self.sock.listen(1)



    def handler(self,c,a):
        while True:
            data = c.recv(1024)
            for connection in self.connections:
                connection.send(bytes(data))
            if not data:
                print(str(a[0]) + ':' + str(a[1]) + 'disconnected')
                self.connections.remove(c)
                c.close()
                break

    def run(self):
        while True:
            c, a = self.sock.accept()

            # Create a thread to handle multiple connections
            cthread = threading.Thread(target=self.handler, args=(c,a))
            # Close the program regardless if program is still running
            cthread.daemon = True
            cthread.start()

            self.connections.append(c)
            print(str(a[0]) + ':' + str(a[1]) + 'connected')


class Client:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send_message(self):
        while True:
            self.sock.send(bytes(input(""), 'utf-8'))

    def __init__(self, address):
        self.sock.connect((address, 10000))

        input_thread = threading.Thread(target=self.send_message)
        input_thread.daemon = True
        input_thread.start()

        while True:
            data = self.sock.recv(1024)
            if not data:
                break
            print(str(data, 'utf-8'))





if (len(sys.argv) > 1):
    client = Client(sys.argv[1])
else:
    server = Server()
    server.run()