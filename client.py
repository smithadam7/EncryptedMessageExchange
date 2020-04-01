import select
import socket
import sys

# import pycryptodome
from Crypto.Cipher import AES


def chat_client():
    host = "127.0.0.1"
    port = 777

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Give the other person 100 seconds to reply, or shut down
    s.settimeout(100)

    try:
        s.connect((host, port))

    except:
        print("\033[91m" + 'Unable to connect' + "\033[0m")
        sys.exit()

    print("\033[33m" + "Connected to remote host. Type a message and press enter to send.")
    sys.stdout.write("\033[94m" + '\n[Me]: ' + "\033[0m")
    # sys.stdout.flush()
    # predetermined key to be shared by both parties.
    key = b"\x96\xbb=\xeb\x1e\x02\xd8\x1aOu\xff\xdd\xc9i\xa5'k\xd9\\\x18\x93\xdf\x01\xac\x8f\x13&\x8f\x1f\x14i\xb2"

    # Get message from user and encode to utf-8
    data_to_encrypt = sys.stdin.readline()
    data = data_to_encrypt.encode('utf-8')

    # Create the cipher object and encrypt the data, iv is needed for decryption along with the key
    cipher_encrypt = AES.new(key, AES.MODE_CFB)
    ciphered_bytes = cipher_encrypt.encrypt(data)
    iv = cipher_encrypt.iv

    # === Decrypt ===

    # Create the cipher object and decrypt the data
    # cipher_decrypt = AES.new(key, AES.MODE_CFB, iv=iv)
    # deciphered_bytes = cipher_decrypt.decrypt(ciphered_bytes)

    # Convert the bytes object back to the string
    # decrypted_data = deciphered_bytes.decode('utf-8')
    # Send the encrypted message along with the iv needed to decrypt separated by a SPACER
    s.sendall(ciphered_bytes + b'SPACER' + iv)
    # print("Ciphered Data: ", ciphered_bytes)

    # Received encrypted reply message
    encrypted_message_and_iv = s.recv(1024)
    bytestreamArray = encrypted_message_and_iv.split(b"SPACER")
    encrypted_message = bytestreamArray[0]
    ivrec = bytestreamArray[1]
    cipher_decryptrec = AES.new(key, AES.MODE_CFB, iv=ivrec)
    deciphered_bytesrec = cipher_decryptrec.decrypt(encrypted_message)

    # Convert the bytes object back to the string and display
    decrypted_datarec = deciphered_bytesrec.decode('utf-8')
    print("\033[32m" + '[Reply]: ' + "\033[32m" + decrypted_datarec + "\033[0m")

    # print("\033[91m" + 'Server took too long to send reply message' + "\033[0m")

    while 1:
        # sys.stdin on linux, socket.socket() on windows
        # socket_list = [sys.stdin, s]
        socket_list = [socket.socket(), s]
        read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])

        for sock in read_sockets:
            if sock == s:

                data = sock.recv(4096)

                if not data:
                    print("\033[33m" + "\nDisconnected from server")
                    sys.exit()
                else:
                    # data = ciphered_data
                    sys.stdout.write(data)
                    sys.stdout.write("\033[34m" + '\n[Me :] ' + "\033[0m")
                    sys.stdout.flush()

            else:
                print("\033[33m" + "\nDisconnected from server")
                break


if __name__ == "__main__":
    sys.exit(chat_client())
