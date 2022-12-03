from vue import JeuVue, MenuVue
from modeles import Vaisseau, Projectile, Background
from c31Geometry2 import *
import csv
from time import sleep
class MenuControleur:
    def __init__(self, root, jeuControleur):
        self.jeuControleur = jeuControleur
        #self.vue = MenuVue(root, self.nouvelleSession, self.afficherScore, self.quitter)

    def commencerJeu(self):
        self.vue.draw()

    def quitter(self):
        self.jeuControleur.vue.destroy(self.jeuControleur.vue.root)
    def afficherScore(self):
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
    def __init__(self, root):
        self.root = root
        self.vue = JeuVue(root)
        #self.vue.setNom(self.partie.nom)
        #self.vue.setDif(self.partie.difficulte)
        self.isMovingg = False
        self.released = False

    def genererJeu(self):
        self.partieEnCours = False
        self.canvasJeu = self.vue.getCanvas()
        self.background = Background(self.canvasJeu)
        self.vue.drawEspaceJeu()
        self.vue.drawFond(self.background.imageTk)
        self.vaisseau = Vaisseau(self.canvasJeu)
        self.vue.drawObjet(self.vaisseau)
        self.projectile = Projectile(self.canvasJeu)
        self.ovnis = []
        #! Generer les ovnis ici!
        #for i in range(0, 20):
            #self.ovnis.append(Ovni(self.canvasJeu))
        #self.vue.drawObjet(self.vaisseau)
        #self.vue.drawObjet(self.projectile)
        #self.vue.drawObjet(self.ovnis)
        self.__defineEvent()

    def demarrerPartie(self):
        return self.partieEnCours
    def __defineEvent(self):
        self.vue.setListen("<ButtonRelease-1>", self.buttonReleased)
        self.vue.setListen("<Motion>", self.isMoving)
        print("event defined")

    def buttonReleased(self, event):
        self.pressed = False
        self.released = True
        self.tirerProjectile(event.x, event.y)

    def isMoving(self, event):
        self.isMovingg = True
        self.x = event.x
        self.y = event.y
        if not self.partieEnCours:
            #self.partie = Partie()
            self.debuter()

    def debuter(self):
        self.partieEnCours = True
        if self.partieEnCours:
            self.e = LoopEvent(self.vue.root, self.roulerJeu, 10)
            self.e.start()

    def roulerJeu(self):
        if not self.verifierCollision():
            self.deplacementOvnis()
            self.afficherPouvoir()
            self.deplacementLogiqueVaisseau(self.x, self.y)
        else:
            self.terminerPartie()

    def terminerPartie(self):
        self.vue.destroy(self.vue.root)   #!!! A voir dependament de la place du canvas    #self.vue.destroy(self.canvasJeu.canvas)\
        self.e.stop()
        self.genererJeu()
        sleep(1)

    def verifierCollision(self):
        vaisseauX = self.vaisseau.getOrigine().x
        vaisseauY = self.vaisseau.getOrigine().y

        #! Verifier les collisions avec les ovnis ici!

    def afficherPouvoir(self):
        ##Afficher les pouvoirs aleatoirement sur le canvas
        return True

    def deplacementOvnis(self):
        for ovni in self.ovnis:
            x = self.ovnis[ovni].getOrigine().x
            y = self.ovnis[ovni].getOrigine().y
            deplacement = self.deplacementLogique(ovni, x, y)

            self.ovnis[ovni].translateTo(deplacement)
            self.ovnis[ovni].modificationPos(deplacement)
            self.vue.drawObjet(self.ovnis)

    def deplacementLogique(self, ovni, x, y):
        #! Deplacement logique des ovnis ici!
        return True

    def deplacementLogiqueVaisseau(self, x, y):
        speed = 3
        if x > self.vaisseau.get_origine().x and y < self.vaisseau.get_origine().y : #curseur est au nord-est
            self.deplacementVaisseau(self.vaisseau.get_origine().x +speed, self.vaisseau.get_origine().y -speed)
        elif x == self.vaisseau.get_origine().x and y < self.vaisseau.get_origine().y : #curseur est au nord
            self.deplacementVaisseau(self.vaisseau.get_origine().x, self.vaisseau.get_origine().y -speed)
        elif x < self.vaisseau.get_origine().x and y < self.vaisseau.get_origine().y : #curseur est au nord-ouest
            self.deplacementVaisseau(self.vaisseau.get_origine().x -speed, self.vaisseau.get_origine().y -speed)
        elif x < self.vaisseau.get_origine().x and y == self.vaisseau.get_origine().y : #curseur est à l'ouest
            self.deplacementVaisseau(self.vaisseau.get_origine().x -speed, self.vaisseau.get_origine().y)
        elif x < self.vaisseau.get_origine().x and y > self.vaisseau.get_origine().y : #curseur est au sud-ouest
            self.deplacementVaisseau(self.vaisseau.get_origine().x -speed, self.vaisseau.get_origine().y +speed)
        elif x == self.vaisseau.get_origine().x and y > self.vaisseau.get_origine().y : #curseur est au sud
            self.deplacementVaisseau(self.vaisseau.get_origine().x, self.vaisseau.get_origine().y +speed)
        elif x > self.vaisseau.get_origine().x and y > self.vaisseau.get_origine().y : #curseur est au sud-est
            self.deplacementVaisseau(self.vaisseau.get_origine().x +speed, self.vaisseau.get_origine().y +speed)
        elif x > self.vaisseau.get_origine().x and y == self.vaisseau.get_origine().y : #curseur est à l'est
            self.deplacementVaisseau(self.vaisseau.get_origine().x +speed, self.vaisseau.get_origine().y)
        elif x == self.vaisseau.get_origine().x and y == self.vaisseau.get_origine().y : #curseur est sur l'origine du vaisseau
            self.deplacementVaisseau(self.vaisseau.get_origine().x, self.vaisseau.get_origine().y)

    def deplacementVaisseau(self,x,y):
        deplacement = Vecteur(x, y)
        self.vaisseau.translateTo(deplacement)
        self.vaisseau.modificationPos(deplacement)
        self.vue.drawObjet(self.vaisseau)

    def tirerProjectile(self, x, y):
        for i in range(y):
            deplacement = Vecteur(x, y)
            self.projectile.translateTo(deplacement)
            self.projectile.modificationPos(deplacement)
            self.vue.drawObjet(self.projectile)
            y -= 1