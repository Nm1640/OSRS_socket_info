import socket
import threading
import json

class OsrsSocket:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = None

        # Data attributes
        self.player_name = ''
        self.tick = 0
        self.run_energy = 0
        self.special_attack = 0
        self.attack = {}
        self.equipment_stats = {}
        self.equipment = []
        self.inventory = []
        self.skills = []
        self.prayers = []
        self.local_point = {}
        self.world_point = {}
        self.camera = {}

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(1)
        print(f'Listening on {self.host}:{self.port}.')
        threading.Thread(target=self.accept_connections).start()

    def accept_connections(self):
        while True:
            client_socket, client_address = self.server_socket.accept()
            threading.Thread(target=self.handle_connection, args=(client_socket,)).start()

    def handle_connection(self, client_socket):
        try:
            data = client_socket.recv(4096).decode()
            json_start = data.find('{')
            json_str = data[json_start:]
            data = json.loads(json_str)
            self.update_data(data)

        except Exception as e:
            print(f"Error handling connection: {e}")

        finally:
            client_socket.close()

    def update_data(self, data):
        self.attack = data['attack']
        self.player_name = data['playerName']
        self.tick = data['tick']
        self.run_energy = data['runEnergy']
        self.special_attack = data['specialAttack']
        self.equipment_stats = data['equipmentStats']
        self.equipment = data['equipment']
        self.inventory = data['inventory']
        self.skills = data['skills']
        self.prayers = data['prayers']
        self.local_point = data['localPoint']
        self.world_point = data['worldPoint']
        self.camera = data['camera']

if __name__ == '__main__':
    host = 'localhost'
    port = 12347
    osrs_listener = OsrsSocket(host, port)
    osrs_listener.start()

    while True:
        print(osrs_listener.run_energy)
        print(osrs_listener.prayers)
