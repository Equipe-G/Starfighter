import tkinter as tk
import math
# Permet d'encapsuler une fonction et ses paramètres
from functools import partial, update_wrapper
from tkinter.tix import Tree
from turtle import pos

class LoopEvent:
    """Cette classe permet de définir une action à exécuter
       après un certain temps (par défaut 500 ms).
    """    

    def __init__(self, root, callback = lambda : print("Event"), timesleep = 500) :
        """Initialise le gestionnaire d'évènement

        :param root: Widget parent de notre boucle
        :type root: tk.Widget
        :param callback: Expression lambda ou fonction devant être exécuté à chaque boucle., defaults to print("Event")
        :type callback: lambda|function, optional
        :param timesleep: Temps en milliseconde entre chaque exécution., defaults to 500
        :type timesleep: int, optional
        """
        self.root = root
        self.function = callback
        self.timesleep = timesleep
        self.run = True

    def start(self) :
        """Lance l'exécution de la première boucle après un premier interval de la méthode
        """
        if self.run :
            self.root.after(self.timesleep, LoopEvent.prepareCallback(LoopEvent.__loop, self, self.function))

    def stop(self) :
        self.run = False

    def startImmediately(self) :
        """Lance immédiatement une première exécution de la méthode
        """
        LoopEvent.__loop(self, self.function)

    @staticmethod
    def __loop(event, callback) :
        """Permet de lancer la méthode et génère une nouvelle boucle

        :param event: Objet représentant la boucle de l'évènement
        :type event: LoppEvent
        :param callback: Expression lambda ou fonction devant être exécuté à chaque boucle.
        :type callback: function
        """
        callback()
        event.start()

    @staticmethod
    def prepareCallback(func, *args, **kwargs):
        """Fonction de préparation d'un callback pour une boucle d'évènement

        :param func: Expression lambda ou fonction devant être exécuté à chaque boucle.
        :type func: function|lambda
        :return: Callback préparer par partial
        :rtype: partial
        """
        partial_func = partial(func, *args, **kwargs)
        update_wrapper(partial_func, func)
        return partial_func

class Dash:
    """Représente un trait pour une ligne
    """

    def __init__(self, longueur, espace):
        """Crée un trait discontinue pour les lignes Tkinter

        :param longueur: Longueur en pixel d'un trait
        :type longueur: int
        :param espace: Espace en pixel entre deux trait
        :type espace: int
        :raises TypeError: Le paramètre longueur être de type int
        :raises TypeError: Le paramètre espace être de type int
        """
        if not isinstance(longueur, int) :
            raise TypeError("Le paramètre longueur être de type int")  
        if not isinstance(espace, int) :
            raise TypeError("Le paramètre espace être de type int")  
        
        self.longueur = longueur
        self.espace = espace

    def get_tkinter(self):
        """Fournit la description du trait pour tkinter

        :return: Tuple de int représentant les traits
        :rtype: int
        """        
        return (self.longueur, self.espace)
    
    @staticmethod
    def Empty():
        """Un trait vide ou plein selon le sens

        :return: La représentation d'un trait plein
        :rtype: None
        """
        return None

