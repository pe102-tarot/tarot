# -*- coding: utf-8 -*-
"""

@author: IATECH

"""
from player import Player
from excuse import Excuse
from trump import Trump
from card import Card
import random as random


def play_def_not_first(self,trick, bidder, j,first_player):
    """
    fct générale appelée quand une IA en défense doit jouer un pli déjà commencé
    j est le nº du pli
    trick est une liste de Card
    """
    print('[DNF16]  hello from DefenseNoFirst')
    #print('[DNF17]  from dnf bidder = ',bidder)
    #print('[DNF18]  from dnf first_player = ',first_player)
    #print('[DNF19]  from dnf plie nº = ',j)
    playable_cards=self.playable_cards(trick)
    #print('[DNF21]  playables_cards= ',playable_cards)
    bidder_relatif = (bidder - first_player) % 4
    #print('[DNF24]  from dnf bidder_relatif = ',bidder_relatif)
    presence_excuse=False
    i=0
    for el in playable_cards:
        if el.get_rank()==0: #vérifier que la suite de excuse est bien "excuse"
            presence_excuse=True
            position_excuse=i
            i += 1
    if (j==16 and presence_excuse):   # jouer l'excuse si c'est l'avant dernier pli et quand possède l'excuse
        return play_DNF(self,trick,position_excuse,bidder_relatif)

    bidder_played= False

    if bidder_relatif < len(trick):
        bidder_played = True


    if bidder_played:
        return after_bidder(self,trick,bidder_relatif)
    else:
        return before_bidder(self,trick,bidder_relatif)


# vérifier pertinence de la fct play
def play_DNF(self,trick,i,bidder_relatif):
    #fct en charge de jouer une carte
    #i correspond à la position de la position de la carte de playable_card à être joué
    playable_cards = self.playable_cards(trick)

    card = playable_cards[i]

    if card == None :
        card = playable_cards[0]
    return card


def check_if_iam_winner(self,trick,bidder_relatif):
    """fct =True si une de mes cartes bat à l'ATT"""
    #print('[DNF72]  from check_if_iam_winner')
    # Liste de mes cartes jouables + la carte gagnante de l'att
    hypo_trick=[]
    hypo_trick.append(trick[0])
    # J'ajoute la premiere carte du pli (pour savoir la couleur demandée)
    if bidder_relatif != 0:


        for el,j in enumerate(trick):
            if el==bidder_relatif:
                hypo_trick.append(el) #j'introduit la carte gagnante de l'att
        playable_cards=self.playable_cards(trick)

        for el in playable_cards:
            hypo_trick.append(el) #j'introduit mes cartes jouables
        #print('[DNF85]  from check_if_iam_winner bid_rel != 0,  hypo_trick =',hypo_trick)
        #si la meilleur carte de hypo_trick est mienne, cette variable prend la valeur de la position dans payable_cards de ma meilleur carte
        position_meilleur_carte= Player.best_card(hypo_trick) - 2
        #print('[DNF87]  from check_if_iam_winner position_meilleur_carte =',position_meilleur_carte)


        if Player.best_card(hypo_trick)<2: #cad que je ne peux pas battre la carte de l'attaquant
            #print('false', position_meilleur_carte)
            return False , position_meilleur_carte
        else:
            #print('true', position_meilleur_carte)
            return True , position_meilleur_carte

    else:
        playable_cards=self.playable_cards(trick)
        for el in playable_cards:
            hypo_trick.append(el) #j'introduit mes cartes jouables
        #print('[DNF85]  from check_if_iam_winner bid_rel = 0, hypo_trick =',hypo_trick)
        #si la meilleur carte de hypo_trick est mienne, cette variable prend la valeur de la position dans payable_cards de ma meilleur carte
        position_meilleur_carte= Player.best_card(hypo_trick)
        #print('[DNF87]  from check_if_iam_winner position_meilleur_carte =',position_meilleur_carte)


        if position_meilleur_carte == 0: #cad que je ne peux pas battre la carte de l'attaquant
            #print('false', position_meilleur_carte)
            return False , position_meilleur_carte
        else:
            #print('true', position_meilleur_carte)
            return True , position_meilleur_carte - 1


