# -*- coding: utf-8 -*-
"""

@author: IATECH

"""
from playing_card import PlayingCard


class Trump(PlayingCard):
    """Trump Cards"""
    def __init__(self, n):
        PlayingCard.__init__(self, n)
        if n==1 or n==21:
            self.set_point(4.5)
            self.set_oulder(1)

    def __str__(self):
        return "{} d'Atout".format(self.get_rank())

    def __repr__(self):
        return "Trump({})".format(self.get_rank())

    def __eq__(self, other):
        if isinstance(other, Trump):
            return self.get_rank() == other.get_rank()
        else:
            return False

    def __lt__(self, other):
        """Rich comparison method. Since two cards are always differents,
        only strict inferiority and strict superiority need to be implemented.
        This may not be very useful because at least one of the 2 cards must be
        a Trump for the comparison to work. But if L is a list of Trump cards,
        sorted(L) will return a correctly sorted list"""
        if isinstance(other,Trump):
            return self.get_rank() < other.get_rank()
        else:
            return False

    def __gt__(self, other):
        """Rich comparison method. Since two cards are always differents,
        only strict inferiority and strict superiority need to be implemented.
        This may not be very useful because at least one of the 2 cards must be
        a Trump for the comparison to work. But if L is a list of Trump cards,
        sorted(L) will return a correctly sorted list"""
        if isinstance(other,Trump):
            return self.get_rank() > other.get_rank()
        else:
            return True
