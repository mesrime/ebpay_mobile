
commande pour importer le shema de la base de donnees sur son pc(postgre): psql -U postgres -d qrpaydb < database/ebpay.sql

Si un membre fait des modifications à la base :
    Il met à jour schema.sql
    Il fait un commit avec un message clair
    Les autres membres font un git pull et réappliquent si besoin
