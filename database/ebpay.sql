CREATE TABLE `administrateur` (
  `id` char(36) NOT NULL,
  `role` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `client`
--

CREATE TABLE `client` (
  `id` char(36) NOT NULL,
  `code_pin` int(11) NOT NULL,
  `qr_code_id` char(36) DEFAULT NULL,
  `niveau_verification` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `kyc_document`
--

CREATE TABLE `kyc_document` (
  `id` varchar(36) NOT NULL,
  `utilisateur_id` char(36) DEFAULT NULL,
  `type_document` enum('CNI','PASSEPORT','PERMIS') DEFAULT NULL,
  `numero_document` varchar(50) DEFAULT NULL,
  `date_soumission` timestamp NOT NULL DEFAULT current_timestamp(),
  `etat` enum('EN_ATTENTE','VALIDE','REJETE') DEFAULT NULL,
  `justification_refus` char(10) DEFAULT NULL,
  `url_fichier` char(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `marchand`
--

CREATE TABLE `marchand` (
  `id` char(36) NOT NULL,
  `nom_commercial` varchar(100) DEFAULT NULL,
  `localisation` varchar(25) DEFAULT NULL,
  `qr_paiement_fixe_id` char(36) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `notification`
--

CREATE TABLE `notification` (
  `id` char(36) NOT NULL,
  `utilisateur_id` char(36) DEFAULT NULL,
  `titre` varchar(150) DEFAULT NULL,
  `contenu` varchar(750) DEFAULT NULL,
  `date_envoi` timestamp NOT NULL DEFAULT current_timestamp(),
  `type` enum('TRANSACTION','SYSTEME','ADMIN') DEFAULT NULL,
  `vu` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `portefeuille`
--

CREATE TABLE `portefeuille` (
  `id` char(36) NOT NULL,
  `utilisateur_id` char(36) DEFAULT NULL,
  `solde` float DEFAULT 0,
  `devise` varchar(10) DEFAULT NULL,
  `date_derniere_mise_a_jour` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `qrcode`
--

CREATE TABLE `qrcode` (
  `id` char(36) NOT NULL,
  `valeur` varchar(750) DEFAULT NULL,
  `valide_jusqu_a` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `date_creation` timestamp NOT NULL DEFAULT current_timestamp(),
  `est_statique` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `transaction`
--

CREATE TABLE `transaction` (
  `id` char(36) NOT NULL,
  `montant` float NOT NULL,
  `devise` varchar(10) DEFAULT NULL,
  `type` enum('ENVOI','RECEPTION','RETRAIT') DEFAULT NULL,
  `date` timestamp NOT NULL DEFAULT current_timestamp(),
  `statut` enum('EN_COURS','SUCCES','ECHEC') DEFAULT NULL,
  `message` varchar(750) DEFAULT NULL,
  `methode_paiement` enum('QR_CODE','NUMERO_TELEPHONE') DEFAULT NULL,
  `expediteur_id` char(36) DEFAULT NULL,
  `destinataire_id` char(36) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `utilisateur`
--

CREATE TABLE `utilisateur` (
  `id` char(36) NOT NULL,
  `nom` varchar(100) DEFAULT NULL,
  `prenom` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `mot_de_passe` varchar(35) NOT NULL,
  `numero_telephone` varchar(20) DEFAULT NULL,
  `date_naissance` date DEFAULT NULL,
  `adresse` varchar(35) DEFAULT NULL,
  `date_inscription` timestamp NOT NULL DEFAULT current_timestamp(),
  `kyc_status` enum('EN_ATTENTE','VALIDE','REJETE') DEFAULT NULL,
  `type_utilisateur` enum('CLIENT','MARCHAND','ADMIN') DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `utilisateur`
--

INSERT INTO `utilisateur` (`id`, `nom`, `prenom`, `email`, `mot_de_passe`, `numero_telephone`, `date_naissance`, `adresse`, `date_inscription`, `kyc_status`, `type_utilisateur`) VALUES
('243e53d4-5921-11f0-bca2-8c04ba17d320', 'end', 'thelast', 'thelast@gmail.com', 'thelast12345', '655341218', '2005-04-13', 'yaounde', '2025-07-04 21:52:12', 'VALIDE', 'CLIENT');

-- --------------------------------------------------------

--
-- Doublure de structure pour la vue `vue_portefeuilles_alerte`
-- (Voir ci-dessous la vue réelle)
--
CREATE TABLE `vue_portefeuilles_alerte` (
`id` char(36)
,`utilisateur_id` char(36)
,`solde` float
,`devise` varchar(10)
,`date_derniere_mise_a_jour` timestamp
);

-- --------------------------------------------------------

--
-- Doublure de structure pour la vue `vue_transactions_utilisateur`
-- (Voir ci-dessous la vue réelle)
--
CREATE TABLE `vue_transactions_utilisateur` (
`id` char(36)
,`montant` float
,`devise` varchar(10)
,`type` enum('ENVOI','RECEPTION','RETRAIT')
,`date` timestamp
,`statut` enum('EN_COURS','SUCCES','ECHEC')
,`message` varchar(750)
,`methode_paiement` enum('QR_CODE','NUMERO_TELEPHONE')
,`expediteur_id` char(36)
,`destinataire_id` char(36)
,`nom_expediteur` varchar(100)
,`nom_destinataire` varchar(100)
);

-- --------------------------------------------------------

--
-- Structure de la vue `vue_portefeuilles_alerte`
--
DROP TABLE IF EXISTS `vue_portefeuilles_alerte`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `vue_portefeuilles_alerte`  AS SELECT `portefeuille`.`id` AS `id`, `portefeuille`.`utilisateur_id` AS `utilisateur_id`, `portefeuille`.`solde` AS `solde`, `portefeuille`.`devise` AS `devise`, `portefeuille`.`date_derniere_mise_a_jour` AS `date_derniere_mise_a_jour` FROM `portefeuille` WHERE `portefeuille`.`solde` < 5000 ;

-- --------------------------------------------------------

--
-- Structure de la vue `vue_transactions_utilisateur`
--
DROP TABLE IF EXISTS `vue_transactions_utilisateur`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `vue_transactions_utilisateur`  AS SELECT `t`.`id` AS `id`, `t`.`montant` AS `montant`, `t`.`devise` AS `devise`, `t`.`type` AS `type`, `t`.`date` AS `date`, `t`.`statut` AS `statut`, `t`.`message` AS `message`, `t`.`methode_paiement` AS `methode_paiement`, `t`.`expediteur_id` AS `expediteur_id`, `t`.`destinataire_id` AS `destinataire_id`, `u1`.`nom` AS `nom_expediteur`, `u2`.`nom` AS `nom_destinataire` FROM ((`transaction` `t` join `utilisateur` `u1` on(`t`.`expediteur_id` = `u1`.`id`)) join `utilisateur` `u2` on(`t`.`destinataire_id` = `u2`.`id`)) ;

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `administrateur`
--
ALTER TABLE `administrateur`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `client`
--
ALTER TABLE `client`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `qr_code_id` (`qr_code_id`);

--
-- Index pour la table `kyc_document`
--
ALTER TABLE `kyc_document`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `numero_document` (`numero_document`),
  ADD KEY `idx_kyc_utilisateur` (`utilisateur_id`);

--
-- Index pour la table `marchand`
--
ALTER TABLE `marchand`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `qr_paiement_fixe_id` (`qr_paiement_fixe_id`);

--
-- Index pour la table `notification`
--
ALTER TABLE `notification`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_notification_utilisateur` (`utilisateur_id`);

--
-- Index pour la table `portefeuille`
--
ALTER TABLE `portefeuille`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `utilisateur_id` (`utilisateur_id`),
  ADD KEY `idx_portefeuille_utilisateur` (`utilisateur_id`);

--
-- Index pour la table `qrcode`
--
ALTER TABLE `qrcode`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `transaction`
--
ALTER TABLE `transaction`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_transaction_expediteur` (`expediteur_id`),
  ADD KEY `idx_transaction_destinataire` (`destinataire_id`);

--
-- Index pour la table `utilisateur`
--
ALTER TABLE `utilisateur`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD UNIQUE KEY `numero_telephone` (`numero_telephone`),
  ADD KEY `idx_utilisateur_email` (`email`);

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `administrateur`
--
ALTER TABLE `administrateur`
  ADD CONSTRAINT `administrateur_ibfk_1` FOREIGN KEY (`id`) REFERENCES `utilisateur` (`id`) ON DELETE CASCADE;

--
-- Contraintes pour la table `client`
--
ALTER TABLE `client`
  ADD CONSTRAINT `client_ibfk_1` FOREIGN KEY (`id`) REFERENCES `utilisateur` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `client_ibfk_2` FOREIGN KEY (`qr_code_id`) REFERENCES `qrcode` (`id`);

--
-- Contraintes pour la table `kyc_document`
--
ALTER TABLE `kyc_document`
  ADD CONSTRAINT `kyc_document_ibfk_1` FOREIGN KEY (`utilisateur_id`) REFERENCES `utilisateur` (`id`) ON DELETE CASCADE;

--
-- Contraintes pour la table `marchand`
--
ALTER TABLE `marchand`
  ADD CONSTRAINT `marchand_ibfk_1` FOREIGN KEY (`id`) REFERENCES `utilisateur` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `marchand_ibfk_2` FOREIGN KEY (`qr_paiement_fixe_id`) REFERENCES `qrcode` (`id`);

--
-- Contraintes pour la table `notification`
--
ALTER TABLE `notification`
  ADD CONSTRAINT `notification_ibfk_1` FOREIGN KEY (`utilisateur_id`) REFERENCES `utilisateur` (`id`) ON DELETE CASCADE;

--
-- Contraintes pour la table `portefeuille`
--
ALTER TABLE `portefeuille`
  ADD CONSTRAINT `portefeuille_ibfk_1` FOREIGN KEY (`utilisateur_id`) REFERENCES `utilisateur` (`id`) ON DELETE CASCADE;

--
-- Contraintes pour la table `transaction`
--
ALTER TABLE `transaction`
  ADD CONSTRAINT `transaction_ibfk_1` FOREIGN KEY (`expediteur_id`) REFERENCES `utilisateur` (`id`),
  ADD CONSTRAINT `transaction_ibfk_2` FOREIGN KEY (`destinataire_id`) REFERENCES `utilisateur` (`id`);
COMMIT;
