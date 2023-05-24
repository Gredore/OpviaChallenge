import paramiko
from pathlib import Path

key = paramiko.RSAKey.from_private_key_file('./private_key', password="test_password")
client = paramiko.SSHClient()
client.get_host_keys().add('localhost', 'ssh-rsa', key)

client.connect(hostname='localhost', port=22, pkey=key)

sftp = client.open_sftp()
sftp.sshclient = client


source_path = Path('C:/Users/Georg/OneDrive/Documents/opvia_challenge/TestFile.txt')
target_path = Path('C:/Users/Georg/OneDrive/Documents/opvia_challenge/MovedTestFile.txt')
#sftp.mkdir(str(Path('C:/Users/Georg/OneDrive/Documents/opvia_challenge/testfolder')))
#print(sftp.listdir())
sftp.get(str(source_path), str(target_path))