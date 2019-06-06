# -*- coding: utf-8 -*-
"""

@author: IATECH

"""
from trump import Trump
from card import Card
from excuse import Excuse


class Player():
    """Abstract parent class for both IA and Human."""
    def __init__(self, score, identite):
        self.identite = identite
        self.__score= score
        self.hand = []

    def get_hand(self):
        return self.hand
    def set_hand(self, hand):
        self.hand = hand

    def get_score(self):
        return self.__score
    def set_score(self, score):
        """Add the score of a game to the total score."""
        self.__score+= score


    @staticmethod
    def best_card(cards):
        """
        Return the index of the best card in a list
        The first card defines the winning suit.
        This list is often a trick of two, three or four cards.
        The index (0, 1, 2, or 3) thus defines the winner of the trick
        """
        w_card=cards[0]
        w=0
        for i in range(1,len(cards)):
            if isinstance(w_card, Trump):
                if isinstance(cards[i], Trump) and cards[i]>w_card:
                    w_card, w=cards[i], i
            elif isinstance(w_card, Card):
                if isinstance(cards[i], Trump):
                    w_card, w=cards[i], i
                elif isinstance(cards[i], Card) and cards[i].get_suit()==w_card.get_suit() and cards[i].get_rank()>w_card.get_rank():
                    w_card, w=cards[i], i
            elif isinstance(w_card, Excuse):
                w_card, w=cards[i], i
        return w

    def playing_trump(self, trick):
        '''
        Vérifie si la main contient des atouts, si ce n'est pas le cas,
        elle renvoie toute la main du joueur en tant que cartes jouables,
        sinon renvoie une liste d'atouts supérieurs au précédent atout joué
        !! Il faut gérer le cas où l'atout précédemment joué est trop grand !!

        '''
        hand=self.get_hand()[:]
        L=[el for el in hand if isinstance(el,Trump)]

        if L==[]:
            K=[]
            for el in hand :
                if isinstance(el, Card):
                    K.append(el)
            return K
        else:
            best_trump=0
            if isinstance( trick[Player.best_card(trick)], Trump) :
                best_trump=trick[Player.best_card(trick)].get_rank()
            K=[el for el in L if el.get_rank()>best_trump]
        if K==[]:
            return L
        else:
            return K

    def playable_cards(self, trick):
        hand=self.get_hand()[:]
        ex=[]
        for el in hand:
            if isinstance(el,Excuse):
                ex=[el]
        if trick==[]:
            return hand #Si dans le tas de cartes jouées il n'y a rien on peut tout jouer

        elif isinstance(trick[0], Trump):
            #Si la premiere carte est un atout, on doit jouer un atout,
            #si on en a pas, n'importe quelle carte
            #On ajoute l'excuse aux cartes jouables
            return self.playing_trump(trick)+ex

        elif isinstance(trick[0], Card):
            #Si on ne joue pas atout, on regarde quelle couleur est jouée
            suit=trick[0].get_suit()

            #!!! N'implique pas forcément de jouer au dessus de la dernière carte
            L=[el for el in hand if (isinstance(el,Card) and el.get_suit()==suit)]
            if L==[]:
                #Si on a pas de cartes, on joue atout
                return self.playing_trump(trick)+ex
            else :
                #Si on a, on joue la couleur
                return L+ex
        elif isinstance(trick[0], Excuse):
            return self.playable_cards(trick[1:])

    def playable_cards_dog(self):
        hand = self.hand[:]
        playable = []
        for c in hand:
            if isinstance(c, Card) and c.get_rank() != 14:
                playable.append(c)
        return playable
