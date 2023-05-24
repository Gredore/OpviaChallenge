import paramiko

key = paramiko.RSAKey.from_private_key_file('./private_key', password="test_password")
client = paramiko.SSHClient()
client.get_host_keys().add('localhost', 'ssh-rsa', key)

client.connect(hostname='localhost', port=22, pkey=key)

sftp = client.open_sftp()
sftp.sshclient = client

dirlist = sftp.listdir('.')
for row in dirlist:
    print(row)