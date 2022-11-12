# -*- coding: utf8 -*-
from c31Geometry2 import *

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

