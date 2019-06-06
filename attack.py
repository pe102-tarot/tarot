# -*- coding: utf-8 -*-
"""

@author: IATECH

"""
from player import Player
from trump import Trump
from card import Card
from excuse import Excuse


def yes_I_can(self,best_card, playable_cards):
    """Renvoie la possibilité de remporter le pli en cours
    (sur les cartes visibles)"""
    j=0
    Test =[best_card,playable_cards[j]]
    i = Player.best_card(Test)
    if i == 0 :
        j += 1
        while i ==0 and j < len(playable_cards):
            Test =[ best_card,playable_cards[j]]
            i = Player.best_card(Test)
            j += 1
        if i==1:
            return i==1
    return i==1


def risk_be_overtrumped(self,playable_cards,n,color):
    alpha = 0
    color = str(color)
    ID=self.identite-1
    for i in range(int(n)) :
        if self.database.coupes[(i+ID)%4][color] :
            trump = self.database.coupes[(i+ID)%4]['max_trump']
            if not(yes_I_can(self,Trump(trump),playable_cards)) :
                if alpha < 1-(len(playable_cards)+1)/(len(self.database.dico['T'])+1):
                    alpha =1-(len(playable_cards)+1)/(len(self.database.dico['T'])+1)
        else :
            if alpha < (1-(len(playable_cards)+1)/(len(self.database.dico['T'])+1))/2:
                alpha = (1-(len(playable_cards)+1)/(len(self.database.dico['T'])+1))/2
    return alpha


def risk_be_trumpdefeated(self, playable_cards,n):
    alpha = 0
    ID=self.identite-1
    for i in range(int(n)) :
        trump = self.database.coupes[(i+ID)%4]['max_trump']
        if not(yes_I_can(self,Trump(trump),playable_cards)) :
            alpha =1-(len(playable_cards)+1)/(len(self.database.dico['T'])+1)
    return alpha


def risk_be_trumped(self,playable_cards,color,n):
    alpha = 0
    color = str(color)
    ID=self.identite-1
    for i in range(int(n)) :
        if self.database.coupes[(i+ID)%4][color] :
            alpha = 1
    if alpha != 1 :
        if self.database.dico[color] == []:
            return 1
        if not(yes_I_can(self,Card(self.database.dico[color][-1],color),playable_cards)):
            return 1
        else :
            return (len(playable_cards)+1)/(len(self.database.dico[color])+1)
    return alpha


def play_attaque(self, trick):
    alpha = 0.5
    playable_cards = self.playable_cards(trick)
    #playable_cards = tri(playable_cards,database)
    #j'ai considéré que les cartes étaient triées dans
    #l'ordre décroissant de leur valeur (avec l'excuse au bout)


    # IA joue en dernier on part sur maximiser les points
    if len(trick) == 3 :
        best_card = trick[Player.best_card(trick)]
        if yes_I_can(self,best_card, playable_cards) :
            return playable_cards[0]
        else :
            return playable_cards[-1]

    #IA joue en 2 ou 3
    elif len(trick) != 0:
        best_card = trick[Player.best_card(trick)]
        n = 4-len(trick)-1
        if isinstance(playable_cards[0],Trump) :
            if not (isinstance (trick[0],Trump)) and not(isinstance (trick[0],Excuse)) :
                color = trick[0].get_suit()
                if yes_I_can(self,best_card, playable_cards):
                    if risk_be_overtrumped(self,playable_cards,n,color) < alpha:
                        return  playable_cards[0]
            else :
                if yes_I_can(self,best_card, playable_cards):
                    if risk_be_trumpdefeated(self,playable_cards,n) < alpha :
                        return playable_cards[0]
                    else :
                        return  playable_cards[-1]
        else :
            if isinstance(best_card,Trump):
                return playable_cards[-1]
            #Cas particulier de l'excuse
            else :
                if not (isinstance (trick[0],Excuse)):
                    color = trick[0].get_suit()
                else :
                    if len(trick) == 1 :
                        return playable_cards[0]
                    else :
                       color = trick[1].get_suit()


                if yes_I_can(self,best_card, playable_cards):
                    if  risk_be_trumped(self,playable_cards,color,n) < alpha:
                        return playable_cards[0]
                    else :
                        return playable_cards[-1]
    else :
        return playable_cards[0]
    return  playable_cards[-1]
        #return tri_efficace(playble_cards)[0]



def tri_efficace(self,playable_cards):
    ID=self.identite-1
    ex = []
    if self.database.dico['S'] !=[]:
        spa, M_S = [], self.database.dico['S'][-1]
    else :
        spa, M_S = [], 20
    if self.database.dico['H'] !=[]:
        hea, M_H = [], self.database.dico['H'][-1]
    else :
        hea, M_H = [], 20
    if self.database.dico['D'] !=[]:
        dia, M_D = [], self.database.dico['D'][-1]
    else :
        dia, M_D = [], 20
    if self.database.dico['C'] !=[]:
         clo, M_C  = [],self.database.dico['C'][-1]
    else :
        clo, M_C = [], 20
    if self.database.dico['T'] !=[]:
        trump, M_T = [], self.database.dico['T'][-1]
    else :
        trump, M_T = [], 25


    for i in playable_cards :
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

    leng = [len(spa)-1,len(hea)-1,len(dia)-1,len(clo)-1, len(trump)-1]
    maxi = [M_S,M_H,M_D,M_C,M_T]
    fam=[spa, clo, dia, hea, trump]
    leng,fam = self.triSS(leng, fam)
    print(fam)
    leng = [len(spa)-1,len(hea)-1,len(dia)-1,len(clo)-1, len(trump)-1]
    leng,maxi = self.triSS(leng, maxi)

    if len(playable_cards)==2 :
        print(ex+fam[4]+fam[3]+fam[2]+fam[1]+fam[0],"2")
        return ex+fam[4]+fam[3]+fam[2]+fam[1]+fam[0]

    else:
        for i in range(5) :
            famille = fam[i]
            rank_max = maxi[i]
            if famille !=[] and famille[0].get_rank() > rank_max :
                if not isinstance(famille[0],Trump) :
                    color = famille[0].get_suit()
                    alpha = 0
                    for j in range(1,4) :
                        if not(self.datbase.coupe[(ID+j)%4][color]) :
                            alpha+=1
                    if alpha == 3 :
                        print(famille,"et 1")
                        return famille
                else :
                    if len(famille)>len(self.database.dico['T']//4):
                        if famille[-1].get_rank == 1:
                            print(famille+ex,"et 2")
                            return famille+ex
                        else :
                            print(famille,"et 3")
                            return famille
        print(fam[-1],"et raté")
        return fam[-1]

    return  playable_cards[-1]