def bidder_payable(self,trick,bidder_relatif): # savoir si l'attaquant peut a priori jouer la couleur demandée + savoir la couleur demande
    #print('[DNF118] from bidder_payable')
    playable_cards=self.playable_cards(trick)
    first_card = trick[0]

    if isinstance(first_card, Excuse): #si la 1º carte jouée est une excuse
        if len(trick) == 1: #si l'IA est 2º (c'est un cas très particulier et compliqué...) A VOIR COMMENT LE GERER
            first_card = random.choice(playable_cards)
        else: #on prend la couleur du 2º joueur
            first_card = trick[1]

    if isinstance(first_card, Trump): #si first_card est un obj type Trump
        #to do: estimer si il peut gagner le pli
        couleur_demande="T"
        if self.database.coupes[bidder_relatif]['max_trump'] != 0:  #si bidder a des atout d'apres database
            #print('data bidder a des atout')
            return 'oui' , couleur_demande  #la couleur demandé est atout est l'ATT va jouer atout
        else:
            return 'atout_couleur' , couleur_demande #ATT  n'a pas atout et joue une autre couleur (ATT perd le plie)

    if isinstance(first_card, Card):
        couleur_demande=first_card.get_suit()
        if self.database.coupes[bidder_relatif][couleur_demande] == False :#si bidder a couleur_demande d apres database
            #print('data bidder a couleur demande')
            return 'oui' , couleur_demande
        else:
            if self.database.coupes[bidder_relatif]['max_trump'] != 0: #bidder a des atout d apres database:
                #print('data bidder a des atout')
                return 'couleur_atout' , couleur_demande #ATT  n'a pas une couleur et joue atout
            else:
                return 'couleur_couleur' , couleur_demande #ATT  n'a pas la couleur et joue une autre couleur (ATT perd le plie)

def avoir_couleur_demande(self,trick, bidder_relatif):
    """True si j'ai la couleur demandée"""
    #print('[DNF152]  from avoir_couleur_demande' )
    a , couleur_demande=bidder_payable(self,trick,bidder_relatif)
    playable_cards=self.playable_cards(trick)
    for el in playable_cards:
        if isinstance(el,Card):
            suit=el.get_suit()
            if suit==couleur_demande :
                return True
        elif isinstance(el,Trump):
            if couleur_demande=="T" :
                return True
        return False


def avoir_atout(self,trick):
    """True si j'ai des atout dans mes cartes jouables"""
    #print('[DNF164]  from avoir_atout' )
    playable_cards=self.playable_cards(trick)
    for el in playable_cards:
        if isinstance(el, Trump): #à vérifier
            return True
    return False

def atout_max(self,trick):
    """retourne le rang de ton plus grand atout jouable et sa position ds playable_cards"""
    #print('[DNF172]  from atout_max')
    playable_cards=self.playable_cards(trick)
    rank_max=0
    position_atout_max = 10
    i=-1
    for el in playable_cards:
        i += 1
        if isinstance(el, Trump):
            if el.get_rank() > rank_max:
                rank_max == el.get_rank()
                position_atout_max = i
    return rank_max , position_atout_max

def atout_min(self,trick):
    """retourne le rang du plus petit atout jouable et sa position ds playable_cards"""
    #print('[DNF187]  from atout_min' )
    playable_cards=self.playable_cards(trick)
    rank_min=22
    position_atout_min = 0
    i = -1
    for el in playable_cards:
        i += 1
        if isinstance(el, Trump):
            if el.get_rank() < rank_min:
                rank_min == el.get_rank()
                position_atout_min = i
    return rank_min , position_atout_min

def jouer_petit(self,trick):
    #print('[DNF201]  from jouer_petit' )
    playable_cards=self.playable_cards(trick)
    for el in enumerate(playable_cards):
        if isinstance(el[1], Trump) and el[1].get_rank() == 1: # True si je peux jouer le petit
            return True , el[0]
    return False , -1



def jouer_excuse(self,trick):
    """Joue l'excuse si l'ATT gagne le plie pour l'instant et
    qu'on peut jouer que des atouts/l'excuse"""
    #print('[DNF211]  from jouer_excuse' )
    playable_cards=self.playable_cards(trick)
    presence_excuse=False
    for el in enumerate(playable_cards):
        if isinstance(el[1], Excuse): #c'est l'excuse
            presence_excuse=True
            position_excuse=el[0]
    if presence_excuse:
        for el in playable_cards:
            if isinstance(el, Card):
                return False, 1
        else:
            return True,position_excuse
    else:
        return False, 1


