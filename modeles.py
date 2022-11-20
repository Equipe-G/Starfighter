# -*- coding: utf8 -*-
from c31Geometry2 import *

class objetVolant(Oval): 
    def __init__(self, canvas, vitesse, vie, petitRayon, grandRayon, origine):
        self.vitesse = vitesse
        self.vie = vie
        self.petitRayon = petitRayon
        self.grandRayon = grandRayon
        super().__init__(canvas, origine, self.petitRayon, self.grandRayon, "white", "white", 0)

    def getOrigine(self) -> Vecteur:
        return super().getOrigine()

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
    def __init__(self, canvas, origine):
        self.vitesse = 3
        self.rayon = 10
        super().__init__(canvas, origine, self.rayon, "white", "white", 0)
    
    def getOrigine(self) -> Vecteur:
        return super().getOrigine()

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

class Projectile(Oval):
    def __init__(self, canvas, origine):
        self.petitRayon = 5
        self.grandRayon = 10
        self.vitesse = 1
        super().__init__(canvas, origine, self.petitRayon, self.grandRayon, "white", "white, 0")

    def getOrigine(self) -> Vecteur:
        """Permet de récupérer l'origine du projectile
        Returns:
            Vecteur: Origine du projectile
        """
        return super().get_origine()

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
        super().__init__(canvas, 10, 100, 50, 100 , Vecteur(100,500))

class Ovni(objetVolant):
    def __init__(self, canvas, origine):
        super().__init__(canvas, 5, 10, 20, 50 , origine)

class asteroides(objetVolant):
    def __init__(self, canvas, origine):
        super().__init__(canvas, 3, 1, 20, 20, origine)

