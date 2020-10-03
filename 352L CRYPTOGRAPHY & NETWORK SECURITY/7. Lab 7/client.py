
# Import Python Socket, pickle, hashlib Module
import socket, pickle, hashlib


# Recieve message from user
print("Enter message to send: ")
# Assign to @param msg
msg = input()


# Connect to server port and send message
def connect(msg):

    # Initialize socket stream
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Specify port
    port = 6000
    # Connect to port 
    s.connect((socket.gethostname(), port))

    # Recieve Encryption Key
    e = s.recv(1024)

    # Decode byte string
    e = e.decode("utf-8")

    # Show public encryption key
    print(f"Key recieved {e}")

    # Recieve Mod Key
    n = s.recv(1024)

    # Decode byte string
    n = n.decode("utf-8")

    # Encrypt message
    enc_msg, hex_value = encrypt(msg, e, n)

    # Pickle array 
    data_string = pickle.dumps(enc_msg)

    # Send pickle to server
    s.send(data_string)

    # Send original hex to server (debug for verification)
    s.send(bytes(str(hex_value), "utf-8"))

    # Close connection / Cleanup
    s.close()

# EOF


# Returns encrypted message
def encrypt(msg, e, n):

    # Hash message using SHA-1
    hash_obj = hashlib.sha1(bytes(msg, encoding='utf-8'))

    # Convert Hash object to hex
    hex_value = hash_obj.hexdigest()

    # Confirm hashing completed
    print(f"Hashed message to {hex_value}")

    # Encrypt via RSA Scheme
    signed_msg = rsa(str(hex_value), int(e), int(n))

    #Confirm signed message
    print(f"Signed message to {signed_msg}")

    # Return encrypted message
    return signed_msg, hex_value

# EOF


# Encrypt Message with key
def rsa(text, e, n):

    # Sign each charachter with key
    ctext = [pow(ord(char),e,n) for char in text]
    
    # Returns Array
    return ctext

# EOF


# Run function for connection
connect(msg)

# End of client.py