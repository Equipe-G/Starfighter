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
        self.frame = tk.Frame(root, width=300, height=0)        
        self.btn_nouvellePartie = tk.Button(root, text='Nouvelle Partie',
                                            command=fctLancerPartie)
        self.btn_quitApp = tk.Button(root, text='Quitter',
                                     command=closeApp)
        self.btn_voirScore = tk.Button(root, text='Meilleur score',
                                            command=voirScore)

    

    def draw(self):
        """ dessine le menu graphique et tout les boutons
        """
        self.frame.pack()
        self.btn_nouvellePartie.pack(fill='x',side = "top")
        self.btn_voirScore.pack(fill='x',side = "top")
        self.btn_quitApp.pack(fill='x',side = "top")

    def destroy(self):
        self.btn_nouvellePartie.destroy()
        self.btn_quitApp.destroy()
        self.btn_voirScore.destroy()
        self.frame.destroy()

class JeuVue:
    """ cette classe permet de définir l'aparence de l'espace de jeu
    """
    def __init__(self, root): #! Mettre imgFond en parametre
        """
        :param root: Widget parent de notre boucle
        :type  root: tk.Widget
        """
        self.root = root
        self.canvas = tk.Canvas(root, width=1000, height=1000, bg='white')
        self.idVIe = ""
        self.idScore = ""

    def drawEspaceJeu(self):
        self.canvas.pack()

    def drawFond(self,fond):
        self.canvas.create_image(0,0,image=fond, anchor="nw")
        self.idVIe =self.canvas.create_text(800,50,text="",fill="red", font=("Helvetica",20))
        self.idScore = self.canvas.create_text(200,50,text="",fill="green", font=("Helvetica",20))
    def destroy(self, canvas):
        """ ferme l'espace de jeu
        """
        canvas.destroy()
        
    def getCanvas(self):
        return self.canvas

    def setListen(self, eventName, command) :
        """ Ecoute les evenement qui ce déroule sur sur le canvas et bind une commande sur un evenement 

        Args:
            eventName (String) : le nom de l'evenement 
            command (methode()) : la commande a effectuer 

        """ 
        self.root.bind(eventName, command)


    def setScore(self,score) :
        """ change le champ score

        Args:
            temp(String(format)) : le score de la partie
        """
        self.canvas.itemconfig(self.idScore, text = "Score : " + score  ) 

    def setVie(self,vie) :
        """ change le champ vie

        Args:
            temp(String(format)) : les point de vie du vaisseau
        """
        self.canvas.itemconfig(self.idVIe, text = "Vie : "  + vie + "%" )

    def drawObjet(self, objet):
        """Permet de dessiner tous les objet ayant un sprite valide(une image)
        """
        if hasattr(objet, 'id'):
            self.canvas.delete(objet.id)

        objet.id = self.canvas.create_image(objet.getOrigine().x, objet.getOrigine().y, image=objet.imageTk) #voir les paramètre
        
        self.canvas.update()

    
    def updateObjet(self, objet, x, y):
        self.canvas.move(objet.id, x, y)
        self.canvas.update()

    def demanderNom(self,root) :
        """ demande le nom de l'utulisateur dans un pop up

        Args: 
            root (tk.Widjet) : Widget parent de notre boucle

        Returns:
            String: le nom choisi        
        """
        return simpledialog.askstring("Input", "Quel est votre nom", parent=root)
    