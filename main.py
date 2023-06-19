import socket
import json

def listen_socket(host, port):
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to a specific address and port
    server_socket.bind((host, port))

    # Listen for a single incoming connection
    server_socket.listen(1)

    print(f'Listening on {host}:{port}...')

    previous_attack = 'None'
    attack_count = 1
    previous_tick = 0
    current_attack = 'None'
    death_counter = 0

    while True:
        # Accept client connections
        client_socket, client_address = server_socket.accept()
        print(f'Connected to {client_address[0]}')

        # Receive data from the client
        data = client_socket.recv(4096).decode()
        print(data)
        # Find where JSON data starts
        json_start = data.find('{')

        # Extract the JSON from the data
        json_str = data[json_start:]

        # Display the data
        data = json.loads(json_str)

        # Handle Death Crashing
        if data['packetType'] == 'death':
            print('Oh dear you are dead...')
            death_counter += 1
            continue

        # Update current information
        if data['attack']['animationName'] !='N/A':
            current_attack = data['attack']['animationAttackStyle']

        # Display Info
        print()
        print('---')
        print()

        print(f'{"Username":>16}: {data["playerName"]}')
        print(f'{"Deaths":>16}: {death_counter}')
        print()
        print(f'{"Health":>16}: {data["skills"][5]["boostedLevel"]} / {data["skills"][5]["realLevel"]}')
        print(f'{"Prayer":>16}: {data["skills"][6]["boostedLevel"]} / {data["skills"][6]["realLevel"]}')
        print(f'{"Run":>16}: {data["runEnergy"] / 100}%')
        print(f'{"Active Prayers":>16}: ', end='')
        if data['prayers']:
            for prayer in data['prayers']:
                print(prayer, end=' ')
        else:
            print('None', end='')
        print()

        if data['inventory']:
            for item in data['inventory']:
                print(item, end=' ')
        else:
            print('None', end='')

        print()
        print()
        print(f'{"Current tick":>16}: {data["tick"]}')
        print(f'{"last attack tick":>16}: {previous_tick}')
        print(f'{"Current attack":>16}: {data["attack"]["animationName"]}')
        print(f'{"Previous attack":>16}: {previous_attack}')
        print(f'{"attack counter":>16}: {attack_count}')
        print()
        if attack_count >= 6:
            print('!!!!!SWITCH STYLES!!!!!')

        # Update Previous information
        if data['attack']['animationName'] !='N/A':
            if previous_attack != current_attack:
                previous_attack = current_attack
                attack_count = 1
            elif previous_attack == current_attack and data['tick'] != previous_tick + 1:
                attack_count += 1

            # Update Tick last
            previous_tick = data['tick']

if __name__ == '__main__':
    host = 'localhost'  
    port = 12347
    listen_socket(host, port)