class Vecteur:
    """Classe représentant un vecteur dans un plan cartésien 2D
    """
    def __init__(self, x, y):
        """Initialise un vecteur

        :param x: Composante x du vecteur
        :type x: int|float
        :param y: Composante y du vecteur
        :type y: int|float
        """
        self.x = x
        self.y = y
        
    def __add__(self, other) :
        """Permet d'ajouter un vecteur au vecteur actuel. (Retourne un nouveau vecteur)

        :param other: vecteur à ajouter aux valeurs du vecteurs
        :type other: vecteur
        :raises TypeError: other doit être une instance de vecteur
        :return: Nouveau vecteur créer par l'addition des deux vecteurs en paramètre
        :rtype: vecteur
        """
        
        if not isinstance(other, Vecteur) :
            raise TypeError("Le paramètre être de type vecteur")

        return Vecteur(self.x + other.x, self.y + other.y)
    
    def __iadd__(self, other):
        """Ajouter les valeurs d'un vecteur au vecteur actuel

        :param other: Vecteur à ajouter à notre vecteur
        :type other: Vecteur
        :raises TypeError:other doit être une instance de vecteur
        """
        
        self = self.__add__(other)
        
    def __mul__(self, t):
        """Permet la multiplication du vecteur par un scalaire

        :param t: Scalaire utiliser dans la multiplication du vecteur
        :type t: float|int
        :raises TypeError: Le paramètre doit être une instance de float ou de int
        :return: Le vecteur grandit du facteur (scalaire)
        :rtype: Vecteur
        """
        
        if not isinstance(t, float) and not isinstance(t, int) :
            raise TypeError("Le paramètre doit être une instance de float ou de int")
        
        return Vecteur(self.x * t, self.y * t)
    
    def __imul__(self, t):
        """Permet la multiplication du vecteur par un scalaire

        :param t: Scalaire utiliser dans la multiplication du vecteur
        :type t: float|int
        :raise TypeError: other doit être une instance de vecteur
        """
        
        self = self.__mul__(t)
        
    def __sub__(self, other):
        """Permet de soustraire un vecteur à un autre

        Args:
            other (Vecteur): Vecteur que l'on retire au vecteur

        Raises:
            TypeError: other doit être une instance de vecteur

        Returns:
            Vecteur: Le nouveau vecteur calculer
        """
        sub = other * -1
        return self.__add__(sub)
    
    def __isub__(self, other):
        """Permet de soustraire un vecteur à un autre

        Args:
            other (Vecteur): Vecteur que l'on retire au vecteur

        Raises:
            TypeError: other doit être une instance de vecteur
        """
        self = self.__sub__(other)
        
    def norme(self):
        """Détermine la norme du vecteur avec l'origine

        Returns:
            float: Longueur du vecteur avec l'origine
        """
        return math.sqrt((self.x ** 2) + ((self.y ** 2)))
    
    def distance(self, other):
        """Calcul la distance entre deux points

        Args:
            other (Vecteur): Vecteur à calculer

        Raises:
            TypeError: other doit être une instance de vecteur

        Returns:
            float: La distance entre les deux vecteurs
        """
        if not isinstance(other, Vecteur) :
            raise TypeError("Le paramètre être de type vecteur")
        
        return math.sqrt((other.x - self.x)**2 + (other.y - self.y)**2)
    
    def unitaire(self):
        """Fournit un vecteur unitaire dans la direction du vecteur

        Returns:
            Vecteur: Vecteur unitaire dans la direction du vecteur
        """
        return self / self.norme()
    
    def get_coordonnee(self):
        """Récupère les coordonnées de l'objet

        Returns:
            tuple(float, float): Tuple contenant les positions X, Y du vecteur
        """
        return (self.x, self.y)

    def zero():
        """Fournit un vecteur null

        Returns:
            Vecteur: Vecteur null
        """
        return Vecteur(0, 0)
    
    def gauche():
        """Fournit un vecteur unitaire vers la gauche (x = -1)

        Returns:
            Vecteur: Vecteur unitaire vers la gauche (x = -1)
        """
        return Vecteur(-1, 0)

    def droite():
        """Fournit un vecteur unitaire vers la droite (x = 1)

        Returns:
            Vecteur: Vecteur unitaire vers la droite (x = 1)
        """
        return Vecteur(1, 0)
    
    def haut():
        """Fournit un vecteur unitaire vers le haut (y = -1)

        Returns:
            Vecteur: Vecteur unitaire vers la haut (y = -1)
        """
        return Vecteur(0, -1)

    def bas():
        """Fournit un vecteur unitaire vers le bas (y = 1)

        Returns:
            Vecteur: Vecteur unitaire vers la bas (y = 1)
        """
        return Vecteur(0, 1)
        
    def __str__(self):
        return f"({self.x}, {self.y})"
    
    def __eq__(self, other):
        """Détermine si les deux objets sont égaux

        :param other: Objet à vérifier
        :type other: object
        :return: True si les deux objets sont égaux
        :rtype: bool
        """
        if not isinstance(other, Vecteur) :
            return False
        
        return self.x == other.x and self.y == other.y
    
    def __ne__(self, other):
        """Détermine si les deux objets sont différent

        :param other: Objet à vérifier
        :type other: object
        :return: True si les deux objets sont égaux
        :rtype: bool
        """
        if not isinstance(other, Vecteur) :
            return False
        
        return self.x != other.x or self.y != other.y
    
    def __str__(self):
        return "{" + self.x + "; " + self.y + "}"

