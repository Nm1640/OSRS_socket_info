import json
import socket

def receive_status(port):
    # Create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Bind the socket to a specific address and port
    s.bind(('localhost', port))
    
    # Listen for incoming connections
    s.listen(1)
    
    print("Waiting for a connection...")
    
    while True:
        # Accept a connection from a client
        conn, addr = s.accept()
        print()
        print("Connected by", addr)
        print()
        
        # Receive data from the client
        data = conn.recv(4096).decode('utf-8')
        
        # Process the received data as needed

        json_data = data.split('\n\n')[-1]

        # Parse the JSON data
        parsed_data = json.loads(json_data)

        # Extract specific information from the parsed data
        player_name = parsed_data['playerName']
        tick = parsed_data['tick']
        run_energy = parsed_data['runEnergy']
        attack = parsed_data['attack']
        equipment = parsed_data['equipment']
        inventory = parsed_data['inventory']
        skills = parsed_data['skills']

        # Print the extracted information
        print(f"Player Name: {player_name}")
        print()
        print(f"Tick: {tick}")
        print()
        print(f"Run Energy: {run_energy}")
        print()
        print(f"Attack: {attack}")
        print()
        print(f"Equipment: {equipment}")
        print()
        print(f"Inventory: {inventory}")
        print()
        print(f"Skills: {skills}")
        print()


if __name__ == '__main__':
    # Specify the port number on which to listen
    port = 12345
    
    # Call the receive_status function
    receive_status(port)
