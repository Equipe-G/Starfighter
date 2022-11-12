class Vaisseau(Oval):
    def __init__(self, canvas, origine, vitesse, vie, petitRayon, grandRayon):
        self.vitesse = vitesse
        self.vie = vie
        self.petitRayon = petitRayon
        self.grandRayon = grandRayon
        super().__init__(canvas, origine, petitRayon, grandRayon, "red", "red", 0)

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
