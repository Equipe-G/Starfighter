from vue import JeuVue, MenueVue
from modeles import Vaisseau, Projectile, Partie
from c31Geometry2 import *
import csv
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
        self.isMoving = False
        self.pressed = False
        self.released = False
        #! Generer les ovnis ici!
        for i in range(0, 20):
            self.ovnis.append(Ovni(self.canvasJeu))
        self.vue.draw(self.vaisseau)
        self.vue.draw(self.projectile)
        self.vue.draw(self.ovnis)
        self.__defineEvent()

    def demarrerPartie(self):
        return self.partieEnCours

    def __defineEvent(self):
        self.vue.setListen("<ButtonPress-1>", self.pressed)
        self.vue.setListen("<ButtonRelease-1>", self.released)
































