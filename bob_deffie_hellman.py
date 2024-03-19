import socket 
import sys 
import pickle 

# g^x mod n 

def calc_power(n,g,x): 
    if(g==1): 
        return 1 
    return (g**x) % n 

def main(): 
    host = '127.0.0.1' 
    port = 12346

    try: 

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

        s.bind((host, port)) 
        s.listen(1) 
        
        print(f"Listening on {host}:{port}...") 
        
        conn, addr = s.accept() 

        print(f"Connection from {addr}") 

        n = 11 # prime number 
        g = 7 # primitive root of n 
        
        private_key_b = int(input("Enter private key of Bob: ")) # 3 
        
        public_key_b = calc_power(n,g,private_key_b) 
        
        # send public key of bob to attacker
        data2 = pickle.dumps(public_key_b) 
        conn.sendall(data2) 
        
        # Receive public key of attacker
        data = conn.recv(4096) 
        public_key_a = pickle.loads(data) 

        print("Received public key of Tom: ", public_key_a) 

        # Calculate shared secret key 
        shared_secret_key = calc_power(n,public_key_a,private_key_b)
        print("Bob's Shared Secret Key with Tom: ", shared_secret_key) 
        
        conn.close() 

    except Exception as e: 

        print(f"Error: {e}") 
        sys.exit(1) 

if __name__ == "__main__": 
    main() 