def proba_apriori(self,trick,couleur_demande,bidder_relatif):
    """Choisir une carte quand l'ATT n'a pas encore joué
    et peut a priori jouer la couleur demandée
    """
    #print('[DNF225]  from proba_apriori')
    playable_cards=self.playable_cards(trick)
    if couleur_demande == 'T':
        if avoir_atout(self,trick):
            bidder_atout_max = self.database.coupes[bidder_relatif]['max_trump']
            #print('data borne sup de l atout max du bidder', bidder_atout_max )
            # C'est une borne sup de l'atout max du bidder
            mon_atout_max = atout_max(self,trick)[0]
            if mon_atout_max > bidder_atout_max: #je suis sûr de gagner
                return play_DNF(self,trick,atout_max(self,trick)[1],bidder_relatif)
            else: #je sais pas si je gagne
                return play_DNF(self,trick,worst_card(self,trick),bidder_relatif)
                #to do: calcul proba de battre l atout que joueras l ATT
        else:
            return play_DNF(self,trick,worst_card(self,trick),bidder_relatif)

    elif couleur_demande in ['S','H','D','C']:
        if avoir_couleur_demande(self,trick, bidder_relatif):
            i=-1
            maxi = True
            if self.database.dico[couleur_demande] == [] :
                return play_DNF(self,trick,worst_card(self,trick),bidder_relatif)
            rank_max = self.database.dico[couleur_demande][-1]
            #print('data carte de ',couleur_demande,' max pas encore joue',rank_max )
            for c in playable_cards:
                i+=1
                if isinstance(c, Card) and c.get_suit() == couleur_demande:
                    if c.get_rank() == rank_max:
                        return play_DNF(self,trick,i,bidder_relatif)
                        maxi = False
            if maxi:
                return play_DNF(self,trick,worst_card(self,trick),bidder_relatif)

             #to do calcul proba de battre à l ATT
        else:
            if avoir_atout(self,trick):
                return play_DNF(self,trick,atout_min(self,trick)[1],bidder_relatif)
            else:
                return play_DNF(self,trick,worst_card(self,trick),bidder_relatif)


def before_bidder (self,trick,bidder_relatif):
    """L'attaquant n'a pas  encore joué dans ce pli"""
    #print('[DNF258]  hello from before_bidder')
    a , couleur_demande=bidder_payable(self,trick,bidder_relatif)
    # savoir si l'attaquant peut a priori jouer la couleur demandée
    if a=="oui":
         #choisir une carte quand l'attaquant n'a pas encore joué et il peut a priori jouer la couler demandée
        return proba_apriori(self,trick,couleur_demande,bidder_relatif)
    elif a=="atout_couleur": # la défense remporte le plie
        if jouer_petit(self,trick)[0]:
            return play_DNF(self,trick,jouer_petit(self,trick)[1],bidder_relatif)
        else:
             return play_DNF(self,trick,card_max_point(self,trick),bidder_relatif) # à optimiser: remporter des points + garder des cartes qui peuvent remporter d autres plies
    elif a=="couleur_atout":
        if avoir_couleur_demande(self,trick, bidder_relatif):
            return play_DNF(self,trick,worst_card(self,trick),bidder_relatif)
        else:
            if avoir_atout(self,trick):
                bidder_atout_max = self.database.coupes[bidder_relatif]['max_trump'] #c'est une cote sup de l'atout max du bidder
                #print('data cote sup de l atout max du bidder',bidder_atout_max )
                mon_atout_max = atout_max(self,trick)[0]
                if mon_atout_max > bidder_atout_max: #je suis sûre de gagner
                    return play_DNF(self,trick,atout_max(self,trick)[1],bidder_relatif)
                else: #je sais pas si je gagne
                    return play_DNF(self,trick,worst_card(self,trick),bidder_relatif) #to do: calcul proba de battre l atout que jouras l ATT

            else:
                return play_DNF(self,trick,worst_card(self,trick),bidder_relatif)

    elif a=="couleur_couleur": # la défense remporte le plie

        if jouer_petit(self,trick)[0]:
            return play_DNF(self,trick,jouer_petit(self,trick)[1],bidder_relatif)
        else:
             return play_DNF(self,trick,card_max_point(self,trick),bidder_relatif) # à optimiser: remporter des points + garder des cartes qui peuvent remporter d autres plies

