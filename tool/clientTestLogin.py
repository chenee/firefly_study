from twisted.internet.protocol import Protocol, ClientFactory

class Echo(Protocol):
    def connectionMade(self):
        a = 'N%&0\t\x00\x00\x00\x00\x00\x00\x00.\x00\x00\x00e{"password":"chenee","username":"chenee"}\n'
        self.transport.write(a)

    def dataReceived(self, data):
        print data
        #self.transport.loseConnection()


class EchoClientFactory(ClientFactory):
    def startedConnecting(self, connector):
        print 'Started to connect.'

    def buildProtocol(self, addr):
        print 'Connected.'
        return Echo()

    def clientConnectionLost(self, connector, reason):
        print 'Lost connection.  Reason:', reason

    def clientConnectionFailed(self, connector, reason):
        print 'Connection failed. Reason:', reason

from twisted.internet import reactor
reactor.connectTCP("localhost", 11009, EchoClientFactory())
reactor.run()
