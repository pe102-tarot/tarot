# -*- coding: utf-8 -*-
"""

@author: IATECH

"""
import tkinter as tk


class Card_GUI():
    def __init__(self, canvas, nom):
        """Initialisation sans héritage de tk.PhotoImage"""
        self.image = tk.PhotoImage(file="img/"+nom+".png")
        #Essentiel de rattacher l'image à un label pour l'afficher effectivement
        self.label = tk.Label(image = self.image)
        self.label.image=self.image
        self.width = self.image.width()
        self.height = self.image.height()
        self.name = nom
        self.canvas = canvas
        self.id = None  # Tout élément du canvas possède un ID
        self.x = 0  # Le coin en haut à gauche
        self.y = 0  # Le coin en haut à gauche
        self.hitbox = [self.x, self.y, self.width*0.35, self.height]
        self.click = False  # Si on a cliqué sur la carte
        self.up = False  # Si la carte est surélevée
        self.is_first = False

    def draw(self):
        """Permet de créer l'image sur le canvas"""
        if self.id != None:
            self.canvas.delete(self.id)
        self.id = self.canvas.create_image(self.x, self.y, anchor=tk.NW, image=self.image)

    def set_position(self, x, y):
        """Change la position de la carte, et change aussi la hitbox"""
        self.x = x
        self.y = y
        #print("set position,", x, y)
        if self.is_first:
            self.hitbox = [self.x, self.y, self.width, self.height]
        else:
            self.hitbox = [self.x, self.y, self.width*0.35, self.height]
        self.draw()

    def hitbox_listener(self, event):
        """Si la souris a le focus sur la carte, on la surélève"""
        flag_x = (event.x > self.hitbox[0] and event.x < self.hitbox[0]+self.hitbox[2])
        flag_y = (event.y > self.hitbox[1] and event.y < self.hitbox[1]+self.hitbox[3])
        if not self.up:
            if flag_x and flag_y:
                self.set_position(self.x, self.y-20)
                self.up = True
        elif not flag_x or not flag_y:
            self.set_position(self.x, self.y+20)
            self.up = False

    def click_listener(self,event):
        """Renvoie le nom de la carte si on a cliqué dessus"""
        flag_x = (event.x > self.hitbox[0] and event.x < self.hitbox[0]+self.hitbox[2])
        flag_y = (event.y > self.hitbox[1] and event.y < self.hitbox[1]+self.hitbox[3])
        if flag_x and flag_y:
            print(self.name, " : Clicked")
            self.click = True

    def __eq__(self, other):
        if not isinstance(other, Card_GUI):
            return NotImplemented
        return self.name == other.name

    def play(self, player):
        """Place la carte devant le joueur"""
        w, h = int(self.canvas['width']), int(self.canvas['height'])
        if player == 0:  # SOUTH
            self.set_position((w-self.width)//2, h-2*self.height-70)
        elif player == 1:  # WEST
            self.set_position(w//2-2*self.width-50, (h-self.height)//2)
        elif player == 2:  # NORTH
            self.set_position((w-self.width)//2, self.height+70)
        elif player == 3:  # EAST
            self.set_position(w//2+self.width+50, (h-self.height)//2)
        return self.id
