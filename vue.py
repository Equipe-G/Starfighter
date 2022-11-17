import tkinter as tk
from tkinter import simpledialog
from c31Geometry2 import *
from tkinter import*


class MenuVue:
    """ cette classe permet de définir l'aparence du menu
    """
    def __init__(self, root, fctLancerPartie,voirScore,closeApp):
        """ Initialise le menu graphique

        :param root: Widget parent de notre boucle
        :type  root: tk.Widget
        :param fctLancerParti: methode de lancement de partie
        :type  fctLancerParti: methode()
        :param voirScore: methode voir le score
        :type  voirScore: methode()
        :param closeApp: methode fermer l'application
        :type closeApp : method() 
        """
        self.root = root
        self.score = tk.Label(root, text="")         
        self.btn_nouvellePartie = tk.Button(root, text='Nouvelle Partie',
                                            command=fctLancerPartie)
        self.btn_quitApp = tk.Button(root, text='Quitter',
                                     command=closeApp)
        self.btn_voirScore = tk.Button(root, text='Meilleur score',
                                            command=voirScore)

    def draw(self):
        """ dessine le menu graphique et tout les boutons
        """
        self.btn_nouvellePartie.pack()
        self.btn_voirScore.pack()
        self.btn_quitApp.pack() 

    def destroy(self, canvas):
        canvas.destroy()

class JeuVue:
    """ cette classe permet de définir l'aparence de l'espace de jeu
    """
    def __init__(self, root):
        """
        :param root: Widget parent de notre boucle
        :type  root: tk.Widget
        """
        self.root = root
        self.nom = tk.Label(root, text="") # a aller chercher au debut de la partie et save
        self.score = tk.Label(root, text="") # a changer tout au long de la partie et a save a la fin 
        self.vie = tk.Label(root, text="") # a changer tout au long de la partie
        #self.nom.grid()
        #self.vie.grid()
        #self.score.grid()

    def destroy(self, canvas):
        """ ferme l'espace de jeu
        """
        canvas.destroy()

    def setListen(self, eventName, command) :
        """ Ecoute les evenement qui ce déroule sur sur le canvas et bind une commande sur un evenement 

        Args:
            eventName (String) : le nom de l'evenement 
            command (methode()) : la commande a effectuer 

        """ 
        self.root.bind(eventName, command)

    def setNom(self,nom) :
        """ change la valeur du champ nom

        Args:
            nom (String) : le nom du joueur chosi  
        """
        self.nom.config(text= "Nom du joueur : " + nom )


    def setScore(self,score) :
        """ change le champ score

        Args:
            temp(String(format)) : le score de la partie
        """
        self.score.config(text= str(score))

    def setVie(self,vie) :
        """ change le champ vie

        Args:
            temp(String(format)) : les point de vie du vaisseau
        """
        self.vie.config(text= "Point de vie : " + str(vie) +"%")

    def demanderNom(self,root) :
        """ demande le nom de l'utulisateur dans un pop up

        Args: 
            root (tk.Widjet) : Widget parent de notre boucle

        Returns:
            String: le nom choisi        
        """
        return simpledialog.askstring("Input","Quel est votre nom",parent=root)

    def drawVaiseau(self,vaiseau) :
        """Permet de dessiner le vaiseau
        """
        if hasattr(self, 'id'):
            self.canvas.delete(self.id)
            
        #self.id = self.canvas.create_image(image=vaisseau) voir les paramètre
        
        self.canvas.update()

    def drawVaiseau(self,ovnis) :
        """Permet de dessiner les ovnis
        """
        if hasattr(self, 'id'):
            self.canvas.delete(self.id)
            
        #self.id = self.canvas.create_image((x_coordinate, y_coordinate)image=ovnis) voir les paramètre
        
        self.canvas.update()

    def drawVaiseau(self,asteroide) :
        """Permet de dessiner les asteroide
        """
        if hasattr(self, 'id'):
            self.canvas.delete(self.id)
            
        #self.id = self.canvas.create_image((x_coordinate, y_coordinate)image=asteroide) voir les paramètre
        
        self.canvas.update()


    def drawVaiseau(self,missile) :
        """Permet de dessiner les missile
        """
        if hasattr(self, 'id'):
            self.canvas.delete(self.id)
            
        #self.id = self.canvas.create_image((x_coordinate, y_coordinate)image=missile) voir les paramètre
        
        self.canvas.update()