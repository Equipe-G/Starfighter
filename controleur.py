from vue import JeuVue, MenuVue
from modeles import Vaisseau, Projectile, Ovni, PowerUp, asteroides
from c31Geometry2 import *
import csv
from time import sleep
from random import Random, random
class MenuControleur:
    def __init__(self, root, jeuControleur):
        self.jeuControleur = jeuControleur
        self.vue = MenuVue(root, self.nouvelleSession, self.afficherScore, self.quitter)

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
        self.vue.setNom(self.partie.nom)
        self.vue.setDif(self.partie.difficulte)
        self.genererJeu()

    def genererJeu(self):
        self.partieEnCours = False
        self.canvasJeu = CanvasJeu(self.root)
        self.vaisseau = Vaisseau(self.canvasJeu, 1, 100)
        self.projectile = Projectile(self.canvasJeu, self.vaisseau.getOrigine())
        self.ovnis = []
        self.asteroide = []
        self.isMoving = False
        self.pressed = False
        self.released = False
        #! Generer les ovnis ici!
        for i in range(0, 20):
            self.ovnis.append(Ovni(self.canvasJeu))
        for i in range(0,20):
            self.asteroide.append(asteroides(self.canvasJeu))
        self.vue.draw(self.vaisseau)
        self.vue.draw(self.projectile)
        self.vue.draw(self.ovnis)
        self.__defineEvent()

    def demarrerPartie(self):
        return self.partieEnCours

    def __defineEvent(self):
        self.vue.setListen("<ButtonPress-1>", self.buttonPressed)
        self.vue.setListen("<ButtonRelease-1>", self.buttonReleased())
        self.vue.setListen("<Motion>", self.isMoving)
    
    def buttonPressed(self):
        self.pressed = True
        self.released = False

    def buttonReleased(self):
        self.pressed = False
        self.released = True

    def isMoving(self, event):
        self.isMoving = True
        self.x = event.x
        self.y = event.y
        if not self.partieEnCours:
            # self.partie = Partie()
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
            self.deplacerVaisseau(self.x, self.y)
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
            self.vue.draw(self.ovnis)

    def deplacementLogique(self, ovni, x, y):
        #! Deplacement logique des ovnis ici!
        return True

    def deplacementLogiqueVaisseau(self, x, y):
        if x > self.vaisseau.getOrigine().x and y > self.vaisseau.getOrigine().y : #curseur est au nord-est
            self.deplacementVaisseau(self.vaisseau.getOrigine().x +1, self.vaisseau.getOrigine().y +1)
        elif x == self.vaisseau.getOrigine().x and y > self.vaisseau.getOrigine().y : #curseur est au nord
            self.deplacementVaisseau(self.vaisseau.getOrigine().x, self.vaisseau.getOrigine().y +1)
        elif x < self.vaisseau.getOrigine().x and y > self.vaisseau.getOrigine().y : #curseur est au nord-ouest
            self.deplacementVaisseau(self.vaisseau.getOrigine().x -1, self.vaisseau.getOrigine().y +1)
        elif x < self.vaisseau.getOrigine().x and y == self.vaisseau.getOrigine().y : #curseur est à l'ouest
            self.deplacementVaisseau(self.vaisseau.getOrigine().x -1, self.vaisseau.getOrigine().y)
        elif x < self.vaisseau.getOrigine().x and y < self.vaisseau.getOrigine().y : #curseur est au sud-ouest
            self.deplacementVaisseau(self.vaisseau.getOrigine().x -1, self.vaisseau.getOrigine().y -1)
        elif x == self.vaisseau.getOrigine().x and y < self.vaisseau.getOrigine().y : #curseur est au sud
            self.deplacementVaisseau(self.vaisseau.getOrigine().x, self.vaisseau.getOrigine().y -1)
        elif x > self.vaisseau.getOrigine().x and y < self.vaisseau.getOrigine().y : #curseur est au sud-est
            self.deplacementVaisseau(self.vaisseau.getOrigine().x +1, self.vaisseau.getOrigine().y -1)
        elif x > self.vaisseau.getOrigine().x and y == self.vaisseau.getOrigine().y : #curseur est à l'est
            self.deplacementVaisseau(self.vaisseau.getOrigine().x +1, self.vaisseau.getOrigine().y)
        elif x == self.vaisseau.getOrigine().x and y == self.vaisseau.getOrigine().y : #curseur est sur l'origine du vaisseau
            self.deplacementVaisseau(self.vaisseau.getOrigine().x, self.vaisseau.getOrigine().y)
            
    def deplacementVaisseau(self,x,y):
        deplacement = Vecteur(x, y)
        self.vaisseau.translateTo(deplacement)
        self.vaisseau.modificationPos(deplacement)
        self.vue.draw(self.vaisseau)
        
    def initAsteroide(self):
        for a in self.asteroide:
            rndX = random.randint(50,450)
            position = Vecteur(rndX, -20)
            a.modificationPos(position)
    
    def deplacementAsteroide(self):
        for a in self.asteroide :
            newPos = Vecteur(a.getOrigine().x, a.getOrigine().y - 1)
            a.modificationPos(newPos)
            
    def initOvni(self):
        for o in self.ovnis:
            rndX = random.randint(50,450)
            maxRndY = random.randint(15, 95)
            position = Vecteur(rndX, -20)
            o.modificationPos(position)
        



































