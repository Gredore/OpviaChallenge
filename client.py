import paramiko
from pathlib import Path
import json


class SFTPClientRunner:
    def __init__(self):
        self.controls = self.get_controls(path="server_controls.json")

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
        with open(path, "r") as f:
            return json.load(f)

    @staticmethod
    def get_key(key_path, password):
        return paramiko.RSAKey.from_private_key_file(key_path, password=password)

    @staticmethod
    def set_up_client(key, address):
        client = paramiko.SSHClient()
        client.get_host_keys().add(address, "ssh-rsa", key)

        return client

    @staticmethod
    def make_connection(client, key, address, port):
        client.connect(hostname=address, port=port, pkey=key)

        sftp = client.open_sftp()
        sftp.sshclient = client

        return sftp

    @staticmethod
    def move_files(file_list, source_path, target_path, sftp):
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
