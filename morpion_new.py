#! /usr/bin/python3

import socket, sys, threading

connexions_clients = {} # dictionaire des connexions clients
nombre_clients = 0

def serveur():

    global nombre_clients

    # Création du socket :
    connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connexion_principale.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Liaison du socket à une adresse précise
    try:
        connexion_principale.bind((HOTE, PORT))
    except socket.error:
        print("La liaison du socket à l'adresse choisie a échoué.")
        sys.exit()

    # Attente de la requete de connexion d'un client :
    print("Serveur pret, en attente de requetes ...")
    connexion_principale.listen(5)

    # Prise en charge des connexions demandées par les clients :
    while 1:        
        # Etablissement de la connexion :
        connexion, adresse = connexion_principale.accept()
        
        # Mémoriser la connexion dans le dictionnaire :
        nombre_clients = nombre_clients + 1
        connexions_clients[str(nombre_clients)] = connexion
        print("Client {} connecté, adresse IP {}, port {}.".format(str(nombre_clients), adresse[0], adresse[1]))
 
        # Dialogue avec les clients
        message_client = "Vous etes connecte. Envoyez vos messages."
        message_client_bytes = message_client.encode()
        connexion.send(message_client_bytes)
        print(connexions_clients[str(nombre_clients)])


def client():
    # 1) création du socket :
    connexion_au_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 2) Envoi d'une requete de connexion au serveur :
    try:
        connexion_au_serveur.connect((HOTE, PORT))
    except socket.error:
        print("La connexion a échoué.")
        sys.exit()
    print("Connexion établie avec le serveur.")

    # 3) Dialogue avec le serveur :    
    while 1:
        message_serveur_bytes = connexion_au_serveur.recv(1024)
        message_serveur = message_serveur_bytes.decode()
        print(message_serveur)


    # 4) Fermer la connexion :
    print("Fin de la connexion")
    connexion_au_serveur.close()

PORT = 2345
if len(sys.argv) < 2:
    HOTE = ''
    serveur()
else:
    HOTE = sys.argv[1]
    client()