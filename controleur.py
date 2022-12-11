from vue import JeuVue, MenuVue
from modeles import Partie, Vaisseau, Projectile, Background, PowerUp, Asteroides, Ovni
from c31Geometry2 import *
import csv
from time import sleep
import random
class MenuControleur:
    """Permet de controler le menu du programme
    Attributes:
        jeuControleur: controleur du jeu
        vue: la vue du menu
    """
    def __init__(self, root, jeuControleur):
        """Permet de definir un controleur de menu et affiche le menu
            Initialise jeuControleur et vue
            Args:
                root(tk): la fenetre tkinter 
                jeuControleur(JeuControleur): controleur du jeu
        """
        self.jeuControleur = jeuControleur
        self.vue = MenuVue(root, self.commencerJeu, self.afficherScore, self.quitter)
        self.vue.draw()
    def commencerJeu(self):
        """Debute le jeu
            Enleve le menu et affiche le jeu
        """
        self.vue.destroy()
        self.jeuControleur.genererJeu()

    def quitter(self):
        """Quitte le jeu
        """
        self.jeuControleur.vue.destroy(self.jeuControleur.vue.root)
    def afficherScore(self):
        """Affiche les scores dans le fichier csv en les organisants du plus grand au plus petit
        """
        # Lecture du fichier csv
        self.dataRead = []
        self.string = ""
        with open('FichierScores.csv', 'r') as csvFile:
            lecteur_score = csv.reader(csvFile, delimiter=',')
            cpt = 0
            for row in lecteur_score:
                if cpt % 2 == 0:
                    self.dataRead.append(row)
                cpt += 1

        # Triage selon le meilleur
        for i in range(0, len(self.dataRead)):
            for j in range(i+1, len(self.dataRead)):
                if float(self.dataRead[j][1]) >= float(self.dataRead[i][1]):
                    temp = self.dataRead[i]
                    self.dataRead[i] = self.dataRead[j]
                    self.dataRead[j] = temp

        # Affichage de la string
        for i in range(0, 10):
            for j in range(0, 3):
                self.string += str(self.dataRead[i][j])
                self.string += "     "
            self.string += "\n"
        self.vue.setScore(self.string)

