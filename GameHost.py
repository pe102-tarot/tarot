# -*- coding: utf-8 -*-
"""

@author: IATECH

"""
from conversion import card_to_ranksuit
from player import Player
from human import Human
from ia import IA
from card import Card
from trump import Trump
from excuse import Excuse
from database import Database
import socket, sys
import random


"""Variables à modifier avant de lancer le jeu"""
host = ''  # Ajouter l'adresse IP de l'ordinateur hôte entre les guillemets
port = 40000  # Garder cette valeur
nombre_humains =  2  # Nombre de joueurs humains, compris entre 0 et 4
nombre_manches = None  # Nombre de manches, None pour un nombre illimité


class GameHost():
    """fenêtre principale de l'application serveur"""
    def __init__(self, host, port, nb_clients, nb_manches = None):
        """
        nb_clients est le nombre d'humains, ie d'ordis, jouant ensemble
        nb_manches est le nombre de manches à jouer. Si ce nombre est donné,
        la partie ne s'arrête qu'après que toutes les manches aient été jouées
        """
        self.host, self.port = host, port
        # Variables d'une manche:
        self.database=Database()
        self.bidder = None
        self.bid = 0
        self.first_player = None
        self.dog = []
        self.attaque = []
        self.defense = []
        # Variables d'une partie:
        self.nb_manches = nb_manches
        self.manche = 0 # L'identifiant de la manche en cours
        self.dealer = random.randint(0, 3)
        self.nb_clients = nb_clients
        self.clients = []
        self.connect()
        self.players = []
        self.creer_joueurs()
        self.run()

    def connect(self):
        """Initialisation du serveur - Mise en place du socket"""
        mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        mySocket.settimeout(None)
        try:
            mySocket.bind((self.host, self.port))
        except socket.error:
            print("La liaison du socket à l'adresse choisie a échoué.")
            sys.exit()
        print("Serveur prêt, en attente de requêtes ...")
        mySocket.listen(5)
        # Attente et prise en charge des connexions demandées par les clients :
        for i in range(self.nb_clients):
            conn, adresse = mySocket.accept()  # Connexion avec un client
            print("Client connecté, adresse IP %s, port %s." %(adresse[0], adresse[1]) )
            conn.send("Vous êtes connecté.".encode('utf-8'))  # Dialogue avec le client
            self.clients.append(conn)

    def envoi(self, conn, txt):
        """Envoie un message à un client et attend une confirmation"""
        conn.send(txt.encode('utf-8'))
        assert conn.recv(1024).decode() == 'ok'

    def run(self):
        """Déroulement d'une manche"""
        self.donne()
        self.prise()
        if self.bid == 0:
            self.reset()
            self.run()
        else:
            self.chien()
            self.first_player = self.dealer + 1
            for i in range(18):
                trick = []
                for j in range(4):
                    index = (self.first_player+j) % 4
                    if isinstance(self.players[index], IA):
                        carte = self.players[index].play(trick, self.bidder, i, self.first_player)
                    elif isinstance(self.players[index], Human):
                        carte = self.players[index].play(trick)
                    self.database.actualiser(carte, trick, index)
                    print("Carte jouée", carte)
                    rank, suit = card_to_ranksuit(carte)
                    for conn in self.clients:
                        self.envoi(conn, "a_joue;"+str(index)+";"+str(rank)+";"+suit)
                    trick.append(carte)
                self.fin_pli(trick)
            self.fin_manche()

    def creer_deck(self):
        """Creates a tarot deck of 78 cards"""
        L=[]
        for i in range(1, 22):
            L.append(Trump(i))
        for suit in ('S', 'H', 'D', 'C'):
            for i in range(1, 15):
                L.append(Card(i, suit))
        L.append(Excuse())
        return L

    def creer_joueurs(self):
        """
        Crée les 4 joueurs (Humains et IAs et les répartit aléatoirement
        """
        liste = [i+1 for i in range(self.nb_clients)] + [0]*(4-self.nb_clients)
        random.shuffle(liste)
        for i, p in enumerate(liste):
            if p > 0:
                self.envoi(self.clients[p-1], "indice,"+str(i))
                self.players.append(Human(0, i, self.clients[p-1]))
            else:
                self.players.append(IA(0, i, self.database))

    def donne(self):
        """Crée un deck, le mélange et le distribue aux 4 joueurs"""
        self.dealer += 1
        # Crée un deck et le mélange:
        if self.nb_manches is None:
            seed = None
        else:
            seed = self.manche
        deck = self.creer_deck()
        random.Random(seed).shuffle(deck)
        self.manche += 1
        # Distribue les cartes aux joueurs:
        for player in self.players:
            main = []
            txt_main = "main,"+str(player.identite)+","
            for i in range(18):
                carte = deck.pop(-1)
                main.append(carte)
                rank, suit = card_to_ranksuit(carte)
                txt_main += str(rank)+","+suit+","
            # Informe les clients
            for conn in self.clients:
                self.envoi(conn, txt_main)
            # On donne sa main au joueur
            player.hand = main
        # Créé le chien avec les cartes restantes
        self.dog = deck
        assert len(self.dog) == 6
        txt="chien"
        for carte in self.dog:
                rank, suit = card_to_ranksuit(carte)
                txt += ";"+str(rank)+","+suit
        # Informe les clients
        for conn in self.clients:
            self.envoi(conn, txt)

    def prise(self):
        """
        Permet le choix des prises
        """
        temp_bidder = None
        for i in range(4):
            index = (self.dealer + i) % 4
            temp_bid = self.players[index].bid(self.bid)
            for conn in self.clients:
                self.envoi(conn, "a_pris,"+str(index)+","+str(temp_bid))
            if temp_bid > self.bid:
                self.bid = temp_bid
                temp_bidder = index
                print("Joueur {} a surenchéri".format(index))
            elif temp_bid == 0:
                print("Joueur {} a passé".format(index))
            else:
                print("Erreur: prise illégale")
        self.bidder = temp_bidder
        for conn in self.clients:
            self.envoi(conn, "bidder,"+str(self.bidder)+","+str(self.bid))

    def chien(self):
        """
        Permet le choix du chien
        """
        if self.bid == 1 or self.bid == 2:
            for conn in self.clients:###!!
                self.envoi(conn, "afficher_chien")
            self.players[self.bidder].hand += self.dog
            ecart = self.players[self.bidder].ecart()
            txt="ecart_fait;"+str(self.bidder)
            for card in ecart:
                self.players[self.bidder].hand.remove(card)
                a, b = card_to_ranksuit(card)
                txt += ";"+str(a)+";"+b
            for conn in self.clients:#!!!
                self.envoi(conn, txt)
        elif self.bid == 3 or self.bid == 4:
            if self.bid == 3:
                self.attaque += self.dog
            else:
                self.defense += self.dog
            for conn in self.clients:
                self.envoi(conn, "pas_chien")

    def fin_pli(self, trick):
        """
        Détermine le gagnant du pli
        """
        indice = Player.best_card(trick)
        winner = (self.first_player+indice) % 4
        for i, card in enumerate(trick):
            # On néglige le cas ou l'Excuse est jouée au dernier tour
            if isinstance(card, Excuse):
                if (self.first_player+i) % 4 == self.bidder:
                    self.attaque.append(trick.pop(i))
                else:
                    self.attaque.append(trick.pop(i))
        print("Le gagnant du pli est", winner)
        self.first_player = winner
        if winner == self.bidder:
            print("L'attaque gagne le pli")
            self.attaque += trick
        else:
            print("La défense gagne le pli")
            self.defense += trick
        for conn in self.clients:
            self.envoi(conn, "fin_pli")