class Rotation:
    """Classe représentant une rotation matriciel utilisable sur les vecteurs de la bibliothèque

    Raises:
        TypeError: Le paramètre « angle » n'est pas de type float ou int
    """
    def __init__(self, angle):
        """Crée une instance objet de la classe Rotation

        Args:
            angle (float | int): Angle de la rotation 

        Raises:
            TypeError: Le paramètre « angle » n'est pas de type float ou int        
        """        
        self.set_angle(angle)
        
    def set_angle(self, angle) :
        """Définit l'angle de la rotation

        Args:
            angle (float | int): Angle de la rotation 

        Raises:
            TypeError: Le paramètre « angle » n'est pas de type float ou int
        """
        if not isinstance(angle, float) and not isinstance(angle, int) :
            raise TypeError("Le paramètre « angle » doit être une instance de float ou de int alors qu'il est de type : ", type(angle))
        self.sinus = math.sin(angle)
        self.cosinus = math.sqrt(1 - (self.sinus ** 2))
        
    def get_angle(self):
        """Retourne l'angle de la matrice de Rotation

        Returns:
            (int|float): Angle de la rotation
        """
        return math.acos(self.cosinus)
        
    def rotate(vecteur, angle) :
        """Permet la rotation d'un vecteur

        Args:
            vecteur (Vecteur): Vecteur à rotationner
            angle (float|int): Angle de la rotation

        Raises:
            TypeError: Le paramètre vecteur doit être de type vecteur
            TypeError: Le paramètre angle doit être de type float ou int

        Returns:
            Vecteur: Le vecteur ayant sublit la rotation
        """
        
        R = Rotation(angle)
        return R.rotate(vecteur)
        
    def rotate(self, vecteur) :
        """Permet la rotation d'un vecteur à partir de la matrice

        Args:
            vecteur (Vecteur): Vecteur à rotationner

        Raises:
            TypeError: Le paramètre vecteur doit être de type vecteur

        Returns:
            Vecteur: Le vecteur ayant sublit la rotation
        """
        if not isinstance(vecteur, Vecteur):
            raise TypeError("Le paramètre doit être un vecteur")
    
        return Vecteur(
            vecteur.x * self.cosinus - vecteur.y * self.sinus,
            vecteur.x * self.sinus + vecteur.y * self.cosinus
        )
        
    def __mult__(self, vecteur) :
        """Permet la rotation d'un vecteur à partir de la matrice

        Args:
            vecteur (Vecteur): Vecteur à rotationner

        Raises:
            TypeError: Le paramètre vecteur doit être de type vecteur

        Returns:
            Vecteur: Le vecteur ayant sublit la rotation
        """
        return self.rotate(vecteur)
    
