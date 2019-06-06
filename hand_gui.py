# -*- coding: utf-8 -*-
"""

@author: IATECH

"""
import tkinter as tk


class Hand_GUI():
    def __init__(self, canvas, cards_gui, placement, visibles):
        """
        Initialisation de la main avec la liste non vide des cartes GUI
        et le placement (South,West,North,East)
        """
        self.canvas = canvas
        self.cards = cards_gui # On indique à la main quelles cartes elle possède
        self.width = self.cards[0].width
        self.hauteur = self.cards[0].height
        self.placement = placement
        self.x, self.y = self.position()
        self.bid = None
        self.visibles = visibles

    def position(self):
        """
        Détermine la position de référence de la main, en fonction du nombre
        de cartes et du placement géographique de la main
        """
        w, h = int(self.canvas['width']), int(self.canvas['height'])
        largeur = (len(self.cards)*0.35 + 0.65)*self.width
        if self.placement == 'SOUTH':
            return (w-largeur)//2, h-self.hauteur-30
        elif self.placement == 'WEST':
            return 30, (h -self.hauteur)//2
        elif self.placement == 'NORTH':
            return (w-largeur)//2, 30
        elif self.placement == 'EAST':
            return w-largeur-30, (h-self.hauteur)//2

    def afficher(self):
        """Affichage des cartes de la main"""
        self.x, self.y = self.position()
        for i in range(len(self.cards)):
            if i == len(self.cards)-1:
                self.cards[i].is_first = True
            self.cards[i].set_position(self.x+i*self.width*0.35, self.y)

    def actualiser_bid(self, bid):
        """
        Affiche la prise du joueur concerné à côté de ses cartes
        """
        if bid is None:
            self.canvas.delete(self.bid)
            self.bid = None
        else:
            prises =("Passe", "Petite", "Garde", "Garde sans", "Garde contre")
            w, h = int(self.canvas['width']), int(self.canvas['height'])
            largeur = (len(self.cards)*0.35 + 0.65)*self.width
            if self.placement == 'SOUTH':
                x, y, anchor = (w-largeur)//2, h-self.hauteur-50, tk.SW
            elif self.placement == 'WEST':
                x, y, anchor = 30, (h-self.hauteur)//2-20, tk.SW
            elif self.placement == 'NORTH':
                x, y, anchor = (w-largeur)//2, self.hauteur+50, tk.NE
            elif self.placement == 'EAST':
                x, y, anchor = w-30, (h+self.hauteur)//2+20, tk.NE
            self.bid = self.canvas.create_text(x, y, fill="black", anchor = anchor,
                                           font="Times 20 bold", text=prises[bid])
