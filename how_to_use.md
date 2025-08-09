# Chaque collaborateur doit suivre ces étapes une seule fois au début :

## Aller dans le dossier de travail local
cd /chemin/vers/le/dossier/de/projets

## Cloner le dépôt
git clone https://github.com/TON-UTILISATEUR/ebpaypay_mobile.git

# Entrer dans le dossier du projet
cd ebpay_mobile


Créer une branche locale pour travailler
Chaque fois qu’un collaborateur commence une nouvelle tâche :

# Mettre à jour la branche dev
git checkout dev
git pull origin dev

# Créer une nouvelle branche à partir de dev
git checkout -b feature/nom-fonctionnalité


Enregistrer leurs changements localement (commit)

# Ajouter tous les fichiers modifiés au suivi
git add .

# Enregistrer un commit avec un message clair
git commit -m "Ajout du module de scan QR dans l'app mobile"


Envoyer le travail sur le dépôt GitHub (push)

git push origin feature/ajout-scan-qr


Créer une Pull Request sur GitHub
Aller sur GitHub dans le dépôt

Cliquer sur Compare & Pull Request

Remplir la description

Choisir comme base dev (jamais main directement)

Soumettre la PR pour qu'elle soit revue et fusionnée
