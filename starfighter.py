import tkinter as tk
from controleur import JeuControleur, MenuControleur

if __name__ == "__main__":
    """Le main du programme""" 
    start = True
    while(start == True):
        root = tk.Tk()
        root.title("Bienvenue à bord du Starfighter!")
        controleur = JeuControleur(root)
        menuControleur = MenuControleur(root, controleur)
        root.mainloop()
        if(menuControleur.gameQuit == True):
            start = False
