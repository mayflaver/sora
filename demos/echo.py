from tornado.tcpserver import TCPServer
from tornado.ioloop import IOLoop

from sora.parser import BytesUntil
from sora.datahandler import DataHandler

class EchoServer(TCPServer):
    def handle_stream(self, stream, address):
        def callback(data):
            stream.write(data)
        stream.read_until_close(streaming_callback=DataHandler(BytesUntil('\n').then(lambda x: x+'\n'), callback))


if __name__ == '__main__':
    server = EchoServer()
    server.listen(8888)
    IOLoop.instance().start()
    