class Polygone:
    """Représentation abstraite d'un polygone
    """
    def __init__(self, canvas, origine, remplissage = "black", bordure = "black", epaisseur = 1):
        """Permet de définir la base d'un polygone

        Args:
            canvas (tk.Canvas): canvas où l'on dessine la Polygone
            origine (Vecteur): Point d'origine de la Polygone (au centre de celle-ci)
            remplissage (string): Couleur du remplissage, par défaut "black"
            bordure (string): Couleur de la bordure, par défaut "black"
            epaisseur (int): Épaisseur de la bordure

        Raises:
            TypeError: Le paramètre canvas doit être de type tk.Canvas
            TypeError: Le paramètre origine doit être de type Vecteur
            TypeError: Le paramètre remplissage doit être de type string
            TypeError: Le paramètre bordure doit être de type string
            TypeError:Le paramètre epaisseur doit être de type int
        """
        if not isinstance(canvas, tk.Canvas):
            raise TypeError("Le paramètre canvas doit être de type tk.Canvas")
        if not isinstance(origine, Vecteur):
            raise TypeError("Le paramètre origine doit être de type Vecteur")
        if not isinstance(remplissage, str):
            raise TypeError("Le paramètre remplissage doit être de type string")
        if not isinstance(bordure, str):
            raise TypeError("Le paramètre bordure doit être de type string")
        if not isinstance(epaisseur, int):
            raise TypeError("Le paramètre epaisseur doit être de type int")
        
        self.canvas = canvas
        self.origine = origine
        self._vertex = []
        self.remplissage = remplissage
        self.bordure = bordure
        self.epaisseur = epaisseur
        
    def get_coordonnees(self):
        """Récupère un tableau des coordonnées de tous les points

        Returns:
            Array of Vecteur: Talbeau des coordonnées de tous les points
        """
        return [vex.get_coordonnee() for vex in self._vertex]
        
    def draw(self):
        """Permet de dessiner la Polygone
        """
        if hasattr(self, 'id'):
            self.canvas.delete(self.id)
            
        self.id = self.canvas.create_polygon(self.get_coordonnees(), fill=self.remplissage, outline=self.bordure, width=self.epaisseur)
        
        self.canvas.update()
        
    def rotate_mat(self, R):
        """Permet de tourner la Polygone

        Args:
            R (Rotation): Matrice de rotation à appliquer

        Raises:
            TypeError: Le paramètre doit être de type Rotation
        """
        if not isinstance(R, Rotation):
            raise TypeError("Le paramètre doit être de type Rotation")
        
        bary = self.get_barycentre()
        self.translate(bary * -1)
        self._vertex = [R.rotate(vex) for vex in self._vertex]
        self.translate(bary)        
        
    def rotate(self, angle):
        """Permet de tourner la Polygone

        Args:
            angle (float|int): Angle de la rotation

        Raises:
            TypeError: Le paramètre doit être de type float ou int
        """
        if not isinstance(angle, float) and not isinstance(angle, int):
            raise TypeError("Le paramètre doit être de type float ou int")
        
        self.rotate_mat(Rotation(angle))
        
    def resize(self, facteur):
        """Effectue une redimension de la Polygone

        Args:
            facteur (float|int): Facteur de redimension

        Raises:
            TypeError: Le paramètre doit être de type float ou int
        """
        if not isinstance(facteur, float) and not isinstance(facteur, int):
            raise TypeError("Le paramètre doit être de type float ou int")
        
        bary = self.get_barycentre()
        self.translate(bary * -1)
        self._vertex = [vex * facteur for vex in self._vertex]
        self.translate(bary)  
        
    def translate(self, direction):
        """Effectue une translation de la Polygone

        Args:
            direction (Vecteur): Direction de la translation

        Raises:
            TypeError: Le paramètre doit être de type Vecteur
        """
        if not isinstance(direction, Vecteur) :
            raise TypeError("Le paramètre doit être de type Vecteur")
        
        self._vertex = [ver + direction for ver in self._vertex]
        
    def set_remplissage(self, remplissage) :
        """Modifie la couleur du remplissage de la Polygone

        Args:
            remplissage (string): Couleur du remplissage

        Raises:
            TypeError: Le paramètre remplissage doit être de type string
        """
        if not isinstance(remplissage, str):
            raise TypeError("Le paramètre remplissage doit être de type string")
        self.remplissage = remplissage
        
    def set_bordure(self, bordure):
        """Modifie la couleur de la bordure de la Polygone

        Args:
            bordure (string): Couleur de la bordure

        Raises:
            TypeError: Le paramètre bordure doit être de type string
        """
        if not isinstance(bordure, str):
            raise TypeError("Le paramètre bordure doit être de type string")
        self.bordure = bordure
        
    def set_epaisseur(self, epaisseur):
        """Modifie l'épaisseur de la bordure

        Args:
            epaisseur (int): Épaisseur de la bordure

        Raises:
            TypeError: Le paramètre epaisseur doit être de type int
        """
        if not isinstance(epaisseur, int):
            raise TypeError("Le paramètre epaisseur doit être de type int")
        self.epaisseur = epaisseur

    def get_barycentre(self):
        """Obtient le centre du polygone (barycentre)

        Returns:
            Vecteur: Centre du polygone
        """
        bary = Vecteur(0, 0)
        for ver in self._vertex:
            bary = bary + ver
        return bary * (1 / len(self._vertex))
        
    def get_position(self):
        """Permet de récupérer la position

        :return: Position de l'objet
        :rtype: Vecteur
        """
        return self.origine
    
    def set_position(self, position):
        """Permet de modifier la position de la forme

        :param position: Nouvelle position
        :type position: Vecteur
        :raises TypeError: Le paramètre doit être de type Vecteur
        """
        if not isinstance(position, Vecteur) :
            raise TypeError("Le paramètre doit être de type Vecteur")
        self.origine = position
        
    def get_origine(self) -> Vecteur:
        """Permet de récupérer l'origine du polygone

        Returns:
            Vecteur: Origine du polygone
        """
        return self.origine
    
    def translateTo(self, position:Vecteur) -> None:
        """_summary_

        Args:
            position (Vecteur): Position où déplacer le polygone

        Raises:
            TypeError: Le paramètre doit être de type Vecteur
        """
        self.translate(position - self.origine)
                    
