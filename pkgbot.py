from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
from twisted.python import log
from distro_scripts import archlinux, ubuntu


class PkgBot(irc.IRCClient):

    nickname = "pkgbot"
    class_mapper = {
        'archlinux': archlinux.ArchLinux,
        'ubuntu': ubuntu.Ubuntu,
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
            if '-' in query[1]:
                name, repo = query[1].split('-')
                if name in self.class_mapper.keys():
                    res = self.class_mapper[name].search(query[2],
                                                         repository=repo)
            else:
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


class PkgBotConfig(object):
    """
    Class to hold configuration options for pkgbot.
    """
    def __init__(self,
                 network='irc.oftc.net',
                 channel='#pkgbot',
                 port=6667,
                 ssl=False):
        self.network = network
        self.channel = channel
        self.port = int(port)
        self.ssl = ssl
        self.loadConfig()

    def loadConfig(self, filename=None):
        """
        Look for configuration file and parse it.
        """
        if not filename:
            try:
                import config

                self.network = config.IRC_NETWORK
                self.channel = config.IRC_CHANNEL
                self.port = int(config.IRC_NETWORK_PORT)
                self.ssl = config.IRC_NETWORK_SSL
            except ImportError:
                pass
            except AttributeError:
                pass


if __name__ == '__main__':
    cfg = PkgBotConfig()
    f = PkgBotFactory(cfg.channel)
    reactor.connectTCP(cfg.network, cfg.port, f)
    reactor.run()
