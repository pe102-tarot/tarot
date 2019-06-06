# -*- coding: utf-8 -*-
"""

@author: IATECH

"""
from interface import Interface
from conversion import ranksuit_to_card
import socket, sys


"""Variables à modifier avant de lancer le jeu"""
host = ''  # Ajouter l'adresse IP de l'ordinateur hôte entre les guillemets
port = 40000 # Garder cette valeur
cartes_visibles = False # Garder False pour une partie normale


class GameClient(Interface):
    """fenêtre principale de l'application serveur"""
    """ Possède en attribut Interface, ThreadEmission, ThreadReception"""
    def __init__(self, host, port, cartes_visibles):
        self.host, self.port = host, port
        Interface.__init__(self, cartes_visibles)
        self.indice=0
        self.indice_bidder=0
        self.connexion= None
        self.chien=[]
        self.connect()
        self.bind('<KeyPress-s>',self.launch)

    def connect(self):
        # Programme principal - Établissement de la connexion :
        self.connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.connexion.connect((self.host, self.port))
        except socket.error:
            print ("La connexion a échoué.")
            sys.exit()
        print ("Connexion établie avec le serveur.")
        message_recu = self.connexion.recv(1024)
        message_decode = message_recu.decode()
        print (message_decode)



    def recevoir_indice(self,txt):
        ind=int(txt[1])
        self.indice=ind



    def reproduire_main(self,txt):
        hand=[]
        n=int(txt[1])
        for i in range(18):
            hand.append(ranksuit_to_card(txt[2+i*2],txt[3+i*2]))
        self.ajouter_main((n-self.indice)%4,hand)




    def poser_carte(self,txt):
        n=int(txt[1])
        C=ranksuit_to_card(int(txt[2]),txt[3])
        print("n", n)
        self.jouer_carte((n-self.indice)%4,C)


    def poser_cartes_chien(self,txt) :
        n=int(txt[1])
        C1=ranksuit_to_card(int(txt[2]),txt[3])
        C2=ranksuit_to_card(int(txt[4]),txt[5])
        C3=ranksuit_to_card(int(txt[6]),txt[7])
        C4=ranksuit_to_card(int(txt[8]),txt[9])
        C5=ranksuit_to_card(int(txt[10]),txt[11])
        C6=ranksuit_to_card(int(txt[12]),txt[13])
        self.mettre_au_chien((n-self.indice)%4,C1)
        self.mettre_au_chien((n-self.indice)%4,C2)
        self.mettre_au_chien((n-self.indice)%4,C3)
        self.mettre_au_chien((n-self.indice)%4,C4)
        self.mettre_au_chien((n-self.indice)%4,C5)
        self.mettre_au_chien((n-self.indice)%4,C6)


    def launch(self, event):
        """Une seule fois par partie"""
        #recpetion indice pendant la création des joueurs
        message_recu = self.connexion.recv(1024)
        message_decode =  message_recu.decode()
        print (message_decode)
        txt = message_decode.split(',')
        assert txt[0]== "indice"
        self.recevoir_indice(txt)
        message="ok"
        self.connexion.send(message.encode('utf-8'))
        self.run()


    def run(self):
        """Une manche"""
        #distribution des cartes
        for i in range(4):
            message_recu = self.connexion.recv(1024)
            message_decode = message_recu.decode()
            print (message_decode)
            txt = message_decode.split(',')
            assert txt[0] == "main"
            self.reproduire_main(txt)
            message="ok"
            self.connexion.send(message.encode('utf-8'))



        message_recu = self.connexion.recv(1024)
        message_decode =  message_recu.decode()
        print (message_decode)
        txt_chien = message_decode.split(';')
        assert txt_chien[0] == "chien"
        self.chien = txt_chien[1:]
        print(self.chien)
        message="ok"
        self.connexion.send(message.encode('utf-8'))



        #gérer la prise
        for i in range(4):
            message_recu = self.connexion.recv(1024)
            message_decode =  message_recu.decode()
            print (message_decode)
            txt = message_decode.split(',')


            #à moi de parler
            if txt[0] == "prise" :
                bid = int(txt[2])

                self.choix_prise(bid)


                message="prise,"+str(self.indice)+ ',' + str(self.bid)
                print(message)
                self.connexion.send(message.encode('utf-8'))




                message_recu2 = self.connexion.recv(1024)
                message_decode2 =  message_recu2.decode()
                print (message_decode2)
                txt = message_decode2.split(',')
                self.afficher_prise((int(txt[1])-self.indice)%4,int(txt[2]))
                message="ok"
                self.connexion.send(message.encode('utf-8'))

            #un autre joueur parle

            elif txt[0]== "a_pris" :
                self.afficher_prise((int(txt[1])-self.indice)%4,int(txt[2]))
                message="ok"
                self.connexion.send(message.encode('utf-8'))



        #le bidder est déterminé
        message_recu = self.connexion.recv(1024)
        message_decode =  message_recu.decode()
        print (message_decode)
        txt = message_decode.split(',')

        assert txt[0]== "bidder"
        if txt[2]=="0":
            message="ok"
            self.connexion.send(message.encode('utf-8'))
            self.reset()
            self.run()

        else:
            self.indice_bidder = (int(txt[1])-self.indice)%4
            print("ici afficher bidder")

            self.afficher_bidder(self.indice_bidder)


        message="ok"
        self.connexion.send(message.encode('utf-8'))



        #affichage du chien
        message_recu = self.connexion.recv(1024)
        message_decode =  message_recu.decode()
        print (message_decode)
        txt = message_decode.split(',')
        if txt[0] == "afficher_chien" :
            self.afficher_chien(self.indice_bidder, self.chien)

            message="ok"
            self.connexion.send(message.encode('utf-8'))



            #gérer écart
            message_recu = self.connexion.recv(1024)
            message_decode = message_recu.decode()
            print (message_decode)
            txt = message_decode.split(';')
            if txt[0] == "ecart," +str(self.indice):

                for i in range(6) :


                    rank,suit = self.choix_carte(txt[2:]).split(',')
                    C= ranksuit_to_card(rank,suit)
                    self.mettre_au_chien(0,C)
                    message= rank + ',' +  suit
                    self.connexion.send(message.encode('utf-8'))


                message_recu = self.connexion.recv(1024)
                message_decode = message_recu.decode()
                print (message_decode)
                txt = message_decode.split(';')
                assert txt[0] == "ecart_fait"
                message="ok"
                self.connexion.send(message.encode('utf-8'))

            #un autre joeur a pris
            else :

                assert txt[0] == "ecart_fait"


                self.poser_cartes_chien(txt)
                message="ok"
                self.connexion.send(message.encode('utf-8'))

        else:
             assert txt[0] == "pas_chien"
             message="ok"
             self.connexion.send(message.encode('utf-8'))



        #nombre de pli différents
        for i in range(18):


            #gérer un pli
            for j in range(4):

                message_recu = self.connexion.recv(1024)
                message_decode = message_recu.decode()
                print (message_decode)
                txt = message_decode.split(';')


                #un autre joueur à jouer
                if txt[0]== "a_joue":
                    self.poser_carte(txt)
                    message="ok"
                    self.connexion.send(message.encode('utf-8'))



                elif txt[0]=="joue" :

                #à mon tour de jouer

                    assert int(txt[1]) ==self.indice
                    """jouer la carte grace à l'interface"""
                    rank,suit = self.choix_carte(txt[2:]).split(',')
                    message= rank + ',' +  suit
                    self.connexion.send(message.encode('utf-8'))


                    message_recu = self.connexion.recv(1024)
                    message_decode =  message_recu.decode()
                    print (message_decode)
                    txt = message_decode.split(';')
                    assert txt[0]=="a_joue"
                    self.poser_carte(txt)
                    message="ok"
                    self.connexion.send(message.encode('utf-8'))




            #gestion fin du tour
            message_recu = self.connexion.recv(1024)
            message_decode =  message_recu.decode()
            print (message_decode)
            txt = message_decode.split(',')
            assert txt[0] == "fin_pli"


            self.attente()
            self.ranger_pli()


            message="ok"
            self.connexion.send(message.encode('utf-8'))



        #gestion fin de manche
        message_recu = self.connexion.recv(1024)
        message_decode =  message_recu.decode()
        print (message_decode)
        txt = message_decode.split(',')
        assert txt[0] == "fin_manche"



        message="ok"
        self.connexion.send(message.encode('utf-8'))


        #gestion fin de partie/nouvelle manche
        message_recu = self.connexion.recv(1024)
        message_decode = message_recu.decode()
        print (message_decode)
        txt = message_decode.split(';')


        if txt[0] == "recommencer":
            message="ok"
            self.connexion.send(message.encode('utf-8'))
            self.afficher_score(txt[1],txt[2])
            self.reset()
            self.run()

        else :
            assert txt[0] == "fin_partie"
            message="ok"
            self.connexion.send(message.encode('utf-8'))
            self.afficher_score(txt[1],txt[2],txt[3])


if __name__ =='__main__':
    GameClient(host, port, cartes_visibles).mainloop()
