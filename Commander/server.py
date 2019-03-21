from socketserver import StreamRequestHandler, ThreadingTCPServer


class EchoHandler(StreamRequestHandler):

    def handle(self):
        print('Got connection from: ', self.client_address)

        while True:
            pass

    def deal(self, report):
        print(self.client_address, report)

    def send_command(self, command):
        self.request.send(command)

    def send_resource(self, file_byte):
        self.wfile.write(file_byte)
        self.send_command(b'image_stream_end')


class CommanderServer(ThreadingTCPServer):

    def __init__(self, host='0.0.0.0', port=13140, handler=EchoHandler):
        super().__init__((host, port), handler)


if __name__ == '__main__':
    CommanderServer().serve_forever()
