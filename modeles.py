import time
from c31Geometry2 import *
from PIL import ImageTk, Image



class objetVolant(Oval):
    """Cette classe est la parente de tout objet volant (Herite de Oval de c31Geometry2)
    
    Attributes:
        origine(Vecteur): position de l'objet
        petitRayon(int): taille du petit rayon de l'oval
        grandRayon(int): taille du grand rayon de l'oval
        vie(int): vie de l'objet
        vitesse(int): vitesse de mouvement de l'objet
        imageTk(): image representant l'objet
    """ 
    def __init__(self, canvas, vitesse, vie, petitRayon, grandRayon, origine, lienImage, xImage, yImage):
        """Permet de definir un objet volant 

        Initialise origine, petitRayon, grandRayon, vie, vitesse et imageTk
            Args: 
                canvas (tk.Canvas): canvas où l'on dessine le carré
                origine(Vecteur): position de l'objet
                petitRayon(int): taille du petit rayon de l'oval
                grandRayon(int): taille du grand rayon de l'oval
                vie(int): vie de l'objet
                vitesse(int): vitesse de l'objet
                lienImage(string): chemin relatif de l'image de l'objet
        """ 
        self.vitesse = vitesse
        self.vie = vie
        self.petitRayon = petitRayon
        self.grandRayon = grandRayon
        self.imageBase = Image.open(lienImage)
        self.image = self.imageBase.resize((xImage,yImage), Image.ANTIALIAS)
        self.imageTk = ImageTk.PhotoImage(self.image)
        super().__init__(canvas, origine, self.petitRayon, self.grandRayon, "white", "white", 0)

    def getOrigine(self) -> Vecteur:
        """Permet de récupérer l'origine de l'objet
        Returns:
            int: position de l'objet
        """
        return super().get_position()

    def modificationPos(self, position: Vecteur):
        """Définit l'origine de l'objet et le deplace
        Args:
            position (Vecteur): Nouvelle position de l'objet
        """
        self.origine = position
        super().translateTo(position)

    def getVitesse(self):
        """Permet de récupérer la vitesse de l'objet
        Returns:
            int: vitesse de mouvement de l'objet
        """
        return self.vitesse

    def setVitesse(self, vitesse):
        """Change la vitesse de l'objet
        Args:
            petitRayon (int): nouvelle vitesse de mouvement de l'objet
        """
        self.vitesse = vitesse

    def getVie(self):
        """Permet de récupérer la vie de l'objet
        Returns:
            int: vie de l'objet
        """
        return self.vie

    def setVie(self, vie):
        """Change la vie de l'objet
        Args:
            petitRayon (int): nouvelle vie de l'objet
        """
        self.vie = vie

    def getPetitRayon(self):
        """Permet de récupérer le petit rayon de l'objet
        Returns:
            int: petit rayon de l'objet
        """
        return self.petitRayon

    def setPetitRayon(self, petitRayon):
        """Change le petit rayon de l'objet
        Args:
            petitRayon (int): nouvelle petit rayon de l'objet
        """
        self.petitRayon = petitRayon

    def getGrandRayon(self):
        """Permet de récupérer le grand rayon de l'objet
        Returns:
            int: grand rayon de l'objet
        """
        return self.grandRayon

    def setGrandRayon(self, grandRayon):
        """Change le grand rayon de l'objet
        Args:
            grandRayon (int): nouvelle grand rayon de l'objet
        """
        self.grandRayon = grandRayon
        
class PowerUp(objetVolant):
    """Cette classe est la parente de tout powerup (Herite de Cercle de c31Geometry2)
    
    Attributes:
        origine(Vecteur): position de l'objet
        rayon(int): rayon du cercle
        imageTk(): image representant l'objet
        vitesse(int): vitesse de mouvement du powerup
    """ 
    def __init__(self, canvas, origine, power):
        """Permet de definir un objet volant 

        Initialise origine, rayon et imageTk
            Args: 
                canvas (tk.Canvas): canvas où l'on dessine le carré
                origine(Vecteur): position de l'objet
        """
        self.lienImage = ""

        if power == 1:
            self.lienImage = "Image/powerUp1.png"
        elif power == 2:
            self.lienImage = "Image/powerUp2.png"
        elif power == 3:
            self.lienImage = "Image/powerUp3.png"

        super().__init__(canvas, 0, 0, 10, 15, origine, self.lienImage, 30, 45)
    
    def getOrigine(self) -> Vecteur:
        """Permet de récupérer l'origine du powerup
        Returns:
            int: position du powerup
        """
        return super().get_position()

    def modificationPos(self, position: Vecteur):
        """Définit l'origine du powerup et le deplace
        Args:
            position (Vecteur): Nouvelle position du powerup
        """
        self.origine = position
        super().translateTo(position)

    def getVitesse(self):
        """Permet de récupérer la vitesse du powerup
        Returns:
            int: vitesse de mouvement du powerup
        """
        return self.vitesse

    def setVitesse(self, vitesse):
        """Change la vitesse du powerup
        Args:
            petitRayon (int): nouvelle vitesse de mouvement du powerup
        """
        self.vitesse = vitesse

    def getRayon(self):
        """Permet de récupérer le rayon du powerup
        Returns:
            int: taille du rayon du powerup
        """
        return self.rayon

