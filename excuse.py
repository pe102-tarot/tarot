# -*- coding: utf-8 -*-
"""

@author: IATECH

"""
from playing_card import PlayingCard


class Excuse(PlayingCard):
    """
    The Fool or Excuse
    Rank: 0
    Point: 4.5
    """
    def __init__(self):
        PlayingCard.__init__(self, 0, 4.5, 1)

    def __eq__(self, other):
        if isinstance(other, Excuse):
            return True
        else:
            return False

    def __str__(self):
        return "Excuse"

    def __repr__(self):
        return "Excuse()"
