import socket
import json

# Example Responce #
'''
Received: POST /log HTTP/1.1
Content-Type: application/json; charset=utf-8
Content-Length: 1816
Host: localhost:12346
Connection: Keep-Alive
Accept-Encoding: gzip
User-Agent: okhttp/3.14.9

{'packetType':'inventory',
'playerName':'Cursed Nm',
'tick':870,'
runEnergy':10000,
'specialAttack':0,
'attack':{'isAttacking':false,
'animationName':'N/A',
'animationId':-1, 
'animationIsSpecial':false,
'animationBaseSpellDmg':0},
'equipmentStats':{'aStab':26,'aSlash':-2,'aCrush':24,'aMagic':-30,'aRange':-10,'dStab':41,'dSlash':41,'dCrush':30,'dMagic':-6,'dRange':40,'str':29,'rStr':0,'mDmg':0},
'equipment':[{'index':0,'id':26969,'amount':1,'name':'Circlet of water'},
{'index':2,'id':6707,'amount':1,'name':'Camulet'},
{'index':3,'id':1275,'amount':1,'name':'Rune pickaxe'},
{'index':4,'id':13105,'amount':1,'name':'Varrock armour 2'},
{'index':7,'id':12015,'amount':1,'name':'Prospector legs'},
{'index':10,'id':12016,'amount':1,'name':'Prospector boots'},
{'index':13,'id':22947,'amount':1,'name':'Rada\u0027s blessing 4'}],
'inventory':[
{'index':0,'id':1275,'amount':1},
{'index':1,'id':20590,'amount':1},
{'index':4,'id':12179,'amount':1}],
'skills':[
{'skillName':'ATTACK','experience':14666173,'boostedLevel':99,'realLevel':99},
{'skillName':'STRENGTH','experience':15258749,'boostedLevel':99,'realLevel':99},
{'skillName':'DEFENCE','experience':13628745,'boostedLevel':99,'realLevel':99},
{'skillName':'RANGED','experience':12291804,'boostedLevel':98,'realLevel':98},
{'skillName':'MAGIC','experience':14452912,'boostedLevel':99,'realLevel':99},
{'skillName':'HITPOINTS','experience':22604604,'boostedLevel':99,'realLevel':99},
{'skillName':'PRAYER','experience':4519749,'boostedLevel':86,'realLevel':88},
{'skillName':'OVERALL','experience':183011911,'boostedLevel':1,'realLevel':1}],
'prayers':[],
'localPoint':{'x':6464,'y':7104,'sceneX':50,'sceneY':55},
'worldPoint':{'x':3218,'y':9623,'plane':0,
'regionID':12950,'regionX':18,'regionY':23},
'camera':{'yaw':2036,'pitch':252,'x':6420,'y':5892,'z':-1517,'x2':6420,'y2':-1517,'z2':5892}}
'''

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