class JeuControleur:
    """Permet de controler le jeu
    Attributes:
        root: la fenetre tkinter
        vue: la vue du jeu
        moving: si le joueur bouge
        released: si le bouton de souris et relache
        i: loop du jeu? //a completer
        j: pas utilisé? // a completer
        partie: les attributs de la la partie actuelle
        partieEnCours: si la partie est active
        canvasJeu: le canvas tkinter
        background: l'arriere plan
        vaisseau: les atributs du vaisseau du joueur
        projectile:les atributs d'un projectile le nombre de powerups
        ast: ? //a completer
        ovnis: tableau contenant les ovnis ennemis
        asteroide: tableau contenant les asteroides
    """
    def __init__(self, root):
        """Permet de definir un controleur de jeu et affiche le jeu
            Initialise moving, released, i, j, root, partie et vue
            Args:
                root(tk): la fenetre tkinter 
        """
        self.root = root
        self.vue = JeuVue(root)
        #self.vue.setNom(self.nom)
        self.moving = False
        self.released = False
        self.i = 0
        self.j = 0
        #self.partie = Partie(self.nom)

    def genererJeu(self):
        self.partieEnCours = False
        self.canvasJeu = self.vue.getCanvas()
        self.background = Background()
        self.vue.drawEspaceJeu()
        self.vue.drawFond(self.background.imageTk)
        self.vaisseau = Vaisseau(self.canvasJeu)
        self.vue.drawObjet(self.vaisseau)
        self.projectile = Projectile(self.canvasJeu, self.vaisseau.getOrigine())
        self.powerUp = 0
        self.ast = 0
        self.ovnis = []
        self.asteroide = []
        for i in range(0, 20):
            self.ovnis.append(Ovni(self.canvasJeu,Vecteur(random.randint(50,450),-20),random.randint(15, 95)))
        for i in range(0,20):
            self.asteroide.append(Asteroides(self.canvasJeu,Vecteur(random.randint(50,450),-20)))
        # self.vue.drawObjet(self.vaisseau)
        # self.vue.drawObjet(self.projectile)
        # self.vue.drawObjet(self.ovnis)
        self.__defineEvent()

    def demarrerPartie(self):
        return self.partieEnCours

    def __defineEvent(self):
        self.vue.setListen("<ButtonRelease-1>", self.buttonReleased)
        self.vue.setListen("<Motion>", self.isMoving)
    
    def buttonReleased(self, event):
        self.pressed = False
        self.released = True
        self.tirerProjectile()

    def isMoving(self, event):
        self.moving = True
        self.x = event.x
        self.y = event.y
        if not self.partieEnCours:
            #self.partie = Partie()
            self.debuter()

    def debuter(self):
        """Debute la partie actuelle
            Commence la boucle de jeu
        """
        self.partieEnCours = True
        if self.partieEnCours:
            self.e = LoopEvent(self.vue.root, self.roulerJeu, 15)
            self.e.start()

    def roulerJeu(self):
        if not self.verifierCollision():
            #self.deplacementOvnis()
            self.deplacementLogiqueVaisseau(self.x, self.y)
            self.powerUps()
            self.deplacementAsteroide()
            self.deplacementOvni()
        else:
            self.terminerPartie()

    def terminerPartie(self):
        """Termine la partie actuelle
            Enleve le canevas, arrête la boucle, puis sauvegarde le score
        """
        self.vue.destroy(self.vue.root)   #!!! A voir dependament de la place du canvas    #self.vue.destroy(self.canvasJeu.canvas)\
        self.e.stop()
        self.genererJeu() #Besoind de ca? C'est pas le menu qui va en créer une autre apres?
        sleep(1)
        #self.sauverScore()

    def verifierCollision(self):
        vaisseauX = self.vaisseau.getOrigine().x
        vaisseauY = self.vaisseau.getOrigine().y

        #! Verifier les collisions avec les ovnis ici!

    def afficherPouvoir(self):
        ##Afficher les pouvoirs aleatoirement sur le canvas
        return True

    # def deplacementOvnis(self):
    #     for ovni in self.ovnis:
    #         x = self.ovnis[ovni].getOrigine().x
    #         y = self.ovnis[ovni].getOrigine().y
    #         deplacement = self.deplacementLogique(ovni, x, y)

    #         self.ovnis[ovni].translateTo(deplacement)
    #         self.ovnis[ovni].modificationPos(deplacement)
    #         self.vue.drawObjet(self.ovnis)

    def deplacementLogique(self, ovni, x, y):
        #! Deplacement logique des ovnis ici!
        return True

    def deplacementLogiqueVaisseau(self, x, y):
        """Verifie le type de mouvement necessaire par le vaisseau puis appelle deplacementVaisseau
        """
        speed = 4
        if x > self.vaisseau.get_origine().x and y < self.vaisseau.get_origine().y : #curseur est au nord-est
            self.deplacementVaisseau(self.vaisseau.get_origine().x + speed, self.vaisseau.get_origine().y - speed)
        elif x == self.vaisseau.get_origine().x and y < self.vaisseau.get_origine().y : #curseur est au nord
            self.deplacementVaisseau(self.vaisseau.get_origine().x, self.vaisseau.get_origine().y - speed)
        elif x < self.vaisseau.get_origine().x and y < self.vaisseau.get_origine().y : #curseur est au nord-ouest
            self.deplacementVaisseau(self.vaisseau.get_origine().x - speed, self.vaisseau.get_origine().y - speed)
        elif x < self.vaisseau.get_origine().x and y == self.vaisseau.get_origine().y : #curseur est à l'ouest
            self.deplacementVaisseau(self.vaisseau.get_origine().x - speed, self.vaisseau.get_origine().y)
        elif x < self.vaisseau.get_origine().x and y > self.vaisseau.get_origine().y : #curseur est au sud-ouest
            self.deplacementVaisseau(self.vaisseau.get_origine().x - speed, self.vaisseau.get_origine().y + speed)
        elif x == self.vaisseau.get_origine().x and y > self.vaisseau.get_origine().y : #curseur est au sud
            self.deplacementVaisseau(self.vaisseau.get_origine().x, self.vaisseau.get_origine().y + speed)
        elif x > self.vaisseau.get_origine().x and y > self.vaisseau.get_origine().y : #curseur est au sud-est
            self.deplacementVaisseau(self.vaisseau.get_origine().x + speed, self.vaisseau.get_origine().y + speed)
        elif x > self.vaisseau.get_origine().x and y == self.vaisseau.get_origine().y : #curseur est à l'est
            self.deplacementVaisseau(self.vaisseau.get_origine().x + speed, self.vaisseau.get_origine().y)
        elif x == self.vaisseau.get_origine().x and y == self.vaisseau.get_origine().y : #curseur est sur l'origine du vaisseau
            self.deplacementVaisseau(self.vaisseau.get_origine().x, self.vaisseau.get_origine().y)
            

    def deplacementVaisseau(self,x,y):
        """Deplace le vaisseau vers la position de la souris
        """
        deplacement = Vecteur(x, y)
        self.vaisseau.translateTo(deplacement)
        self.vaisseau.modificationPos(deplacement)
        self.vue.drawObjet(self.vaisseau)
        #self.canvasJeu.move(self.vaisseau, x, y)
        #self.canvasJeu.update()

    def tirerProjectile(self):
        """Tire un projectile
            //j'ai des questions sur cette methode
        """
        y = self.vaisseau.getOrigine().y
        for i in range(y):
            deplacement = Vecteur(self.vaisseau.getOrigine().x, y)
            self.projectile.translateTo(deplacement)
            self.projectile.modificationPos(deplacement)
            self.vue.drawObjet(self.projectile)
            y -= 1

    def powerUps(self):
        if self.i <= 100:
            self.i += 1
        else:
            print("powerUps")
            x = random.randint(200, 700)
            y = random.randint(100, 800)
            power = random.randint(1, 3)
            affichage = Vecteur(x, y)

            self.powerUp = PowerUp(self.canvasJeu, affichage, power)
            self.powerUp.translateTo(affichage)
            self.powerUp.modificationPos(affichage)
            self.vue.drawObjet(self.powerUp)
            self.i = 0

    def deplacementAsteroide(self):
        """Deplace les asteroides vers le bas de la page
        """
        for a in self.asteroide :
            newPos = Vecteur(a.getOrigine().x, a.getOrigine().y + 1)
            a.translateTo(newPos)
            a.modificationPos(newPos)
            self.vue.drawObjet(a)

    def deplacementOvni(self):
        """Deplace les ovnis
            //a completer
        """
        for o in self.ovnis:
            if o.getOrigine().y < o.getMaxY() :
                newPos = Vecteur(o.getOrigine().x, +1)
            else :
                rndDirection = random.randint(0,1)
                rndWobble = random.randint(o.getOrigine().y -15, o.getOrigine().y +15)
                if rndDirection == 0 : #vers la gauche
                    if rndWobble == o.getOrigine().y : #no wobble
                        newPos = Vecteur(o.getOrigine().x - 1, o.getOrigine().y)
                    elif rndWobble < o.getOrigine().y : #wobble vers le haut
                        newPos = Vecteur(o.getOrigine().x - 1, o.getOrigine().y-1)
                    elif rndWobble > o.getOrigine().y : #wobble vers le bas
                        newPos = Vecteur(o.getOrigine().x -1, o.getOrigine().y +1)
                else : #vers la droite
                    if rndWobble == o.getOrigine().y : #no wobble
                        newPos = Vecteur(o.getOrigine().x + 1, o.getOrigine().y)
                    elif rndWobble < o.getOrigine().y : #wobble vers le haut
                        newPos = Vecteur(o.getOrigine().x + 1, o.getOrigine().y - 1)
                    elif rndWobble > o.getOrigine().y : #wobble vers le bas
                        newPos = Vecteur(o.getOrigine().x + 1, o.getOrigine().y + 1)
            #Affichage 
            o.translateTo(newPos)
            o.modificationPos(newPos)
            self.vue.drawObjet(self.powerUp)

    # def asteroide(self):
    #     if self.j <= 175:
    #         self.j += 1
    #     else:
    #         print("asteroides")
    #         x = random.randint(200, 800)
    #         y = 0
    #         affichage = Vecteur(x, y)
    #         self.ast = Asteroides(self.canvasJeu, affichage)
    #         self.ast.translateTo(affichage)
    #         self.ast.modificationPos(affichage)
    #         self.vue.drawObjet(self.ast)
    #         for i in range(10000):
    #             deplacement = Vecteur(x, y)
    #             self.ast.translateTo(deplacement)
    #             self.ast.modificationPos(deplacement)
    #             self.vue.drawObjet(self.ast)
    #             y += 0.1
    #         self.j = 0
    
    def sauverScore(self):
        """Permet d'ajouter les informations de cette session dans le fichier csv
        """
        with open('FichierScores.csv', 'a') as csvFile :
            ecriture_score = csv.writer(csvFile, delimiter=',')
            texte = [self.partie.getNom(), str(self.partie.getTemps()), self.partie.getScore()]
            ecriture_score.writerow(texte)