#        for conn in self.clients:
#            conn.send("fin-pli".encode('utf-8'))
#        for conn in self.clients:
#            assert conn.recv(1024).decode() == 'ok'

    def fin_manche(self):
        """
        Gère la fin de la manche
        """
        for conn in self.clients:
            self.envoi(conn, "fin_manche")
        msg = self.actualiser_score()
        if self.nb_manches is None or self.manche < self.nb_manches:
            for conn in self.clients:
                self.envoi(conn, "recommencer;"+msg)
            self.reset()
            self.run()
        else:
            true_winner = 0
            score = self.players[0].get_score()
            for i in range(1, 4):
                if self.players[i].get_score() > score:
                    score = self.players[i].get_score()
                    true_winner = i
            for conn in self.clients:
                self.envoi(conn, "fin_partie;"+msg+";"+str(true_winner))
            print("C'est fini pour GameHost")

    def reset(self):
        """Variables d'une manche remises à zero"""
        self.database=Database()
        self.bidder = None
        self.bid = 0
        self.first_player = None
        self.dog = []
        self.attaque = []
        self.defense = []

    def result(self,oulders, points, bonus_bidder, bonus_def):
        """
        Return the scoring points that each player gives to the bidder
        The bonuses are not counted here.
        """
        multiplier= {1:1,2:2,3:4,4:6}[self.bid]
        # g est la différence avec l'annonce
        if oulders == 3:
            g = points-36
        elif oulders == 2:
            g = points-41
        elif oulders == 1:
            g = points-51
        else:
            g = points-56
        # s est le nombre de points que la défense va donner à l'attaquant
        if g<0:
            s=(g-25+bonus_bidder-bonus_def)*multiplier
        else:
            s=(g+25+bonus_bidder-bonus_def)*multiplier
        b = g>=0
        return int(s), b

    def actualiser_score(self):
        print("\n---------------------------------\n")
        print(" La partie est terminée")
        points = 0 # Somme des points des cartes de l'attaquant
        oulders = 0 # Bouts gagnés par l'attaquant
        n = len(self.attaque)
        bonus_bidder = 0
        cards = self.attaque
        excuse = False # Gestion spéciale de l'excuse
        for i in range(n):
            points += cards[i].get_point()
            # On compte les bouts:
            if cards[i].get_oulder() == 1:
                oulders += 1
                if isinstance(cards[i], Excuse):
                    excuse = True
            # Petit au bout:
            if n-i < 4 and isinstance(cards[i], Trump) and cards[i].get_rank() == 1:
                bonus_bidder += 10
        if points != points//1:
            if excuse:
                points -= 0.5
            else:
                points += 0.5
        cards = self.defense
        bonus_def = 0
        for i in range(1, 5):
            if isinstance(cards[-i], Trump) and cards[-i].get_rank() == 1:
                bonus_def+=10
        print("Points : ", points,"Oulders : ", oulders)
        s, b = self.result(oulders, points, bonus_bidder, bonus_def)
        if b:
            renvoi = str(self.bidder)+";"
        else:
            renvoi = 'D;'
        for i in range(4):
            if i==self.bidder:
                self.players[i].set_score(3*s)
            else:
                self.players[i].set_score(-s)
        with open("score/score.txt","a+") as score_file:
            score_file.write("Manche "+str(self.manche)+" :\n")
            for i in range(4):
                a = str(self.players[i].get_score())
                score_file.write("Joueur"+str(i)+" a "+a+" points.\n")
                renvoi += a+","
        return renvoi


if __name__ =='__main__':
    GameHost(host, port, nombre_humains, nombre_manches)
