# sora
Sora is a wonderful function tool for tornado and provide high level parser to make tornado protocol extends more easy

# demo
Here is a simple echo demo:

    from tornado.tcpserver import TCPServer
    from tornado.ioloop import IOLoop

    from sora.datahandler import DataHandler
    from sora.parser import UnsizedParserBuffer

    class EchoServer(TCPServer):
        def handle_stream(self, stream, address):
            def callback(data):
                stream.write(data)
            stream.read_until_close(streaming_callback=DataHandler(UnsizedParserBuffer('\n', include=True), callback))

    if __name__ == '__main__':
        server = EchoServer()
        server.listen(8888)
        IOLoop.instance().start()

# Current supported protocols:
* echo
* redis

# Third-party protocol extensions
We're currently asking anyone working on implementing support for new protocols to build your project and make share with others. 
