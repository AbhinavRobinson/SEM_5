# Import python socket, random, sympy, hashlib, pickle module
import socket, random, sympy, hashlib, pickle


# Connect and recieve message
def recieve():

    # Define prime upper bound
    PRIME_LIMIT = 1000000000000

    # Generate Key Pair
    e,d,n = generate(sympy.randprime(1,PRIME_LIMIT),sympy.randprime(1,PRIME_LIMIT))

    print(f"Encryption Key: {e} \n Mod Key: {n} \n Secret Key: {d}")

    # Initialize socket stream
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Specify port
    port = 6000

    # Bind to port 
    s.bind((socket.gethostname(), port))

    # Listen for 1 client connection
    s.listen(1)

    # Server init message
    print(f"Server initialised and listening to Port:{port}")

    # Listen for client message
    while True:
 
        # Get client socket and address
        clientsocket, address = s.accept()

        # Print Connection details
        print(f"Connection to {address} established!")

        # Send Encryption key (public)
        clientsocket.send(bytes(str(e),"utf-8"))

        # Send Mod Key (public)
        clientsocket.send(bytes(str(n),"utf-8"))

        # Recieve pickle data stream
        data_string = clientsocket.recv(4096)

        # Recieve Original Hex value (debug for verification)
        hex_encoded = clientsocket.recv(1024)

        # Decode Hex from UTF-8
        public_hex_value = hex_encoded.decode("utf-8")

        # Pickle -> array
        signed_msg = pickle.loads(data_string)

        # Give confirmation
        print(f"Authentication Status: True \n Recieved: {signed_msg}")

        # Decrypt using private key
        hex_value = decrypt(signed_msg, d, n)

        # Show decrypted Hex Value
        print(f"Decrypted Hash Value: {hex_value}")

        # Integrity Check
        if hex_value == public_hex_value: 
            # Success
            print("Integrity Status : True")
            break
    #End of while loop

    # Close Connections / Cleanup
    clientsocket.close()
    s.close()
    
# EOF


# Decrpytes Hex from RSA Scheme
def decrypt(ctext,d,n):

    try:
        # Decrypt Hex Array from Encrypted Array
        text = [chr(pow(int(char),d,n)) for char in ctext]

        # Returns String
        return "".join(text)

    # Catch Exception
    except TypeError as e: print(e)

# EOF


### GENERATE PUBLIC PRIVATE KEY (UNCOMMENTED) ###

def generate(p_num1,p_num2,key_size = 128):
    
    n = p_num1 * p_num2
    tot = (p_num1 - 1) * (p_num2 - 1)
    
    e = generatePublicKey(tot,key_size)
    d = generatePrivateKey(e,tot)

    return e,d,n


def generatePublicKey(tot,key_size):
   
    e = random.randint(2**(key_size-1),2**key_size - 1)
    g = gcd(e,tot)
    
    while g != 1:

        e = random.randint(2**(key_size-1),2**key_size - 1)
        g = gcd(e,tot)

    return e


def generatePrivateKey(e,tot):
    
    d = egcd(e,tot)[1]
    d = d % tot
    
    if d < 0 : d += tot
    
    return d


def egcd(a,b):
    
    if a == 0: return (b, 0, 1)
    else: g, y, x = egcd(b % a, a)
    
    return (g, x - (b // a) * y, y)


def gcd(e,tot):
     
    temp = 0
    
    while True:
        
        temp = e % tot
        
        if temp == 0: return tot
        
        e = tot
        tot = temp


def isPrime(num):
     
    if num < 2 : return False
    if num == 2 : return True
    if num & 0x01 == 0 : return False
    
    n = int(num ** 0.5 )
    
    for i in range(3,n,2):
        if num % i == 0: return False

    return True

### End Of Key Generation ###


# Run function for connection
recieve()

# End of server.py