class Ligne(Polygone):
    """Représente une ligne (hérite de Polygone)
    """
    
    def __init__(self, canvas, origine, longueur, orientation, bordure = "black", dash = None, epaisseur = 1):
        """Permet de créer une ligne

        Args:
            canvas (tk.Canvas): canvas où l'on dessine la Polygone
            origine (Vecteur): Point d'origine de la Polygone (au centre de celle-ci)
            longueur (float|int): Longueur de la ligne
            orientation (float|int): Orientation dans le plan de la ligne
            bordure (string): Couleur de la bordure, par défaut "black"
            dash (Dash): Format du trait discontinue, par défaut aucun (None)
            epaisseur (int): Épaisseur de la bordure

        Raises:
            TypeError: Le paramètre canvas doit être de type tk.Canvas
            TypeError: Le paramètre origine doit être de type Vecteur
            TypeError: Le paramètre longueur doit être de type float ou int
            TypeError: Le paramètre orientation doit être de type float ou int
            TypeError: Le paramètre bordure doit être de type string
            TypeError:Le paramètre epaisseur doit être de type int
        """
        super().__init__(canvas, origine, bordure, bordure, epaisseur)
        
        if not isinstance(longueur, float) and not isinstance(longueur, int) :
            raise TypeError("Le paramètre longueur doit être de type float ou int")
        
        if not isinstance(orientation, float) and not isinstance(orientation, int) :
            raise TypeError("Le paramètre orientation doit être de type float ou int")
        
        if dash is not None and not isinstance(dash, Dash) :
            raise TypeError("Le paramètre dash doit être de type Dash ou None")
                
        demi_longueur = longueur / 2
        
        
        self._vertex.append(self.origine - Vecteur(
            demi_longueur * math.cos(orientation),
            demi_longueur * math.sin(orientation)
        ))
        
        self._vertex.append(self.origine + Vecteur(
            demi_longueur * math.cos(orientation),
            demi_longueur * math.sin(orientation)
        ))
        
        self.dash = dash
        
    def draw(self):
        """Permet de dessiner la Polygone
        """
        if hasattr(self, 'id'):
            self.canvas.delete(self.id)
            
        if self.dash is not None:
            self.id = self.canvas.create_line(self.get_coordonnees(), fill=self.remplissage, dash=self.dash.get_tkinter(), width=self.epaisseur)
        else:
            self.id = self.canvas.create_line(self.get_coordonnees(), fill=self.remplissage, width=self.epaisseur)
        
        self.canvas.update()
        
