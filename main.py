from server import Server, SFTPServer
import paramiko
import socket
import json

class ServerRunner:
    def __init__(self):

        # Read in control file
        self.controls = self.get_controls(path='server_controls.json')

        # Generate private key
        self._key = paramiko.RSAKey.generate(2048)
        self._key.write_private_key_file(filename='private_key', password='test_password')
        # Create Paramiko transport
        self._transport = self.make_transport()

        # Setup server
        self._s = Server()

        self._transport.start_server(server=self._s)

        self._s.event.wait(30)
    @staticmethod
    def get_controls(path):

        with open(path, 'r') as f:
            return json.load(f)

    def make_transport(self):

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('localhost', 22))

        sock.listen(100)
        client, addr = sock.accept()
        t = paramiko.Transport(client)
        t.add_server_key(self._key)

        t.set_subsystem_handler('sftp', paramiko.SFTPServer, SFTPServer)
        return t

    def close_transport(self):
        self._transport.close()

if __name__ == '__main__':

    server_runner = ServerRunner()


    print("---Script terminated---")


