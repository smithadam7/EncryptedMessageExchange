import socket
import socket
import sys

# In Python 3, install pycryptodome for crypto imports to work
from Crypto.Cipher import AES

# This import is for generating a key

# Predetermined key shared by both parties. This was was randomly generated with get_random_bytes(32)
# key = get_random_bytes(32) # Use a stored or generated key
key = b"\x96\xbb=\xeb\x1e\x02\xd8\x1aOu\xff\xdd\xc9i\xa5'k\xd9\\\x18\x93\xdf\x01\xac\x8f\x13&\x8f\x1f\x14i\xb2"
# HOST - change this to public IP if you are using it over the internet
HOST = "127.0.0.1"
# PORT - any unused port can be used. forward this port if you want to use it over internet
PORT = 777
VIEW = 1


SOCKET_LIST = []
RECV_BUFFER = 4096


def chat_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(10)

    SOCKET_LIST.append(server_socket)

    print("Server started on port " + str(PORT))

    conn, addr = server_socket.accept()
    with conn:
        print('Connected by', addr)
        while True:
            encrypted_message_and_iv = conn.recv(1024)
            if not encrypted_message_and_iv:
                break

            # print("Encrypted Data with SPACER: ", encrypted_message_and_iv)
            bytestreamArray = encrypted_message_and_iv.split(b"SPACER")
            encrypted_message = bytestreamArray[0]
            ivrec = bytestreamArray[1]
            cipher_decryptrec = AES.new(key, AES.MODE_CFB, iv=ivrec)
            deciphered_bytesrec = cipher_decryptrec.decrypt(encrypted_message)

            # Convert the bytes object back to the string and display
            decrypted_datarec = deciphered_bytesrec.decode('utf-8')
            print("Decrypted Message: ", decrypted_datarec)

            # Get reply message and encrypt it
            replymessage = sys.stdin.readline()
            replymessage = replymessage.encode("utf-8")
            # Create the cipher object and encrypt the data
            cipher_encrypt_reply = AES.new(key, AES.MODE_CFB)
            ciphered_bytes_reply = cipher_encrypt_reply.encrypt(replymessage)
            iv_reply = cipher_encrypt_reply.iv
            conn.sendall(ciphered_bytes_reply + b'SPACER' + iv_reply)
            conn.close()
            break


if __name__ == "__main__":
    sys.exit(chat_server())
