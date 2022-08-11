from twisted.internet import reactor
from twisted.internet.protocol import Protocol
from twisted.internet.protocol import ServerFactory as ServFactory
from twisted.internet.endpoints import TCP4ServerEndpoint

class Server(Protocol):
    def __init__(self, users):
        self.users = users

    def connectionMade(self):
        print("New connection")
        self.users.append(self)
        self.transport.write("Hello from server".encode("utf-8"))

    def dataReceived(self, data):
        for user in self.users:
            user.transport.write(data)

class ServerFactory(ServFactory):
    def __init__(self):
        self.users = []

    def buildProtocol(self, add):
        return Server(self.users)

if __name__ == '__main__':
    endpoint = TCP4ServerEndpoint(reactor, 2000)
    endpoint.listen(ServerFactory())
    reactor.run()
