# Base de Données ebPay

## 🔧 Configuration
- Type : PostgreSQL
- Nom : ebpay
- Utilisateur : postgres
- Mot de passe : (à configurer localement)
- Port : 5432

## 📦 Initialisation
Pour créer la base localement :

```bash
createdb ebpay
psql -U postgres -d qrpaydb < ebpay.sql

##  mise a jour

Quand une modification est faite :

Modifier ebpay.sql

Ajouter un commentaire clair dans le commit

Faire un git push

Les autres membres font un git pull et mettent à jour chez eux
