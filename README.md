This is an encrypted message exchange. 

In Python 3, make sure to install pycryptodome for crypto imports to work.

Run the server and then run the client python files. They can be on the same local machine or over the internet by simply changing the ip addresses.

The encryption uses a predetermined key that is shared by both parties.

Once the client has connected to the server, enter a message to send. The message is then encrypted with the key and then sent to the server. The server decrypts the message and displays it. Then the server can reply to the message. The message is then encrypted and sent to the client, and then both parties are disconnected. The message is decrypted and displayed on the client.

This prevents an attacker from reading the message. An attacker could only see an encrypted string being sent ovet the internet, they cannot decrypt it without the key which is stored locally.
