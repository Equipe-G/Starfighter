from c31Geometry2 import *
from PIL import ImageTk
from PIL import Image

class objetVolant(Oval): 
    def __init__(self, canvas, vitesse, vie, petitRayon, grandRayon, origine, lienImage):
        self.vitesse = vitesse
        self.vie = vie
        self.petitRayon = petitRayon
        self.grandRayon = grandRayon
        self.imageBase = Image.open(lienImage)
        self.image = self.imageBase.resize((200,200), Image.ANTIALIAS)
        self.imageTk = ImageTk.PhotoImage(self.image)
        super().__init__(canvas, origine, self.petitRayon, self.grandRayon, "white", "white", 0)

    def getOrigine(self) -> Vecteur:
        return super().get_position()

    def modificationPos(self, position: Vecteur):
        self.origine = position
        super().translateTo(position)

    def getVitesse(self):
        return self.vitesse

    def setVitesse(self, vitesse):
        self.vitesse = vitesse

    def getVie(self):
        return self.vie

    def setVie(self, vie):
        self.vie = vie

    def getPetitRayon(self):
        return self.petitRayon

    def setPetitRayon(self, petitRayon):
        self.petitRayon = petitRayon

    def getGrandRayon(self):
        return self.grandRayon

    def setGrandRayon(self, grandRayon):
        self.grandRayon = grandRayon
        
class PowerUp(Cercle):
    def __init__(self, canvas, origine, lienImage):
        self.vitesse = 3
        self.rayon = 10
        self.imageBase = Image.open(lienImage)
        self.image = self.imageBase.resize((50,50), Image.ANTIALIAS)
        self.imageTk = ImageTk.PhotoImage(self.image)
        super().__init__(canvas, origine, self.rayon, "white", "white", 0)
    
    def getOrigine(self) -> Vecteur:
        return super().get_position()

    def modificationPos(self, position: Vecteur):
        self.origine = position
        super().translateTo(position)

    def getVitesse(self):
        return self.vitesse

    def setVitesse(self, vitesse):
        self.vitesse = vitesse

    def getRayon(self): 
        return self.rayon
    
    def setRayon(self, rayon):
        self.rayon = rayon

class Projectile(objetVolant):
    def __init__(self, canvas):
        self.lienImage = "Image/Lazer.png"
        self.image = self.imageBase.resize((50,50), Image.ANTIALIAS)
        self.imageTk = ImageTk.PhotoImage(self.image)
        super().__init__(canvas, 10, 0, 0, 1, Vecteur(5,15), self.lienImage)

    def getOrigine(self) -> Vecteur:
        """Permet de récupérer l'origine du projectile
        Returns:
            Vecteur: Origine du projectile
        """
        return super().get_position()

    def modificationPos(self, position: Vecteur):
        """Définit l'origine du carré et le deplace
        Args:
            position (Vecteur): Nouvelle position du carré
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
    def __init__(self, canvas):
        self.lienImage = "Image/Vaisseau.png"
        super().__init__(canvas, 10, 100, 50, 100, Vecteur(500,900), self.lienImage)

class Ovni(objetVolant):
    def __init__(self, canvas, origine, maxY):
        self.maxY = maxY
        self.lienImage = "Image/Alien.png"
        super().__init__(canvas, 5, 10, 20, 50, origine, self.lienImage)
        
    def getMaxY(self):
        return self.maxY

class asteroides(objetVolant):
    def __init__(self, canvas, origine):
        self.lienImage = "Image/asteroide.png" 
        super().__init__(canvas, 3, 1, 20, 20, origine, self.lienImage)

class Background():
    def __init__(self, canvas):
        self.imageBase = Image.open("Image/background.gif")
        self.image = self.imageBase.resize((1000,1000), Image.ANTIALIAS)
        self.imageTk = ImageTk.PhotoImage(self.image)
        
#class boss(Ovni)

