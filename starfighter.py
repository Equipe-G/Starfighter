import tkinter as tk
from controleur import JeuControleur

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Bienvenue à bord du Starfighter!")

    # creer le controleur du jeu et le passer au menu a la place de None
    #menu = MenuControleur(root, None)
    #menu.commencerJeu()
    controleur = JeuControleur(root)
    controleur.genererJeu()
    root.mainloop()