# Fonction qui permet de calculer la factoriele d'un nombre 

n = int(input("Entrer un nombre: "))
resultat = None

def factorielle(n_int):
    if n_int == 0:
        return 1
    else:
        return n_int*factorielle(n_int-1)
    
try:
    n_int = int(n)
    if n_int < 0 :
        print("Erreur : Veuillez entrer un nombre entier non négatif.")
    else:
        resultat = factorielle(n_int)
        print(f"La factorielle de {n_int} est {resultat}")
except ValueError:
    print("erreur, valeurs incorrects")


