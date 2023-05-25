import paramiko
from pathlib import Path
import json


class SFTPClientRunner:
    def __init__(self):
        self.controls = self.get_controls(path="controls.json")

        self._key = self.get_key(
            key_path=self.controls["private_key_file_path"],
            password=self.controls["password"],
        )

        self._client = self.set_up_client(
            key=self._key, address=self.controls["address"]
        )

        self._sftp = self.make_connection(
            client=self._client,
            key=self._key,
            address=self.controls["address"],
            port=self.controls["port"],
        )

        self.move_files(
            file_list=self.controls["list_of_files_to_move"],
            source_path=self.controls["source_folder_relative_path"],
            target_path=self.controls["target_folder_relative_path"],
            sftp=self._sftp,
        )

    @staticmethod
    def get_controls(path):
        """
        Reads control file json
        :param path: path to find the json control file
        :return: diction of control file data
        """
        with open(path, "r") as f:
            return json.load(f)

    @staticmethod
    def get_key(key_path, password):
        """
        Makes RSAKey from key file path
        :param key_path: path to the private key
        :param password: password encrypting the key
        :return:
        """
        return paramiko.RSAKey.from_private_key_file(key_path, password=password)

    @staticmethod
    def set_up_client(key, address):
        """
        Makes paramiko SSH client and adds the host key
        :param key: RSA key object
        :param address: address of server
        :return:
        """
        client = paramiko.SSHClient()
        client.get_host_keys().add(address, "ssh-rsa", key)

        return client

    @staticmethod
    def make_connection(client, key, address, port):
        """
        Connects to sftp server
        :param client: client object to make the connection with
        :param key: private key object
        :param address: server address
        :param port: server port
        :return:
        """
        client.connect(hostname=address, port=port, pkey=key)

        sftp = client.open_sftp()
        sftp.sshclient = client

        return sftp

    @staticmethod
    def move_files(file_list, source_path, target_path, sftp):
        """
        Moves multiple files from server to client
        :param file_list: list of files to move
        :param source_path: relative path to files on server
        :param target_path: relative path to destination folder on client
        :param sftp: sftp object
        :return:
        """
        for file in file_list:
            source_path_str = str(Path(source_path) / file)
            target_path_str = str(Path(target_path) / file)

            try:
                sftp.get(
                    source_path_str.encode("unicode_escape"),
                    target_path_str.encode("unicode_escape"),
                )
                print(f"{file} successfully transferred to {target_path}")
            except OSError as error:
                print(f"Error with file: {file}")
                print(f"{error}")


if __name__ == "__main__":
    SFTP_client_runner = SFTPClientRunner()

    print("---Script terminated---")
