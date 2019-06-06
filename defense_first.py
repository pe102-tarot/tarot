# -*- coding: utf-8 -*-
"""

@author: IATECH

"""
from card import Card
from trump import Trump
from excuse import Excuse


def play_def_first(self, trick, bidder):
    """Order: Trumps, Hearts, Spades, Diamonds, Clovers"""
    print('[play_def_first 313]  hello from IA first ')
    playable_cards = self.hand[:]
    #print(playable_cards)
    spa = []
    hea = []
    dia = []
    clo  = []
    playable_cards_list = [spa,hea,dia,clo]

    for i in playable_cards:
        if isinstance(i, Trump) or isinstance(i, Excuse):
            pass
        elif i.get_suit() == 'S' :
                spa.append(i)
        elif i.get_suit() == 'H' :
                hea.append(i)
        elif i.get_suit() == 'D' :
                dia.append(i)
        elif i.get_suit() == 'C' :
                clo.append(i)

    #print(spa)
    #print(hea)
    #print(dia)
    #print(clo)

    len_min = 30
    cartes_coupes = []
    for i in range(4):

        #print(len(playable_cards_list[i]))
        if len(playable_cards_list[i]) < len_min and len(playable_cards_list[i]) != 0:

            cartes_coupes = []
            len_min = len(playable_cards_list[i])

            cartes_coupes.extend(playable_cards_list[i])
            #print('YES',i,len_min,cartes_coupes)

        elif len(playable_cards_list[i]) == len_min:
            cartes_coupes.extend(playable_cards_list[i])
            #print('YESYES',i,len_min,cartes_coupes)


    if presence_roi(self,playable_cards,bidder)[0]:
        return presence_roi(self,playable_cards,bidder)[1]

    if presence_reine(self,playable_cards,bidder)[0]:
        return presence_reine(self,playable_cards,bidder)[1]

    if presence_chevalier(self,playable_cards,bidder)[0]:
        return presence_chevalier(self,playable_cards,bidder)[1]

    if presence_valet(self,playable_cards,bidder)[0]:
        return presence_valet(self,playable_cards,bidder)[1]


    if len_min < 3:
        if jouer_coupe(cartes_coupes)[0]:
            return jouer_coupe(cartes_coupes)[1]
    if True:
        return pire_carte(playable_cards)


def pire_carte(l):
    #print('[def first 64]  hello from pire carte ')
    rank_min = 25
    presence_card = False
    for i in enumerate(l):
        if isinstance(i[1], Card) :
            presence_card = True

            if i[1].get_rank() < rank_min:

                rank_min = i[1].get_rank()

                position_pire_carte = i[0]
    if presence_card:
        return l[position_pire_carte]
    else:
        position_atout_min = 0
        for el in enumerate(l):
            if isinstance(el[1], Trump):
                if el[1].get_rank() < rank_min:
                    rank_min = el[1].get_rank()
                    position_atout_min = el[0]
        return l[position_atout_min]


def jouer_coupe(l):
    rank_min = 20
    for j in enumerate(l):
            if j[1].get_rank() < rank_min:
                rank_min = j[1].get_rank()
                position_pire_carte = j[0]
    if rank_min > 10:
        #print('[def first 80]  hello from jouer_coupes Flase ')
        return False, l[position_pire_carte]
    else:
        #print('[def first 80]  hello from jouer_coupes true')
        return True, l[position_pire_carte]


def presence_roi(self, cards, bidder):
    #print('[def first 95]  hello from presence_roi ')
    for card in cards:
        if isinstance(card, Card):
            if card.get_rank()==14 and self.database.coupes[bidder][card.get_suit()] == False:
                return True, card
    return False , -1


def presence_reine(self, cards, bidder):
    #print('[def first 95]  hello from presence_reine ')
    for card in cards:
        if isinstance(card, Card):
            carte_maitre = self.database.carte_maitre(card.get_suit())
            if card.get_rank()==13 and carte_maitre < 14 and self.database.coupes[bidder][card.get_suit()] == False:
                #print(carte_maitre)
                return True, card
    return False , -1


def presence_chevalier(self, cards, bidder):
    #print('[def first 95]  hello from presence_chevalier ')
    for card in cards:
        if isinstance(card, Card):
            carte_maitre = self.database.carte_maitre(card.get_suit())
            if card.get_rank()==12 and carte_maitre < 13 and self.database.coupes[bidder][card.get_suit()] == False:
                #print(carte_maitre)
                return True, card
    return False , -1


def presence_valet(self, cards, bidder):
    #print('[def first 95]  hello from presence_valet ')
    for card in cards:
        if isinstance(card, Card):
            carte_maitre = self.database.carte_maitre(card.get_suit())
            if card.get_rank()==11 and carte_maitre < 12 and self.database.coupes[bidder][card.get_suit()] == False:
                #print(carte_maitre)
                return True, card
    return False , -1
