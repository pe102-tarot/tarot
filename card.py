# -*- coding: utf-8 -*-
"""

@author: IATECH

"""
from playing_card import PlayingCard


class Card(PlayingCard):
    """
    Spades, Hearts, Diamonds and Clovers
    Rank: from 1 to 14
    Point: 0.5 or 1.5 or 2.5 or 3.5 or 4.5
    Suit: 'S','H','D','C'
    """
    def __init__(self, n, s):
        PlayingCard.__init__(self, n)
        self.__suit = s
        if n>10:
            self.set_point(n-9.5)

    def get_suit(self):
        return self.__suit

    def __eq__(self, other):
        if isinstance(other, Card):
            return self.get_suit() == other.get_suit() and self.get_rank() == other.get_rank()
        else:
            return False

    def __str__(self):
        """Clever use of dictionnaries"""
        return "{} de {}".format({11:'Valet',12:'Cavalier',13:'Reine',14:'Roi'}
                                 .get(self.get_rank(),self.get_rank()),
                                 {'S':"Pique",'H':"Coeur",'D':"Carreau",'C':"Trèfle"}[self.__suit])

    def __repr__(self):
        return "Card({},'{}')".format(self.get_rank(), self.__suit)
