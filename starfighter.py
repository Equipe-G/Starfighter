import tkinter as tk
from controleur import JeuControleur, MenuControleur

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Bienvenue à bord du Starfighter!")
    controleur = JeuControleur(root)
    menuControleur = MenuControleur(root,controleur)
    root.mainloop()