class Rectangle(Polygone):
    """Représente un rectangle (hérite de Polygone)
    """
    def __init__(self, canvas, origine, largeur, hauteur, orientation = 0, remplissage="black", bordure="black", epaisseur=1):
        """Permet de créer un rectangle

        Args:
            canvas (tk.Canvas): canvas où l'on dessine la Polygone
            origine (Vecteur): Point d'origine de la Polygone (au centre de celle-ci)
            largeur (int|float): Largeur (selon l'axe x) du rectangle
            hauteur (int|float): Hauteur (selon l'axe y) du rectangle
            orientation (float|int): Orientation dans le plan par défaut 0
            remplissage (string): Couleur du remplissage, par défaut "black"
            bordure (string): Couleur de la bordure, par défaut "black"
            epaisseur (int): Épaisseur de la bordure

        Raises:
            TypeError: Le paramètre canvas doit être de type tk.Canvas
            TypeError: Le paramètre origine doit être de type Vecteur
            TypeError: Le paramètre largeur doit être de type float ou int
            TypeError: Le paramètre hauteur doit être de type float ou int
            TypeError: Le paramètre orientation doit être de type float ou int
            TypeError: Le paramètre remplissage doit être de type string
            TypeError: Le paramètre bordure doit être de type string
            TypeError:Le paramètre epaisseur doit être de type int
        """
        super().__init__(canvas, origine, remplissage, bordure, epaisseur)
        
        if not isinstance(largeur, float) and not isinstance(largeur, int) :
            raise TypeError("Le paramètre largeur doit être de type float ou int")
        
        if not isinstance(hauteur, float) and not isinstance(hauteur, int) :
            raise TypeError("Le paramètre hauteur doit être de type float ou int")
        
        if not isinstance(orientation, float) and not isinstance(orientation, int) :
            raise TypeError("Le paramètre orientation doit être de type float ou int")
        
        demi_largeur = largeur / 2
        demi_hauteur = hauteur / 2
        
        # Coin haut gauche
        self._vertex.append(
            self.origine + Vecteur(
                demi_largeur * -1,
                demi_hauteur * -1
            )
        )
        
        # Coin haut droite
        self._vertex.append(
            self.origine + Vecteur(
                demi_largeur * 1,
                demi_hauteur * -1
            )
        )
        
        # Coin bas droite
        self._vertex.append(
            self.origine + Vecteur(
                demi_largeur * 1,
                demi_hauteur * 1
            )
        )
        
        # Coin bas gauche
        self._vertex.append(
            self.origine + Vecteur(
                demi_largeur * -1,
                demi_hauteur * 1
            )
        )
        
        self.rotate(orientation)
        
class Carre(Rectangle):
    """Représente un carré (hérite de Rectangle)
    """
    def __init__(self, canvas, origine, largeur, orientation = 0, remplissage="black", bordure="black", epaisseur=1):
        super().__init__(canvas, origine, largeur, largeur, orientation, remplissage, bordure, epaisseur)

class Oval(Polygone):
    """Permet de dessiner un Oval (hérite de Oval)
    """
    def __init__(self, canvas, origine, petit_rayon, grand_rayon, remplissage="black", bordure="black", epaisseur=1):
        """Permet de définir un Oval

        Args:
            canvas (tk.Canvas): canvas où l'on dessine la Polygone
            origine (Vecteur): Point d'origine de la Polygone (au centre de celle-ci)
            petit_rayon (int|float): Petit rayon du cercle
            remplissage (string): Couleur du remplissage, par défaut "black"
            bordure (string): Couleur de la bordure, par défaut "black"
            epaisseur (int): Épaisseur de la bordure

        Raises:
            TypeError: Le paramètre canvas doit être de type tk.Canvas
            TypeError: Le paramètre origine doit être de type Vecteur
            TypeError: Le paramètre remplissage doit être de type string
            TypeError: Le paramètre bordure doit être de type string
            TypeError: Le paramètre petit_rayon doit être de type float ou int
            TypeError: Le paramètre epaisseur doit être de type int
        """
        super().__init__(canvas, origine, remplissage, bordure, epaisseur)
        
        if not isinstance(petit_rayon, int) and not isinstance(petit_rayon, float):
            raise TypeError("Le paramètre petit_rayon doit être de type float ou int")
        
        self._vertex.append(
            self.origine - Vecteur(
                grand_rayon,
                petit_rayon
            )
        )
        
        self._vertex.append(
            self.origine + Vecteur(
                grand_rayon,
                petit_rayon
            )
        )
        
    def draw(self):
        """Permet de dessiner le cercle
        """
        if hasattr(self, 'id'):
            self.canvas.delete(self.id)
         
        self.id = self.canvas.create_oval(self._vertex[0].x, self._vertex[0].y, self._vertex[1].x, self._vertex[1].y, fill=self.remplissage, outline=self.bordure, width=self.epaisseur)
        
        self.canvas.update()
        
    def rotate_mat(self, R):
        """Permet de tourner la Polygone

        Args:
            R (Rotation): Matrice de rotation à appliquer

        Raises:
            TypeError: Le paramètre doit être de type Rotation
        """
        pass
        if not isinstance(R, Rotation):
            raise TypeError("Le paramètre doit être de type Rotation")
        
        bary = self.get_barycentre()
        self.translate(bary * -1)
        self._vertex = [R.rotate(vex) for vex in self._vertex]
        self.translate(bary)  
        