def worst_card (self,trick):
    """ Renvoie la position dans playing_carte de la pire carte
    (carte couleur nº minimum < atout de nº minimum)"""
    #print('hello from worst_card' )
    rank_min_couleur = 15
    rank_min_atout = 22
    playable_cards=self.playable_cards(trick)
    presence_carte_couleur= False
    i=-1
    position_worst_card = 0
    for el in playable_cards:
        i+=1
        if isinstance(el, Card): #c'est une carte couleur
            presence_carte_couleur= True
            if el.get_rank() < rank_min_couleur:
                rank_min_couleur = el.get_rank()
                position_worst_card = i

    if  presence_carte_couleur:
        return position_worst_card
    else:
        i=-1
        for el in playable_cards:
            i+=1
            if isinstance(el, Trump): # carte atout
                if el.get_rank() < rank_min_atout:
                    rank_min_atout = el.get_rank()
                    position_worst_card = i
    return position_worst_card

def card_max_point (self,trick):
    """Le pli est déjà gagné, on cherche à mettre la carte couleur avec max point,
    si absence de carte couleur en playable_cards on joue l'atout de min rank"""
    #print('[DNF324]  hello from card_max_point')
    playable_cards=self.playable_cards(trick)
    point_max = -1
    presence_carte_couleur= False
    rank_min = 22
    i = -1
    position_card = 0
    for el in playable_cards:
        i +=1
        if isinstance(el, Card): #c'est une carte couleur
            presence_carte_couleur= True
            if el.get_point() > point_max:
                point_max = el.get_point()
                position_card = i
    if presence_carte_couleur:
        return position_card
    else:
        i=-1
        for el in playable_cards:
            i+=1
            if isinstance(el, Trump): #c'est une carte atout
                if el.get_rank() < rank_min:
                    rank_min = el.get_rank()
                    position_card = i
        return position_card


def after_bidder (self,trick,bidder_relatif):
    """L'attaquant a déjà joué dans ce pli"""
    #print('[DNF357]  hello from after_bidder' )
    if bidder_relatif== Player.best_card(trick):   # True si L'attaquant à joué la meilleur carte par l'instant
        if check_if_iam_winner(self,trick,bidder_relatif)[0]:  # fct =True si une de mes cartes bat à l'ATT
            if jouer_petit(self,trick)[0]: #True si je peux jouer le petit
                hypo_trick = []
                hypo_trick.append(trick[0])        #j'introduit la 1º carte
                hypo_trick.append(trick[bidder_relatif]) #j'introduit la carte gagnante de l'att (VERIFIER j)
                playable_cards=self.playable_cards(trick)
                hypo_trick.append(playable_cards[jouer_petit(self,trick)[1]])  #j'introduit le petit
                if Player.best_card(hypo_trick) == 2: #je joue le petit et je sais que je remporte le plie
                    return play_DNF(self,trick,jouer_petit(self,trick)[1],bidder_relatif)
                else:
                    return play_DNF(self,trick,check_if_iam_winner(self,trick,bidder_relatif)[1],bidder_relatif) #jouer ma meilleur carte

            else:
                return play_DNF(self,trick,check_if_iam_winner(self,trick,bidder_relatif)[1],bidder_relatif) #jouer ma meilleur carte
            # reste à optimiser la carte joué

        else:
            if jouer_excuse(self,trick)[0]:
                position_excuse=jouer_excuse(self,trick)[1]
                return play_DNF(self,trick,position_excuse,bidder_relatif)

            else:   #  jouer la carte la plus petite (reste à optimiser la carte joué )
                return play_DNF(self,trick,worst_card(self,trick),bidder_relatif)

    else: #la defense remporte le plie
        if jouer_petit(self,trick)[0]:
            return play_DNF(self,trick,jouer_petit(self,trick)[1],bidder_relatif)

        else:
             return play_DNF(self,trick,card_max_point(self,trick),bidder_relatif)
