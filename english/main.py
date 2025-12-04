# ==========================================================
# Importations nécessaires
# ==========================================================

# Import de la fonction 'init_pool' pour initialiser la connexion sécurisée
# à la base de données via un pool de connexions (dans database/pool.py)
from database.pool import init_pool

# Import du contrôleur principal qui gère les inscriptions et connexions utilisateurs
from controllers.auth_controller import AuthController


# ==========================================================
# Fonction principale : main()
# ----------------------------------------------------------
# C’est le point d’entrée du programme.
# Elle initialise la connexion à la base, puis lance le menu principal.
# ==========================================================
def main():
    try:
        # Tentative d’initialisation du pool de connexions à la base de données
        init_pool()
        # Si tout se passe bien, on peut continuer le programme normalement
    except Exception as e:
        # Si une erreur survient (mauvais identifiants, serveur PostgreSQL inactif…)
        # on affiche un message explicite et on arrête le programme.
        print(" Erreur de connexion à la base :", e)
        return

    # Boucle principale du menu textuel (interface console)
    while True:
        # Affichage du menu de navigation principal
        print("\n=== EBPay Auth System ===")
        print("1. Inscription")   # Permet de créer un compte
        print("2. Connexion")     # Permet de se connecter avec ses identifiants
        print("3. Quitter")       # Permet de sortir du programme

        # Lecture du choix de l’utilisateur
        choix = input("Choix : ")

        # Selon la sélection, on appelle la méthode appropriée du contrôleur
        if choix == "1":
            # Démarre le processus d’inscription
            AuthController.inscription()

        elif choix == "2":
            # Démarre le processus de connexion
            AuthController.connexion()

        elif choix == "3":
            # Sort proprement du programme
            print("Au revoir.")
            break

        else:
            # Si l’utilisateur entre un choix invalide, on affiche un message d’erreur
            print(" Choix invalide. Veuillez réessayer.")


# ==========================================================
# Point d’entrée du script
# ----------------------------------------------------------
# Cette condition garantit que le programme ne s’exécute
# que si le fichier est lancé directement (et non importé).
# ==========================================================

if __name__ == "__main__":
    main()
