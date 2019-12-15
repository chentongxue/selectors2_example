import socket
import selectors2 as selectors


class Server(object):
    def __init__(self, host, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        address = (host, port)
        self.server.bind(address)
        self.server.listen(10)
        self.server.setblocking(False)

        self.select = selectors.DefaultSelector()
        self.select.register(self.server, selectors.EVENT_READ | selectors.EVENT_WRITE)
        self.connect_count = 0
        self.connections = dict()

    def accept(self, sock):
        connection, address = sock.accept()
        connection.setblocking(False)
        self.select.register(connection, selectors.EVENT_READ, self.read)
        self.connections[address] = self.connect_count
        self.connect_count += 1

    def read(self, connection):
        data = connection.recv(1024)
        address = connection.getpeername()
        address_string = '%s:%s' % address
        client_id = self.connections.get(address)
        if data:
            print 'receive message from Address[%s] ClientID[%s] Message:[%s]' % (address_string, client_id, data)
            message = raw_input("input your message:")
            connection.send(message)
            print 'echo message to Address[%s] ClientID[%s] Message:[%s]' % (address_string, client_id, message)

    def run(self):
        while 1:
            events = self.select.select(1)
            for key, event in events:
                if event & selectors.EVENT_READ:
                    if not key.data:
                        self.accept(key.fileobj)
                    else:
                        self.read(key.fileobj)


server = Server('127.0.0.1', 9999)
server.run()
