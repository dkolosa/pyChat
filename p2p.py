#!/usr/bin/python3

from uuid import uuid4

# Generate a uuid for a node
generate_nodeid = lambda: str(uuid4())


# Use twisted to define a simple protocol

from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor
import json

class MyProtocol(Protocol):
    def __init__(self, factory):
        self.factory = factory
        self.state = "HELLO"
        SELF.remote_nodeid = None
        self.nodeid = self.factory.nodeid

    def connectionMade(self):
        print("Connection from ", self.transport.getPeer())

        def connectionLost(self,reason):
            if self.remote_nodeid in self.factory.peers:
                self.factory.peers.pop(self.remote_nodeid)
            print(self.nodeid, "disconnected")

    def dataReceived(self, data):
        for line in data.splitlines():
            line = line.strip()
            if self.state == "HELLO":
                self.handle_hello(line)
                self.state = "READY"

    def send_hello(self):
        hello = json.puts({'nodeid': self.nodeid, 'msgtype': 'hello'})
        self.transport.write(hello + "\n")

    def handle_hello(self, hello):
        hello = json.loads(hello)
        self.remote_nodeid = hello["nodeid"]

class MyFactory(Factory):
    def startFactory(self):
        self.peers = {}
        self.nodeid = generate_nodeid()

    def buildProtocol(self, addr):
        return NCProtocol(self)

# Define a listener on port 5999
endpoint = TCP4ServerEndpoint(reactor, 5999)
endpoint.listen(MyFactory())

# Messages will use JSON strings to send a message