class Projectile(objetVolant):
    """Cette classe est represente un projectile tire par un vaisseau ou ovni (Herite de ObjetVolant)
    
    Attributes:
        Ceux de la superclasse ObjetVolant
    """ 
    def __init__(self, canvas, origine):
        self.lienImage = "Image/Lazer.png"
        super().__init__(canvas, 10, 1, 1, 2, origine, self.lienImage, 40, 40)

    def getOrigine(self) -> Vecteur:
        """Permet de récupérer l'origine du projectile
        Returns:
            Vecteur: Origine du projectile
        """
        return super().get_position()

    def modificationPos(self, position: Vecteur):
        """Définit l'origine du projectile et le deplace
        Args:
            position (Vecteur): Nouvelle position du projectile
        """
        self.origine = position
        super().translateTo(position)

    def getPetitRayon(self):
        return self.petitRayon

    def getGrandRayon(self):
        return self.grandRayon

    def getVitesse(self):
        return self.vitesse

    def setVitesse(self, vitesse):
        self.vitesse = vitesse
        
class Vaisseau(objetVolant):
    """Cette classe est represente le vaisseau du joueur (Herite de ObjetVolant)
    
    Attributes:
        Ceux de la superclasse ObjetVolant
    """ 
    def __init__(self, canvas):
        """Permet de definir un vaisseau 

        Initialise super et imageTk
            Args: 
                canvas (tk.Canvas): canvas où l'on dessine le carré
        """ 
        self.lienImage = "Image/Vaisseau.png"
        super().__init__(canvas, 10, 100, 50, 100 , Vecteur(500,900), self.lienImage, 200, 200)

class Ovni(objetVolant):
    """Cette classe est represente un ovni ennemi (Herite de ObjetVolant)
    
    Attributes:
        Ceux de la superclasse ObjetVolant
        maxY(int): le plus haut que l'ovni peut aller
    """ 
    def __init__(self, canvas, origine, maxY):
        """Permet de definir un ovni 

        Initialise super et imageTk
            Args: 
                canvas (tk.Canvas): canvas où l'on dessine le carré
        """ 
        self.maxY = maxY
        self.lienImage = "Image/Alien.png"
        super().__init__(canvas, 5, 10, 20, 50 , origine, self.lienImage, 150, 150)
        
    def getMaxY(self):
        """Permet de récupérer le maxY de l'ovni
        Returns:
            int: le plus haut que l'ovni peut aller
        """
        return self.maxY

class Asteroides(objetVolant):
    """Cette classe est represente les asteroides (Herite de ObjetVolant)
    
    Attributes:
        Ceux de la superclasse ObjetVolant
    """ 
    def __init__(self, canvas, origine):
        """Permet de definir une asteroide 

        Initialise super et imageTk
            Args: 
                canvas (tk.Canvas): canvas où l'on dessine le carré
        """ 
        self.lienImage = "Image/asteroide.png" 
        super().__init__(canvas, 3, 1, 20, 20, origine, self.lienImage, 150, 150)

class Background:
    """Cette classe est represente l'arriere plan
    
    Attributes:
        imageTk: image de l'arriere plan
    """ 
    def __init__(self):
        self.imageBase = Image.open("Image/background.gif")
        self.image = self.imageBase.resize((1000,1000), Image.ANTIALIAS)
        self.imageTk = ImageTk.PhotoImage(self.image)
        
class Partie:
    """Cette classe représente une partie dans le jeu
        Attributes:
            tempsDebut(double): temps quand le minuteur commence
            nomJoueur(string): nom du joueur
            score(int): score de la partie
    """
    def __init__(self, nom):
        """Permet de definir la partie
            Initialise tempsDebut
        """
        self.score = 0
        self.nomJoueur = nom
        self.tempsDebut = time.time()  
        
    def addScore(self):
        """Permet d'augenter le score de cette partie
        """
        self.score += 5
        
    def getNom(self):
        """Permet de récupérer nom du joueur cette partie
        Returns:
            string: nom du joueur
        """
        return self.nomJoueur
    
    def getNom(self):
        """Permet de récupérer score cette partie
        Returns:
            string: score
        """
        return self.score
    
    def getTemps(self):
        """Permet de récupérer le temps depuis le debut de la partie
        Returns:
            double: temps passé depuis début de la partie
        """
        return round((time.time() - self.tempsDebut), 2)
