# -*- coding: utf-8 -*-
"""

@author: IATECH

"""
from trump import Trump
from card import Card
from excuse import Excuse


def card_to_ranksuit(card):
    """Convertit un objet Card en un rang et une suite"""
    if  isinstance(card, Excuse):
        return card.get_rank(), "Excuse"
    elif  isinstance(card, Trump):
        return card.get_rank(), "Trump"
    else:
        return card.get_rank(), card.get_suit()


def ranksuit_to_card(rank, suit):
    """Convertit un rang et une suite en objet Card"""
    if suit == "Excuse":
        return Excuse()
    elif suit == "Trump":
        return Trump(int(rank))
    else:
        return Card(int(rank), suit)
