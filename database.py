# -*- coding: utf-8 -*-
"""

@author: IATECH

"""
from trump import Trump
from card import Card


class Database():
    def __init__(self):
        # Dictionnaire contenant des listes représentant les cartes non jouées
        self.dico = {'S': [i for i in range(1, 15)],
                     'H': [i for i in range(1, 15)],
                     'D': [i for i in range(1, 15)],
                     'C': [i for i in range(1, 15)],
                     'T': [i for i in range(1, 22)]
                     }
        self.excuse = False
        # Coupe à [spades, hearts, diamonds, clovers, trumps]
        # mex_trump: indique que le joueur
        # ne peut pas jouer au dessus d'un certain atout
        # max_trump = 0 -> le joueur n'a plus d'atout
        self.coupes = ({'S': False, 'H':  False, 'D':  False,
                        'C':  False, 'T':  False, 'max_trump': 21},
                       {'S': False, 'H':  False, 'D':  False,
                        'C':  False, 'T':  False, 'max_trump': 21},
                       {'S': False, 'H':  False, 'D':  False,
                        'C':  False, 'T':  False, 'max_trump': 21},
                       {'S': False, 'H':  False, 'D':  False,
                        'C':  False, 'T':  False, 'max_trump': 21},
                      )
        # Le chien a été révelé: on note les rois et les bouts qu'il contenait
        self.chien = []

    def actualiser(self, card, trick, player):
        """Pour chaque carte jouée, on actualise la database"""
        """Attention ! trick ne contient pas encore la dernière carte jouée !"""
        # Actualiser la liste des cartes non jouées est facile
        if isinstance(card, Card):
            print("[DB43] ", card, "joué")
            self.dico[card.get_suit()].remove(card.get_rank())
        elif isinstance(card, Trump):
            print("[DB46] ", card, "joué")
            self.dico['T'].remove(card.get_rank())
        else:
            if self.excuse: # Pour debug au cas où (Excuse est censée etre False)
                print("DATABASE : Excuse jouée 2 fois ??")
            print("[DB50]  Excuse jouée")
            self.Excuse = True
        # Actualiser les coupes est plus complexe
        if len(trick) > 0:
            self.actualiser_coupes(card, trick, player)

    def actualiser_coupes(self, card, trick, player):
        # On regarde en premier lieu la première carte du pli
        if isinstance(trick[0], Card):
            if isinstance(card, Card) and card.get_suit() != trick[0].get_suit():
                # Ca a coupé !
                # Pour debug
                print("[DB63]  Joueur", player, "coupe à", trick[0].get_suit())
                self.coupes[player][trick[0].get_suit()] = True
                # Mais ca manque surtout d'atout !
                print("[DB67]  Joueur", player, "n'a plus d'atout")
                self.coupes[player]['T'] = True
                self.coupes[player]['max_trump'] = 0
            elif isinstance(card, Trump):
                # Ca a coupé !
                # Pour debug
                print("[DB72]  Joueur", player, "coupe à", trick[0].get_suit())
                self.coupes[player][trick[0].get_suit()] = True
                # Faut voir si ça n'a pas sous-joué
                self.sous_atout(card.get_rank(), trick, player)
        elif isinstance(trick[0], Trump):
            if isinstance(card, Card):
                # Il n'a plus d'atout !
                print("[DB80]  Joueur", player, "n'a plus d'atout")
                self.coupes[player]['T'] = True
                self.coupes[player]['max_trump'] = 0
            elif isinstance(card, Trump):
                # Ca n'a pas coupé, mais faut voir si ça n'a pas sous-joué
                self.sous_atout(card.get_rank(), trick, player)
        else:
            # La première carte est l'Excuse, on ignore la première carte
            if len(trick) > 1:
                self.actualiser_coupes(card, trick[1:], player)

    def sous_atout(self, val, trick, player):
        """
        Fonction appelée par actualiser_coupes
        val la valeur de l'atout joué par le joueur
        trick le pli joué avant que le joueur ne joue
        """
        atouts = [c.get_rank() for c in trick if isinstance(c, Trump) and c.get_rank() > val]
        # La liste des atouts plus grands que celui joué par le joueur
        if len(atouts) > 0:
            # Le joueur a sous-coupé, mais avait-il déjà sous-coupé avant ?
            max_atout = max(atouts)
            if self.coupes[player]['max_trump'] > max_atout:
                self.coupes[player]['max_trump'] = max_atout
                print("[DB94]  Joueur", player, "a joué en dessous du",  max_atout, "d'atout")

    def carte_maitre(self, suit):
        """Détermine la meilleure carte restant en jeu à une couleur donnée"""
        if len(self.dico[suit]) > 0:
            return self.dico[suit][-1]
        else:
            return 0

# Chemin d'accès type: self.database.dico[card.get_suit()][-1]
