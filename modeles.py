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
        self.id = ""
        self.power = power

        if self.power == 1:
            self.lienImage = "Image/powerUp1.png"
        elif self.power == 2:
            self.lienImage = "Image/powerUp2.png"
        elif self.power == 3:
            self.lienImage = "Image/powerUp3.png"

        super().__init__(canvas, 0, 1, 30, 45, origine, self.lienImage, 30, 45)

    def activerPouvoir(self, vaisseau):
        if self.power == 1:
            vaisseau.setVitesse(20)
        elif self.power == 2:
            vaisseau.setVie(vaisseau.getVie() + 5)
        elif self.power == 3:
            self.power = self.power #placeholder
        #pour en faire un avec la taille du vasseau faudrais changer petit rayon grand rayon et resize l'image

    def desactiverPouvoir(self, vaisseau):
        if self.power == 1:
            vaisseau.setVitesse(10)
        elif self.power == 2:
            self.power = self.power #placeholder
        elif self.power == 3:
            self.power = self.power #placeholder
    
    


class Projectile(objetVolant):
    """Cette classe est represente un projectile tire par un vaisseau ou ovni (Herite de ObjetVolant)
    
    Attributes:
        Ceux de la superclasse ObjetVolant
    """ 
    def __init__(self, canvas, origine):
        """Permet de definir un projectile 

        Initialise super et imageTk
            Args: 
                canvas (tk.Canvas): canvas où l'on dessine le carré
        """ 
        self.lienImage = "Image/Lazer.png"
        self.id = ""
        super().__init__(canvas, 10, 1, 40, 40, origine, self.lienImage, 40, 40)
        
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
        self.id = ""
        super().__init__(canvas, 10, 100, 200, 200 , Vecteur(500, 900), self.lienImage, 200, 200)

class Ovni(objetVolant):
    """Cette classe est represente un ovni ennemi (Herite de ObjetVolant)
    
    Attributes:
        Ceux de la superclasse ObjetVolant
        maxY(int): le plus haut que l'ovni peut aller
    """ 
    def __init__(self, canvas, origine, maxY, taille = 150):
        """Permet de definir un ovni 

        Initialise super et imageTk
            Args: 
                canvas (tk.Canvas): canvas où l'on dessine le carré
        """ 
        self.maxY = maxY
        self.lienImage = "Image/Alien.png"
        super().__init__(canvas, 5, 10, taille, taille, origine, self.lienImage, taille, taille)
        
    def getMaxY(self):
        """Permet de récupérer le maxY de l'ovni
        Returns:
            int: le plus haut que l'ovni peut aller
        """
        return self.maxY

class Boss(Ovni):
    """Cette classe est represente un boss ennemi (Herite de Ovni)
    
    Attributes:
        Ceux de la superclasse Ovni
    """ 
    def __init__(self, canvas, origine, maxY):
        """Permet de definir un boss
        Initialise super et imageTk
            Args: 
                canvas (tk.Canvas): canvas où l'on dessine le carré
        """ 
        super().__init__(canvas, origine, maxY, 300)

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
        self.id = "" 
        super().__init__(canvas, 3, 1, 150, 150, origine, self.lienImage, 150, 150)

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
    
    def getScore(self):
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
