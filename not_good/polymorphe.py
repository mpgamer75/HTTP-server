class Chien:
    # Le constructeur : initialise les caractéristiques de chaque chien créé
    def __init__(self, nom, race):
        self.nom = nom
        self.race = race

    # Une action que le chien peut effectuer
    def aboyer(self):
        print("Wouaf ! Wouaf !")

# Création d'objets (instances) de la classe Chien
mon_chien = Chien("Rex", "Berger Allemand")
autre_chien = Chien("Bella", "Caniche")

# Accès aux caractéristiques des objets
print(f"Le nom de mon chien est : {mon_chien.nom}")
print(f"La race de l'autre chien est : {autre_chien.race}")

# Appel d'une action (méthode) sur un objet
mon_chien.aboyer()
autre_chien.aboyer()


class Compteur:
    def __init__(self):
        self._valeur = 0  # Attribut "protégé"

    def incrementer(self):
        self._valeur += 1

    def get_valeur(self):
        return self._valeur

mon_compteur = Compteur()
mon_compteur.incrementer()
mon_compteur.incrementer()
print(mon_compteur.get_valeur())  # Accès contrôlé via une méthode

# Bien qu'on puisse accéder directement (ce qui n'est pas recommandé) :
# print(mon_compteur._valeur)


class Animal:
    def __init__(self, nom):
        self.nom = nom

    def faire_son(self):
        print("Son générique d'animal")

class Chat(Animal):
    def __init__(self, nom):
        # Appelle le constructeur de la classe parente (Animal)
        super().__init__(nom)

    # Redéfinition de la méthode faire_son pour les chats
    def faire_son(self):
        print("Miaou !")

mon_animal = Animal("Animal")
mon_chat = Chat("Mistigri")

mon_animal.faire_son()  # Output: Son générique d'animal
mon_chat.faire_son()    # Output: Miaou !

print(mon_chat.nom)     # Le chat hérite de l'attribut nom

def faire_parler(animal):
    animal.faire_son()

mon_animal = Animal("Animal")
mon_chat = Chat("Mistigri")

faire_parler(mon_animal)  # Output: Son générique d'animal
faire_parler(mon_chat)    # Output: Miaou !

class Forme:
    def aire(self):
        raise NotImplementedError("La méthode aire doit être implémentée par les sous-classes.")

class Rectangle(Forme):
    def __init__(self, largeur, hauteur):
        self.largeur = largeur
        self.hauteur = hauteur

    def aire(self):
        return self.largeur * self.hauteur

class Cercle(Forme):
    def __init__(self, rayon):
        self.rayon = rayon

    def aire(self):
        import math
        return math.pi * self.rayon**2

# On ne pourrait pas créer une instance directe de Forme (car sa méthode aire n'est pas implémentée)
# forme = Forme() # Cela lèverait une erreur

rectangle = Rectangle(5, 10)
cercle = Cercle(7)

print(f"L'aire du rectangle est : {rectangle.aire()}")
print(f"L'aire du cercle est : {cercle.aire()}")

class Temperature:
    def __init__(self, celsius):
        self._celsius = celsius

    def get_fahrenheit(self):
        return (self._celsius * 9/5) + 32

    # Propriété pour accéder à la température en Celsius
    celsius = property(fget=lambda self: self._celsius)

    # Propriété avec getter et setter
    def get_celsius(self):
        return self._celsius

    def set_celsius(self, value):
        if value < -273.15:
            raise ValueError("Température en dessous du zéro absolu !")
        self._celsius = value

    celsius_controllee = property(fget=get_celsius, fset=set_celsius)

ma_temperature = Temperature(25)
print(f"Température en Celsius : {ma_temperature.celsius}")
print(f"Température en Fahrenheit : {ma_temperature.get_fahrenheit()}")

ma_temperature.celsius_controllee = 30
print(f"Nouvelle température en Celsius : {ma_temperature.celsius_controllee}")

try:
    ma_temperature.celsius_controllee = -300
except ValueError as e:
    print(f"Erreur : {e}")

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"Point({self.x}, {self.y})"

    def __repr__(self):
        return f"Point(x={self.x}, y={self.y})"

    def __add__(self, autre_point):
        if not isinstance(autre_point, Point):
            raise TypeError("L'opérande doit être un objet Point.")
        return Point(self.x + autre_point.x, self.y + autre_point.y)

p1 = Point(1, 2)
p2 = Point(3, 4)

print(p1)         # Output: Point(1, 2) (grâce à __str__)
print([p1, p2])   # Output: [Point(x=1, y=2), Point(x=3, y=4)] (grâce à __repr__)

p3 = p1 + p2
print(p3)         # Output: Point(4, 6) (grâce à __add__)

# Tentative d'addition avec un autre type
try:
    resultat = p1 + (5, 6)
except TypeError as e:
    print(f"Erreur : {e}")