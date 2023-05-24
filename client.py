import paramiko

key = paramiko.RSAKey.from_private_key_file('./private_key')
client = paramiko.SSHClient()
client.get_host_keys().add('localhost', 'ssh-rsa', key)
client.connect(hostname='localhost', port=22, pkey=key)
