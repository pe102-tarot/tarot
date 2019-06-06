# -*- coding: utf-8 -*-
"""

@author: IATECH

"""
import tkinter as tk


class Scoreboard(tk.Toplevel):
    def __init__(self, parent, score, winner, true_winner=None):
        """
        parent la fenêtre principale
        score une liste des 4 scores type string
        winner de type string, le gagnant de la manche
        true_winner de type None ou string, le gagnant de la partie
        """
        tk.Toplevel.__init__(self, parent)
        self.geometry("200x200")
        self.attributes('-topmost', 'true')
        self.title = "Tableau des scores"
        self.parent = parent
        self.main_text = tk.Label(self,text="RESULTATS DE LA PARTIE",padx=5,pady=5,justify='center')
        self.main_text.pack()
        self.winner = winner
        for i in range(4):
            tk.Label(self,text="Joueur "+str(i)+" : "+score[i],padx=2,pady=2,justify='left').pack()
        if winner == 'D':
            txt = "La défense remporte la manche"
        else:
            txt = "Le joueur " + winner + " remporte la manche"
        tk.Label(self,text=txt).pack()
        if true_winner is None:
            txt = "La partie n'est pas terminée !"
        else:
            txt = "Le joueur " + true_winner + " remporte la partie !"
        tk.Label(self,text=txt).pack()
        if true_winner is None:
            tk.Button(self,text="Nouvelle manche",command=self.restart).pack()
        else:
            tk.Button(self,text="Quitter",command=self.finish).pack()

    def restart(self):
        print("Début d'une nouvelle manche")
        self.destroy()
        return(True)

    def finish(self):
        print("Fin de la partie")
        self.parent.destroy()
        print("C'est fini")


if __name__ =='__main__':
    win = tk.Tk()
    score = Scoreboard(win, ['0', '1200', '-300', '-400'], '0', '1')
    score.mainloop()
    win = tk.Tk()
    score = Scoreboard(win, ['0', '1200', '-300', '-400'], 'D')
    score.mainloop()
