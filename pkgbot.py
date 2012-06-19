from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
from twisted.python import log
import time, sys
from distro_scripts import archlinux

class PkgBot(irc.IRCClient):
    
    nickname = "pkgbot"
    class_mapper = {
        'archlinux': archlinux.ArchLinux,
    }
    
    def connectionMade(self):
        irc.IRCClient.connectionMade(self)

    def connectionLost(self, reason):
        irc.IRCClient.connectionLost(self, reason)

    def signedOn(self):
        self.join(self.factory.channel)

    def privmsg(self, user, channel, msg):
        user = user.split('!', 1)[0]
        
        # Check to see if they're sending me a private message
        if channel == self.nickname:
            self.msg(user, 'foobar')
            return

        # Otherwise check to see if it is a message directed at me
        if msg.startswith('.pkg'):
            query = msg.split(' ', 2)
            if query[1] in self.class_mapper.keys():
                res = self.class_mapper[query[1]].search(query[2])
                if len(res) > 0:
                    for package in res:
                        message = "%s - %s (%s);" % (
                            package['name'],
                            package['version'],
                            ', '.join(package['licenses']))
                        del package['name'], package['version'], \
                            package['licenses']
                        extra_data = []
                        for key, value in package.items():
                            extra_data.append("%s: %s" % (key, value))
                        self.msg(channel, "%s: %s %s" % (
                                user,
                                str(message),
                                str(', '.join(extra_data))))
                else:
                    self.msg(channel, user + ": That package wasn't found.")


class PkgBotFactory(protocol.ClientFactory):
    def __init__(self, channel):
        self.channel = channel

    def buildProtocol(self, addr):
        p = PkgBot()
        p.factory = self
        return p

    def clientConnectionLost(self, connector, reason):
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "connection failed:", reason
        reactor.stop()


if __name__ == '__main__':
    f = PkgBotFactory('#programming')
    reactor.connectTCP("irc.tenthbit.net", 6667, f)
    reactor.run()
