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
    try: 

        # Attacker is connecting to Alice
        s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        s1.connect((host, 12345)) 

        print(f"Connected to Alice {host}:12345") 
        
        # Attacker is connecting to Bob
        s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        s2.connect((host, 12346)) 

        print(f"Connected to Bob {host}:12346") 


        n = 11 # prime number 
        g = 7 # primitive root of n 


        print("\nTom is doing a Man in the Middle Attack\n") 

        # Receive public key of alice 
        data = s1.recv(4096) 
        public_key_a = pickle.loads(data) 

        print("Public key of Alice received by Tom: ", public_key_a) 

        # Receive public key of bob 
        data2 = s2.recv(1024) 
        public_key_b = pickle.loads(data2) 

        print("Public key of Bob received by Tom: ", public_key_b) 

        private_key_t = int(input("Enter private key of Tom: ")) # 4 
       

        public_key_t = calc_power(n,g,private_key_t) 

        # send public key of attacker to alice
        
        data = pickle.dumps(public_key_t) 
        s1.sendall(data) 

        # send public key of attacker to bob
        
        data = pickle.dumps(public_key_t) 
        s2.sendall(data) 

        print("Public key of Tom sent to Alice and Bob: ", public_key_t) 
    
        s1.close() 
        s2.close() 

    except Exception as e: 

        print(f"Error: {e}") 
        sys.exit(1) 

if __name__ == "__main__": 
    main() 
