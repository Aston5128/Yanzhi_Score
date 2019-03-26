from socketserver import StreamRequestHandler, ThreadingTCPServer


class EchoHandler(StreamRequestHandler):

    def handle(self):
        print('Got connection from: ', self.client_address)

        while True:
            pass

    def deal(self, report):
        """ 处理士兵报告 """
        print(self.client_address, report)

    def send_command(self, command):
        """ 向士兵发送命令 """
        self.request.send(command)

    def send_resource(self, file_byte):
        """ 发送士兵所需资源（文件） """
        self.wfile.write(file_byte)
        self.send_command(b'image_stream_end')


class CommanderServer(ThreadingTCPServer):

    def __init__(self, host='0.0.0.0', port=13140, handler=EchoHandler):
        super().__init__((host, port), handler)


if __name__ == '__main__':
    CommanderServer().serve_forever()
