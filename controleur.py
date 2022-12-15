from vue import JeuVue, MenuVue
from modeles import Partie, Vaisseau, Projectile, Background, PowerUp, Asteroides, Ovni, Boss
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
                gameQuit(Boolean): si le jeu est quitte
        """
        self.gameQuit = False
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
        """Quitte le jeu"""
        self.jeuControleur.vue.destroy(self.jeuControleur.vue.root)
        self.gameQuit = True

    def afficherScore(self):
        """Affiche les scores dans le fichier csv en les organisants du plus grand au plus petit"""
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
        partie: les attributs de la la partie actuelle
        partieEnCours: si la partie est active
        canvasJeu: le canvas tkinter
        background: l'arriere plan
        vaisseau: les atributs du vaisseau du joueur
        projectile:les atributs d'un projectile le nombre de powerups
        ovnis: tableau contenant les ovnis ennemis
        asteroide: tableau contenant les asteroides
    """
    def __init__(self, root):
        """Permet de definir un controleur de jeu et affiche le jeu
            Initialise moving, root, partie et vue
            Args:
                root(tk): la fenetre tkinter 
        """
        self.root = root
        self.vue = JeuVue(root)
        self.moving = False

    def genererJeu(self):
        """Permet de générer le jeu à chaque nouvelle partie"""
        self.partieEnCours = False
        self.canvasJeu = self.vue.getCanvas()
        self.background = Background()
        self.vue.drawEspaceJeu()
        self.vue.drawFond(self.background.imageTk)
        self.vaisseau = Vaisseau(self.canvasJeu)
        self.vue.drawObjet(self.vaisseau)
        self.typeArmeOvni = 1
        self.typeArmeVaisseau = 1
        self.asteroideSpawnRate = 1
        self.ovnisSpawnRate = 5
        self.powerUpSpawnRate = 1
        self.ovnis = []
        self.asteroide = []
        self.powerUps = []  
        self.projectiles = []
        self.projectilesOvnis = []
        self.__defineEvent()

    def __defineEvent(self):
        """Definit les evenements possibles"""
        self.vue.setListen("<ButtonRelease-1>", self.buttonReleased)
        self.vue.setListen("<Motion>", self.isMoving)
        self.vue.setListen("<Escape>", self.pauserJeu)

    def buttonReleased(self, event):
        """Action lorsque le bouton est relaché : récupère position du curseur et démarre partie"""
        self.initProjectile()

    def isMoving(self, event):
        """Action lorsque la souris est bougé : récupère position du curseur et démarre partie"""
        self.moving = True
        self.x = event.x
        self.y = event.y
        if not self.partieEnCours:
            self.nom = self.vue.demanderNom(self.root)
            self.partie = Partie(self.nom)
            self.debuter()

    def debuter(self):
        """Debute la partie actuelle et commence la boucle de jeu"""
        self.partieEnCours = True
        if self.partieEnCours:
            self.e = LoopEvent(self.vue.root, self.roulerJeu, 15)
            self.e.start()

    def roulerJeu(self):
        """La boucle de jeu"""
        if(self.vaisseau.getVie() > 0):
            self.initAsteroide()
            self.initOvnis()
            self.deplacementLogiqueVaisseau(self.x, self.y)
            self.tirerProjectile()
            self.initPowerUp()
            self.deplacementAsteroide()
            self.deplacementOvni()
            self.tirOvni()
            self.deplacementPowerUp()
            self.ramasserPowerUp()
            self.verifierCollision()
            self.collisionProjectile()
            self.vue.setScore(self.partie.getScore())
            self.vue.setVie(self.vaisseau.getVie())
        else:
            self.terminerPartie()

    def terminerPartie(self):
        """Termine la partie actuelle
            sauvegarde le score, enleve le canvas, finis la boucle
        """
        self.sauverScore()
        self.vue.destroy(self.vue.root)
        self.e.stop()

    def verifierCollision(self):
        """Verifie si le vaisseau colisionne avec un ovni ou une asteroide"""
        for o in self.ovnis:
            if self.vaisseau.getOrigine().x + 50 >= o.getOrigine().x:
                if self.vaisseau.getOrigine().x <= o.getOrigine().x + 50:
                    if self.vaisseau.getOrigine().y + 10 >= o.getOrigine().y:
                        if self.vaisseau.getOrigine().y <= o.getOrigine().y + 10:
                            self.vaisseau.setVie(self.vaisseau.getVie() - 25)
                            self.ovnis.remove(o)
        for a in self.asteroide:
            if self.vaisseau.getOrigine().x + 50 >= a.getOrigine().x:
                if self.vaisseau.getOrigine().x <= a.getOrigine().x + 50:
                    if self.vaisseau.getOrigine().y + 300 >= a.getOrigine().y:
                        if self.vaisseau.getOrigine().y <= a.getOrigine().y + 300:
                            self.vaisseau.setVie(self.vaisseau.getVie() - 50)
                            self.asteroide.remove(a)
                        
    def deplacementLogiqueVaisseau(self, x, y):
        """Verifie le type de mouvement necessaire par le vaisseau puis appelle deplacementVaisseau
            Args: 
                x (Int): x de la position future
                y (Int): y de la position future
        """
        vitesse = self.vaisseau.getVitesse()
        if x > self.vaisseau.get_origine().x and y < self.vaisseau.get_origine().y : #curseur est au nord-est
            self.deplacementVaisseau(self.vaisseau.get_origine().x + vitesse, self.vaisseau.get_origine().y - vitesse, 1)
        elif x == self.vaisseau.get_origine().x and y < self.vaisseau.get_origine().y : #curseur est au nord
            self.deplacementVaisseau(self.vaisseau.get_origine().x, self.vaisseau.get_origine().y - vitesse, 2)
        elif x < self.vaisseau.get_origine().x and y < self.vaisseau.get_origine().y : #curseur est au nord-ouest
            self.deplacementVaisseau(self.vaisseau.get_origine().x - vitesse, self.vaisseau.get_origine().y - vitesse, 3)
        elif x < self.vaisseau.get_origine().x and y == self.vaisseau.get_origine().y : #curseur est à l'ouest
            self.deplacementVaisseau(self.vaisseau.get_origine().x - vitesse, self.vaisseau.get_origine().y, 4)
        elif x < self.vaisseau.get_origine().x and y > self.vaisseau.get_origine().y : #curseur est au sud-ouest
            self.deplacementVaisseau(self.vaisseau.get_origine().x - vitesse, self.vaisseau.get_origine().y + vitesse, 5)
        elif x == self.vaisseau.get_origine().x and y > self.vaisseau.get_origine().y : #curseur est au sud
            self.deplacementVaisseau(self.vaisseau.get_origine().x, self.vaisseau.get_origine().y + vitesse, 6)
        elif x > self.vaisseau.get_origine().x and y > self.vaisseau.get_origine().y : #curseur est au sud-est
            self.deplacementVaisseau(self.vaisseau.get_origine().x + vitesse, self.vaisseau.get_origine().y + vitesse, 7)
        elif x > self.vaisseau.get_origine().x and y == self.vaisseau.get_origine().y : #curseur est à l'est
            self.deplacementVaisseau(self.vaisseau.get_origine().x + vitesse, self.vaisseau.get_origine().y, 8)
        elif x == self.vaisseau.get_origine().x and y == self.vaisseau.get_origine().y : #curseur est sur l'origine du vaisseau            
            self.deplacementVaisseau(self.vaisseau.get_origine().x, self.vaisseau.get_origine().y, 9)
                    
    def deplacementVaisseau(self, x, y, distance):
        """Deplace le vaisseau vers la position de la souris
                Args: 
                x (Int): x de la position future
                y (Int): y de la position future
                distance (Int): disctance entre la position actuelle et celle voulue
        """
        bougeDistance = self.vaisseau.getVitesse()
        a = 0
        b = 0
        if distance == 1:
            a = bougeDistance
            b = -bougeDistance
        elif distance == 2:
            a = 0
            b = -bougeDistance
        elif distance == 3:
            a = -bougeDistance
            b = -bougeDistance
        elif distance == 4:
            a = -bougeDistance
            b = 0
        elif distance == 5:
            a = -bougeDistance
            b = bougeDistance
        elif distance == 6:
            a = 0
            b = bougeDistance
        elif distance == 7:
            a = bougeDistance
            b = bougeDistance
        elif distance == 8:
            a = bougeDistance
            b = 0
        elif distance == 9:
            a = 0
            b = 0
        deplacement = Vecteur(x, y)
        self.vaisseau.translateTo(deplacement)
        self.vaisseau.modificationPos(deplacement)
        self.vue.updateObjet(self.vaisseau, a, b)

    def initProjectile(self):
        """Crée un projectile"""
        newProjectile = Projectile(self.canvasJeu,self.vaisseau.getOrigine(),self.typeArmeVaisseau)
        self.projectiles.append(newProjectile)
        self.vue.drawObjet(newProjectile)

    def tirerProjectile(self):
        """Tire un projectile"""
        for p in self.projectiles:
            newPos = Vecteur(p.getOrigine().x, p.getOrigine().y - p.getVitesse())
            p.translateTo(newPos)
            p.modificationPos(newPos)
            self.vue.updateObjet(p, 0, p.getVitesse() * -1)

            if p.getOrigine().y <= 0:
                self.projectiles.remove(p)

    def initPowerUp(self):
        """"As une chance de generer un powerup"""
        if random.randint(0, 1000) <= self.powerUpSpawnRate:
            x = random.randint(50, 950)
            y = -10
            power = random.randint(1, 3)
            affichage = Vecteur(x, y)

            powerUp = PowerUp(self.canvasJeu, affichage, power)
            powerUp.desactiverPouvoir(self.vaisseau)
            self.typeArmeVaisseau = powerUp.desactiverPouvoir(self.vaisseau)
            self.powerUps.append(powerUp)
            powerUp.translateTo(affichage)
            powerUp.modificationPos(affichage)
            self.vue.drawObjet(powerUp)

    def initOvnis(self):
        """"As une chance de generer un ovni normal ou un boss"""
        if(random.randint(0, 1000) <= self.ovnisSpawnRate):
            x = random.randint(50, 900)
            pos = Vecteur(x, -20)
            if(random.randint(0, 100) >= 15):
                newOvni = Ovni(self.canvasJeu, pos, random.randint(15, 295))
            else:
                newOvni = Boss(self.canvasJeu, pos, random.randint(15, 295))
            self.ovnis.append(newOvni)            
            newOvni.translateTo(pos)
            newOvni.modificationPos(pos)
            self.vue.drawObjet(newOvni)

    def initAsteroide(self):
        """"As une chance de generer une asteroide"""
        if(random.randint(0, 1000) <= self.asteroideSpawnRate):
            x = random.randint(50, 900)
            pos = Vecteur(x, -20)
            newAsteroide = Asteroides(self.canvasJeu, pos)
            self.asteroide.append(newAsteroide)
            newAsteroide.translateTo(pos)
            newAsteroide.modificationPos(pos)
            self.vue.drawObjet(newAsteroide)

    def deplacementPowerUp(self):
        """Deplace les powerUps"""
        for p in self.powerUps:
            newPos = Vecteur(p.getOrigine().x, p.getOrigine().y + 1)
            p.translateTo(newPos)
            p.modificationPos(newPos)
            self.vue.updateObjet(p, 0, 2)
            
            if p.getOrigine().y >= 1000:
                self.powerUps.remove(p)

    def deplacementAsteroide(self):
        """Deplace les asteroides vers le bas de la page"""
        for a in self.asteroide :
            newPos = Vecteur(a.getOrigine().x, a.getOrigine().y + 1)
            a.translateTo(newPos)
            a.modificationPos(newPos)
            self.vue.updateObjet(a, 0, 3)
            
            if a.getOrigine().y >= 1000:
                self.asteroide.remove(a)

    def deplacementOvni(self):
        """Deplace les ovnis vers le bas de la page"""
        for o in self.ovnis:
            newPos = Vecteur(o.getOrigine().x, o.getOrigine().y + 1)
            o.translateTo(newPos)
            o.modificationPos(newPos)
            self.vue.updateObjet(o, 0, 1)
            
            if o.getOrigine().y >= 1000:
                self.ovnis.remove(o)

    def tirOvni(self):
        """As une chance qu'un ovni tire un prjectile"""
        for o in self.ovnis:
            if random.randint(0,100) <= 1 :
                newProjectile = Projectile(self.canvasJeu, o.getOrigine(),self.typeArmeOvni)
                self.vue.drawObjet(newProjectile)
                self.projectilesOvnis.append(newProjectile)

        for p in self.projectilesOvnis:
            newPos = Vecteur(p.getOrigine().x, p.getOrigine().y + p.getVitesse())
            p.translateTo(newPos)
            p.modificationPos(newPos)
            self.vue.updateObjet(p, 0, p.getVitesse())

            if p.getOrigine().x >= self.vaisseau.getOrigine().x - 50 and p.getOrigine().x <= self.vaisseau.getOrigine().x +50: #si la balle se trouve dans la colonne du vaisseau
                if p.getOrigine().y >= self.vaisseau.getOrigine().y -50 and p.getOrigine().y <= self.vaisseau.getOrigine().y +50: #si la balle se trouve sur le vaisseau (colonne + rangée)
                    self.vaisseau.setVie(self.vaisseau.getVie() - 10)
                    self.projectilesOvnis.remove(p)

            if p.getOrigine().y >= 1000:
                self.projectilesOvnis.remove(p)

    def ramasserPowerUp(self):
        """Verifie si le vaisseau ramasse un powerUp"""
        for p in self.powerUps:
            if self.vaisseau.getOrigine().x + 130 >= p.getOrigine().x:
                if self.vaisseau.getOrigine().x <= p.getOrigine().x + 130:
                    if self.vaisseau.getOrigine().y + 130 >= p.getOrigine().y:
                        if self.vaisseau.getOrigine().y <= p.getOrigine().y + 130:
                            self.typeArmeVaisseau = p.activerPouvoir(self.vaisseau)
                            self.powerUps.remove(p)

    def collisionProjectile(self):
        """Verifie si le projectile a touché un objet"""
        for o in self.ovnis:
             for p in self.projectiles:
                if p.getOrigine().x >= o.getOrigine().x - 30 and p.getOrigine().x <= o.getOrigine().x +30: #si projectile est dans la colonne de l'ovni
                    if p.getOrigine().y >= o.getOrigine().y - 30 and p.getOrigine().y <= o.getOrigine().y +30: #si projectile est sur l'ovni (car même colonne et même rangée)
                        o.enleverVie(10)
                        self.projectiles.remove(p)
                        if o.getVie() <= 0:
                            if(o.lienImage == "Image/Boss.png"):
                                self.partie.addScore(15)
                            else:
                                self.partie.addScore(5)
                            self.ovnis.remove(o)

        for a in self.asteroide:
            for p in self.projectiles:
                if p.getOrigine().x >= a.getOrigine().x - 30 and p.getOrigine().x <= a.getOrigine().x +30: #si projectile est dans la colonne de l'ovni
                    if p.getOrigine().y >= a.getOrigine().y - 30 and p.getOrigine().y <= a.getOrigine().y +30: #si projectile est sur l'ovni (car même colonne et même rangée)
                        a.enleverVie(5)
                        self.projectiles.remove(p)
                        if a.getVie() <= 0:
                            self.asteroide.remove(a)

    def sauverScore(self):
        """Permet d'ajouter les informations de cette session dans le fichier csv"""
        with open('FichierScores.csv', 'a') as csvFile :
            ecriture_score = csv.writer(csvFile, delimiter=',')
            texte = [self.partie.getNom(), str(self.partie.getTemps()), self.partie.getScore()]
            ecriture_score.writerow(texte)

    def pauserJeu(self, event):
        """Permet d'ajouter les informations de cette session dans le fichier csv"""
        sleep(5)
