# -*- coding: utf-8 -*-
"""

@author: IATECH

"""
import tkinter as tk
import time
from trump import Trump
from card import Card
from hand_gui import Hand_GUI
from card_gui import Card_GUI
from scoreboard import Scoreboard


class Interface(tk.Tk):
    """Fenêtre de jeu principale"""
    def __init__(self, cartes_visibles):
        """Initialisation"""
        super().__init__()
        self.attributes('-topmost', 'true')
        self.width = 1200  # Fullscreen
        self.height = 650  # Fullscreen
        self.message = tk.Label(self, anchor=tk.NW, text="PE 102 - IATECH")
        self.message.pack()
        self.canvas = tk.Canvas(self, width=self.width, height=self.height,
                               background="green")
        self.canvas.pack()
        self.cartes_visibles = cartes_visibles
        # Attributs utilisés par les fonctions
        self.hands = {0: 'SOUTH', 1: 'WEST', 2: 'NORTH', 3:'EAST'}
        self.playable_cards = []
        self.bid = 0
        self.trick = [] # Contiendra les id des cartes jouées
        self.lastclick = time.time()

    def ajouter_main(self, player, hand):
        """
        player est un indice entre 0 et 3
        hand est une liste d'objet Card
        """
        visibles = self.cartes_visibles or (player==0)
        cards_gui = []
        for card in hand:
            card_gui = self.conversion(card)
            if not visibles:
                card_gui.image = tk.PhotoImage(file="img/back.png")
                card_gui.label.configure(image=card_gui.image)
                card_gui.label.image = card_gui.image
            cards_gui.append(card_gui)
        self.hands[player] = Hand_GUI(self.canvas, cards_gui, self.hands[player], visibles)
        self.hands[player].afficher()

    def afficher_chien(self, player, dog):
        """
        Appelée par GameHost après la prise
        dog est une liste de "rank,suit"
        Affiche les cartes du chien au milieu du terrain
        Attend le clic de l'humain
        Ajoute les cartes du chien à la main du joueur concerné
        Actualise l'affichage de la main du joueur concerné.
        """
        chien=[]
        for card in dog:
            a,b= card.split(',')
            if b == "Excuse":
                chien.append(Card_GUI(self.canvas, b))
            elif b== "Trump":
                chien.append(Card_GUI(self.canvas, 'T'+a))
            else :
                chien.append(Card_GUI(self.canvas, b+a))
        w, h = chien[0].width, chien[0].height
        x, y = self.width//2-3*w, (self.height-h)//2
        for i, card in enumerate(chien):
            card.set_position(x+i*w, y)
        self.attente()
        visibles = self.cartes_visibles or (player==0)
        for carte in chien:
            if not visibles:
                carte.image = tk.PhotoImage(file="img/back.png")
                carte.label.configure(image=card.image)
                carte.label.image = card.image
            self.hands[player].cards.append(carte)
        self.hands[player].afficher()
        time.sleep(2) # Le joueur voit le chien parmi les cartes de l'IA

    def conversion(self, card):
        """Convertit un objet Playing_Card en objet Card_GUI"""
        if isinstance(card, Card):
            return Card_GUI(self.canvas, card.get_suit()+str(card.get_rank()))
        elif isinstance(card, Trump):
            return Card_GUI(self.canvas, 'T'+str(card.get_rank()))
        else:
            return Card_GUI(self.canvas, 'Excuse')

    def choix_prise(self, bid):
        """
            Créé la fenêtre de choix affichant les prises supérieures à bid
            bid: la prise la plus haute actuellement
            MODIFIE [Attribut self.bid]
        """
        popup = tk.Toplevel()
        popup.attributes('-topmost', 'true')
        tk.Label(popup, textvariable="Choisissez").pack()
        var = tk.IntVar()
        def callback():
            print ("choix humain" + str(var.get()))
            self.bid = var.get()
            popup.destroy()
        prises =("Passe", "Petite", "Garde", "Garde sans", "Garde contre")
        for val, nom in enumerate(prises):
            tk.Radiobutton(popup, text=nom, value=val,
                           variable=var, indicator=0).pack()
        tk.Radiobutton(popup, text="Confirm", fg="red", indicator=0,
                       command=callback).pack()
        popup.transient(self) 	  # Réduction popup impossible
        popup.grab_set()		  # Interaction avec fenetre jeu impossible
        self.wait_window(popup)   # Arrêt script principal


    def afficher_prise(self, player, bid):
        """Affiche à côté du joueur concerné son choix de prise"""
        self.hands[player].actualiser_bid(bid)

    def afficher_bidder(self, player):
        """Affiche à côté de l'attaquant son choix de prise"""
        for key in self.hands:
            if key != player:
                self.hands[key].actualiser_bid(None)

    def set_message(self,txt):
        """Change le message affiché en haut"""
        self.message['text'] = txt

    def mettre_au_chien(self, player, card):
        """
        Supprime la carte de la main du joueur concerné, [la pose dans le chien]
        et réarrange ses cartes
        card est de type Card
        player est un indice : 0 (sud), 1 (ouest), 2 (nord), 3 (est)
        L’humain doit donc toujours être 0
        """
        card = self.conversion(card)
        for carte in self.hands[player].cards:
            if carte == card:
                self.canvas.delete(carte.id)
        self.hands[player].cards.remove(card)
        self.hands[player].afficher()

    def jouer_carte(self, player, card):
        """
        Supprime la carte de la main du joueur concerné, la pose devant lui
        et réarrange ses cartes
        card est de type Card
        player est un indice : 0 (sud), 1 (ouest), 2 (nord), 3 (est)
        L’humain doit donc toujours être 0
        """
        card_gui = self.conversion(card)
        self.trick.append(card_gui.play(player))
        print(self.trick)
        for carte in self.hands[player].cards:
            if carte == card_gui:
                self.canvas.delete(carte.id)
        self.hands[player].cards.remove(card_gui)
        self.hands[player].afficher()
        print("Carte", card_gui.name, "jouée")

    def survol_cartes(self, event):
        """
        Suréleve les cartes jouables lorsque le joueur passe la souris dessus.
        [Attribut self.playable_cards]
        """
        for card in self.hands[0].cards :
            if card.name in self.playable_cards:
                card.hitbox_listener(event)

    def choix_carte(self, playable_cards):
        """
        Renvoie la carte sélectionnée par l’humain dans sa main
        Prend un paramètre (liste de "suitrank")
        RETURN : Card object
        """
        self.set_message("A vous de jouer")
        playable = []
        for suitrank in playable_cards:
            # Conversion très moche, dans l'autre sens
            if suitrank[0] == 'E':
                playable.append("Excuse")
            elif suitrank[0] == 'T':
                playable.append('T'+suitrank[5:])
            else:
                playable.append(suitrank)
        self.playable_cards = playable
        self.bind('<Motion>', self.survol_cartes)
        self.bind('<Button-1>', self.clic_carte)
        self.var = tk.IntVar()
        print("waiting for choice")
        self.wait_variable(self.var)
        temp = self.carte
        self.carte = None
        return temp

    def clic_carte(self, event):
        """
        Renvoie la carte sur lequel le joueur a cliqué à condition que:
        -la carte soit jouable [Attribut self.playable_cards]
        -l'écart avec le dernier clic soit <1s [Attribut self.lastclick]
        """
        temp = self.lastclick
        self.lastclick = time.time()
        if (self.lastclick - temp) < 1: # Délai entre chaque clic
            print("DOUBLE CLIC")
        else:
            for card in self.hands[0].cards :
                if card.name in self.playable_cards:
                    card.click_listener(event)
                    if card.click:
                        # Conversion très moche
                        nom = card.name
                        if nom[0] == 'E':
                            self.carte = "0,Excuse"
                        elif nom[0] == 'T':
                            self.carte = nom[1:]+",Trump"
                        else:
                            self.carte = nom[1:]+","+nom[0]
                        self.playable_cards = []
                        self.var.set(1)

    def attente(self):
        """
        Attend que le joueur clique (utile à la fin du tour)
        [Attribut self.attendre]
        """
        self.set_message("Cliquer pour continuer")
        var = tk.IntVar()
        self.bind('<Button-1>',lambda event : var.set(1))
        print("waiting...")
        self.wait_variable(var)

    def fin_attente(self, event):
        """Fonction appelée par attente()"""
        self.attendre = False

    def afficher_score(self, winner, score, true_winner=None):
        """Affiche une nouvelle fenêtre avec les scores en fin de manche"""
        popup = Scoreboard(self, score.split(','), winner, true_winner)
        popup.transient(self) 	  # Réduction popup impossible
        popup.grab_set()		  # Interaction avec fenetre jeu impossible
        self.wait_window(popup)   # Arrêt script principal

    def ranger_pli(self):
        """Retire les cartes du pli"""
        for i in range(4):
            self.canvas.delete(self.trick.pop(-1))

    def reset(self):
        """Remet tout à zéro"""
        self.unbind('<Button-1>')
        self.unbind('<Motion>')
        self.hands[self.indice_bidder].actualiser_bid(None)
        self.hands = {0: 'SOUTH', 1: 'WEST', 2: 'NORTH', 3:'EAST'}
        self.playable_cards = []
        self.bid = 0
        self.trick = [] # Contiendra les id des cartes jouées
        self.lastclick = time.time()
        self.indice_bidder=0
        self.chien=[]
        self.set_message("Nouvelle donne")
        #self.bind('<KeyPress-s>',self.run)