class Cercle(Oval):
    """Permet de dessiner un Oval (hérite de Oval)
    """
    
    def __init__(self, canvas, origine, rayon, remplissage="black", bordure="black", epaisseur=1):
        """Permet de définir un Oval

        Args:
            canvas (tk.Canvas): canvas où l'on dessine la Polygone
            origine (Vecteur): Point d'origine de la Polygone (au centre de celle-ci)
            rayon (int|float): Rayon du cercle
            remplissage (string): Couleur du remplissage, par défaut "black"
            bordure (string): Couleur de la bordure, par défaut "black"
            epaisseur (int): Épaisseur de la bordure

        Raises:
            TypeError: Le paramètre canvas doit être de type tk.Canvas
            TypeError: Le paramètre origine doit être de type Vecteur
            TypeError: Le paramètre remplissage doit être de type string
            TypeError: Le paramètre bordure doit être de type string
            TypeError:Le paramètre epaisseur doit être de type int
        """
        super().__init__(canvas, origine, rayon, rayon, remplissage, bordure, epaisseur)
        
class Croix(Polygone):
    """Permet de définir un X
    """
    
    def __init__(self, canvas, origine, largeur, hauteur, orientation = 0, bordure="black", dash = None, epaisseur=1):
        """Permet de définir la base d'un polygone

        Args:
            canvas (tk.Canvas): canvas où l'on dessine la Polygone
            origine (Vecteur): Point d'origine de la Polygone (au centre de celle-ci)
            largeur (int|float): Largeur du X
            hauteur (int|float): Hauteur du X
            orientation (float|int): Orientation dans le plan par défaut 0
            bordure (string): Couleur de la bordure, par défaut "black"
            epaisseur (int): Épaisseur de la bordure

        Raises:
            TypeError: Le paramètre canvas doit être de type tk.Canvas
            TypeError: Le paramètre origine doit être de type Vecteur
            TypeError: Le paramètre remplissage doit être de type string
            TypeError: Le paramètre largeur doit être de type float ou int
            TypeError: Le paramètre hauteur doit être de type float ou int
            TypeError: Le paramètre orientation doit être de type float ou int
            TypeError: Le paramètre bordure doit être de type string
            TypeError: Le paramètre epaisseur doit être de type int
        """
        super().__init__(canvas, origine, bordure, bordure, epaisseur)
        
        if not isinstance(largeur, float) and not isinstance(largeur, int) :
            raise TypeError("Le paramètre largeur doit être de type float ou int")
        
        if not isinstance(hauteur, float) and not isinstance(hauteur, int) :
            raise TypeError("Le paramètre hauteur doit être de type float ou int")
        
        if not isinstance(orientation, float) and not isinstance(orientation, int) :
            raise TypeError("Le paramètre orientation doit être de type float ou int")
        
        dl = largeur / 2
        dh = hauteur / 2
        
        # coin haut gauche
        self._vertex.append(
            self.origine + Vecteur(
                -dl,
                -dh
            )
        )
        
        # coin bas droit
        self._vertex.append(
            self.origine + Vecteur(
                dl,
                dh
            )
        )
        
        # coin haut droit
        self._vertex.append(
            self.origine + Vecteur(
                dl,
                -dh
            )
        )
        
        # coin bas gauche
        self._vertex.append(
            self.origine + Vecteur(
                -dl,
                dh
            )
        )
        
        self.rotate(orientation)
        
    def draw(self):
        """Permet de dessiner la Polygone
        """
        if hasattr(self, 'id_1'):
            self.canvas.delete(self.id_1)
        if hasattr(self, 'id_2'):
            self.canvas.delete(self.id_2)
            
        self.id_1 = self.canvas.create_line(self._vertex[0].get_coordonnee(), self._vertex[1].get_coordonnee(),
                    fill=self.remplissage, width=self.epaisseur)
        self.id_2 = self.canvas.create_line(self._vertex[2].get_coordonnee(), self._vertex[3].get_coordonnee(),
                    fill=self.remplissage, width=self.epaisseur)
        
        self.canvas.update()