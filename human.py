# -*- coding: utf-8 -*-
"""

@author: IATECH

"""
from player import Player
from conversion import card_to_ranksuit, ranksuit_to_card


class Human(Player):
    def __init__(self, score, identite, connexion):
        Player.__init__(self, score, identite)
        self.conn = connexion

    def play(self, trick):
        """Demande à GameClient de choisir une carte"""
        txt = "joue;" + str(self.identite)
        for card in self.playable_cards(trick):
            rank, suit = card_to_ranksuit(card)
            txt += ";"+suit+str(rank)
        self.conn.send(txt.encode('utf-8'))
        ans = self.conn.recv(1024).decode().split(',')
        if len(ans)== 2:
            card = ranksuit_to_card(ans[0], ans[1])
            print(ans)
            print(card)
            print(self.hand)
            self.hand.remove(card)
            return card
        else:
            print("Carte non identifiable")

    def bid(self, bid):
        """Demande à GameClient de choisir une prise"""
        txt = "prise," + str(self.identite) + ","+ str(bid)
        self.conn.send(txt.encode('utf-8'))
        ans = self.conn.recv(1024).decode().split(',')
        if len(ans) == 3 and ans[0] == "prise" and int(ans[1]) == self.identite:
            return int(ans[2])
        else:
            print("Prise non identifiable")

    def ecart(self):
        txt = "ecart," + str(self.identite)
        for card in self.playable_cards_dog():
            rank, suit = card_to_ranksuit(card)
            txt += ";"+suit+str(rank)
        self.conn.send(txt.encode('utf-8'))
        ecart = []
        for i in range(6):
            ans = self.conn.recv(1024).decode().split(',')
            if len(ans)== 2:
                ecart.append(ranksuit_to_card(ans[0], ans[1]))
            else:
                print("Carte non identifiable")
        return ecart
