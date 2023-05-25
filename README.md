# George Irving - Opvia Challenge
My solution to the challenge is a simple sftp client and server implementation.
- For the process of sending files securely, sftp is a well established technology and there is litte need to reinvent the wheel.
- This implementation sets up a server on localhost, and then a client is able to move files from one folder to another folder over localhost

**Usage**:

- [Optional] Change any options in the `controls.json`
- Run `server.py` in a console
- Run `client.py` in a console

The default implementation moves two files from the `files_to_move` folder to the `destination_folder`.

**Alternative approaches:**

- Given what I understand about Opvia's current product, it would make sense, instead of sending files from one computer to the other, to upload the client's files securely and store them remotely
- Then on the other computer, the client would log into their Opvia account and download the files from their project
