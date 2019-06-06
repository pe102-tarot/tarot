# -*- coding: utf-8 -*-
"""

@author: IATECH

"""
from player import Player
from excuse import Excuse
from trump import Trump
from defense_first import play_def_first
from defense_not_first import play_def_not_first
from attack import play_attaque
from random import random


class IA(Player):
    def __init__(self, score, identite, database):
        Player.__init__(self, score, identite)
        self.database = database

    def play(self, trick, bidder, j, first_player):
        """trick est une liste d'objets Card"""
        """bidder et first_player des int (indices pour joueurs)"""
        """j est le numéro du pli en cours"""
        print('[IA23]  le pli est:', trick)
        if self.identite == bidder:
            # L'IA attaque
            card = play_attaque(self, trick)
            print("[IA28]  IA attaque avec", card)
        else:
            # L'IA défend
            if len(trick) == 0: #IA 1º joueur du pli
                print('[IA32]  hello from IA - len(trick) == 0')
                card = play_def_first(self, trick, bidder)
            else :
                print('[IA36]  hello from IA - len(trick) != 0')
                card = play_def_not_first(self, trick, bidder, j, first_player)
                print('[IA38]  from IA fin DefenseNoFirst_play la card est:',card)
        self.hand.remove(card)
        return card

    def bid(self, bid):
        """Pour comprendre cette fonction, se réfèrer au tableau Wikipédia"""
        points = 0  # Nombre de points attribués à la main
        trumps = 0  # Nombre d'atouts dans la main
        points_garde = 0 # points comptabilisé que pour  garde sans/contre
        petit = False
        hearts = []
        clovers = []
        diamonds = []
        spades = []
        mayor_trump = []
        # A est un dictionnaire permettant de trier les cartes par couleur
        A = {'S': spades, 'H': hearts, 'D': diamonds, 'C': clovers}
        for card in self.get_hand():
            if isinstance(card, Trump):
                trumps += 1  # On compte un atout en plus
                if card.get_rank() > 15:  # 2 pts en + pour les gros Atouts
                    points += 2
                    mayor_trump.append(card.get_rank())  #liste des ranks des mayor trumps
                elif card.get_rank() == 1:  # Présence du petit
                    petit = True
                if card.get_rank() == 21:  # Le 21 vaut 10 pts
                    points += 10
            elif isinstance(card, Excuse):  # L'Excuse vaut 8 pts
                points += 8
            else:
                A[card.get_suit()].append(card.get_rank())

                # on ajoute 1 points pour chaque mayor trump en séquence
        if len(mayor_trump) > 1:
            list.sort(mayor_trump)
            seq= False  # Pour savoir si les 2 cartes précédente était déjà en sequence
            for i in range (len(mayor_trump)-1):
                if (mayor_trump[i] - mayor_trump[i+1]) == -1:
                    if seq:
                        points +=1
                        seq=True
                    else:
                        points +=2
                        seq=True
                else:
                     seq=False

        if petit:  # Le petit vaut un nombre != de pts selon le nbre d'atouts
            if trumps == 4:
                points += 5
            elif trumps == 5:
                points += 7
            elif trumps > 5:
                points += 9
        if trumps > 4:  # 2 pts pour chaque atout s'ils sont assez nombreux
            points += 2*trumps

        for couleur in ['H', 'S', 'D', 'C']:  # Des pts pour les suites
            liste = A[couleur]
            if len(liste) == 5:
                points += 5
            elif len(liste) == 6:
                points += 7
            elif len(liste) > 6:
                points += 9
            elif len(liste) == 0:
                points_garde += 6
            elif len(liste) == 1:
                points_garde += 3
            if (14 in liste and 13 in liste): #10 pts pour K et Q de même couleur
                points +=10
                liste.remove(13)
                liste.remove(14)
            for rank in liste:
                if  rank == 14:  # 6 pts pour chaque Roi
                    points += 6
                elif rank == 13:  # 3 pts pour chaque Dame
                    points += 3
                elif rank == 12:  # 2 pts pour chaque Cavalier
                    points += 2
                elif rank == 11:  # 1 pt pour chaque Valet
                    points += 1
        points = points*(0.9+0.2*random())  # On ajoute un peu de hasard

        if (points + points_garde) > 80 and bid < 4:
            return 4
        elif (points + points_garde) > 70 and bid < 3:
            return 3
        elif points > 55  and bid < 2:
            return 2
        elif points > 39 and bid < 1:
            return 1
        else:
            return 0

    def ecart(self):
        """
        Les cartes ne sont pas retirées de la main par cette fonction
        C'est GameHost qui s'en occupe
        """
        ecart = []
        spa, point_S = [False], 0
        hea, point_H = [False], 0
        dia, point_D = [False], 0
        clo, point_C = [False], 0
        tru = 0
        for i in self.get_hand() :
            if isinstance(i, Trump) or isinstance(i, Excuse):
                tru+=1
            elif i.get_suit() == 'S' :
                if i.get_rank() == 14:
                    spa[0]=True
                else :
                    point_S+=i.get_point()
                    spa.append(i)
            elif i.get_suit() == 'H' :
                if i.get_rank() == 14:
                    hea[0]=True
                else :
                    point_H+=i.get_point()
                    hea.append(i)
            elif i.get_suit() == 'D' :
                if i.get_rank() == 14:
                    dia[0]=True
                else :
                    point_D+=i.get_point()
                    dia.append(i)
            else:  # i.get_suit() == 'C'
                if i.get_rank() == 14:
                    clo[0]=True
                else :
                    point_C+=i.get_point()
                    clo.append(i)
        point = [point_S,point_H,point_D,point_C]
        fam = [spa,hea,dia,clo] # Les cartes pouvant être mise dans le chien
        leng = [len(spa)-1,len(hea)-1,len(dia)-1,len(clo)-1]

        # Premier cas points isolés
        for i in range(4):
            if leng[i]<4 and not(fam[i][0]):
                if point[i] > 2 :
                    for carte in fam[i][1:]:
                        fam[i].remove(carte)
                        ecart.append(carte)
                        if len(ecart)== 6 :
                            return ecart

        # Deuxième cas : coupe franche et/ou de singletons:
        leng = [len(spa)-1,len(hea)-1,len(dia)-1,len(clo)-1]
        #if tru > 5 :
        leng,fam = self.triSS(leng, fam)
        for i in range (4):
            for carte in fam[i][1:]:
                ecart.append(carte)
                fam[i].remove(carte)
                if len(ecart) == 6 :
                    return ecart
        if len(ecart) < 6:
            print("Ecart ne contient que",ecart,"cartes")
        else:
            print("erreur?")

    def triSS(self, leng, fam):
        #Classe les familles (couleurs) en fonction de la longueur
        for i in range(len(leng)):
            m = leng[i]
            j = i+1
            k=i
            while j<len(leng):
                if leng[j]<m:
                   k,m=j,leng[j]
                j+=1
            leng[i],leng[k]=leng[k],leng[i]
            fam[i],fam[k]=fam[k],fam[i]

        return leng, fam

    def triS(self, fam):
        #Classe les familles (couleurs) en fonction de la longueur
        if fam != [] :
            if isinstance(fam[0],Trump):
                for i in range(len(fam)):
                    if fam[i].get_rank() == 1 :
                        m = 0
                    else :
                        m = fam[i].get_point()
                    j = i+1
                    k=i
                while j<len(fam):
                    if fam[j].get_rank() == 1 :
                        m_j = 0
                    else :
                        m_j = fam[i].get_point()
                    if m_j < m :
                       k,m=j,m_j
                    j+=1
                fam[i],fam[k]=fam[k],fam[i]
            else :
                for i in range(len(fam)):
                    m = fam[i].get_point()
                    j = i+1
                    k=i
                    while j<len(fam):
                        if fam[j].get_point()<m:
                            k,m=j,fam[j].get_point()
                        j+=1
                    fam[i],fam[k]=fam[k],fam[i]
        return fam

    def tri(self,cards):
        ex = []
        spa = []
        hea = []
        dia = []
        clo = []
        trump =[]
        for i in cards :
            if isinstance(i, Trump) :
                trump.append(i)
            elif isinstance(i, Excuse) :
                ex.append(i)
            elif i.get_suit() == 'S' :
                spa.append(i)
            elif i.get_suit() == 'H' :
                hea.append(i)
            elif i.get_suit() == 'D' :
                dia.append(i)
            else:  # i.get_suit() == 'C'
                clo.append(i)
        spa = self.triS(spa)
        clo = self.triS(clo)
        dia = self.triS(dia)
        hea = self.triS(hea)
        trump = self.triS(trump)
        return dia+hea+clo+spa+trump+ex
