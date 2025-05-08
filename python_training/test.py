print("========================================Menu===========================================")
print("Bonjour veuillez entrer votre nom, prenom et age")
prenom = None
nom = None
age = None

# Boucle pour obtenir un âge valide
while age is None:
    try:
        age = int(input('Tu as quel age : '))
        if age < 0:
            print("Erreur, l\'age ne peut pas etre negatif")
            age = None
    except ValueError:
        print("Erreur : Veuillez entrer un nombre entier pour l'âge.")

# Boucle pour obtenir un prénom valide
while prenom is None or not isinstance(prenom, str) or not prenom.strip(): # Tant que prenom est nul, qu'il ne respecte pas son type ou qu'il est constituer d'espace blanc 9 espace blanc==> strip()
    prenom_input = input("Entrer votre prenom: ")
    if isinstance(prenom_input, str) and prenom_input.strip():
        prenom = prenom_input.strip()
    else:
        print("Erreur, le prenom doit etre une chaine de caracteres non vide.")

# Boucle pour obtenir un nom valide
while nom is None or not isinstance(nom, str) or not nom.strip():
    nom_input = input("Entrer votre nom : ")
    if isinstance(nom_input, str) and nom_input.strip():
        nom = nom_input.strip()
    else:
        print("Erreur, le nom doit etre une chaine de caracteres non vide.")

print(f"Bonjour {prenom} {nom}, vous avez {age} ans.")
print("**********************Fin***********************")