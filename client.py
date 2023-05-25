import paramiko
from pathlib import Path

key = paramiko.RSAKey.from_private_key_file('./private_key', password="test_password")
client = paramiko.SSHClient()
client.get_host_keys().add('localhost', 'ssh-rsa', key)

client.connect(hostname='localhost', port=22, pkey=key)

sftp = client.open_sftp()
sftp.sshclient = client


source_path = str(Path('./files_to_move/TestFile.txt'))
target_path = str(Path('C:/Users/Georg/OneDrive/Documents/opvia_challenge/destination_folder/TestFile.txt'))


#sftp.listdir()
sftp.get(source_path.encode('unicode_escape'), target_path.encode('unicode_escape'))
