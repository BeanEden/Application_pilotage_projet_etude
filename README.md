---
title: Gestion de Projet Vocalis
emoji: 🚀
colorFrom: blue
colorTo: indigo
sdk: docker
pinned: false
app_port: 7860
---

# 🚀 Dashboard de Gestion de Projet - Vocalis

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-lightgrey.svg)
![Docker](https://img.shields.io/badge/Docker-Supported-blue.svg)

**Vocalis** est une application complète et interactive conçue pour le pilotage, la création de notes de cadrage et la définition d'architecture dans le cadre de la gestion de projets techniques. 

Cette plateforme centralise tous les outils nécessaires aux chefs de projets, architectes et équipes techniques pour suivre l'avancement, maîtriser le budget et assurer la rentabilité.

---

## ✨ Fonctionnalités Principales

L'application offre un éventail complet de modules couvrant tout le cycle de vie d'un projet :

- 🎯 **Cadrage & Objectifs** : Définition du contexte, du périmètre et des livrables.
- 👥 **Parties Prenantes & RACI** : Gestion de l'équipe, des rôles et des responsabilités.
- 🏗️ **Architecture & Modélisation** : Visualisation de l'architecture technique et modélisation des données.
- 📋 **Backlog & User Stories** : Suivi des Epics, des User Stories et gestion détaillée du backlog.
- 📅 **Planning & Kanban** : Suivi d'avancement via diagramme de Gantt interactif et tableau Kanban.
- ⚠️ **Risques & Événements** : Identification des risques, hypothèses et journal de bord du projet.
- 💰 **Budget & Rentabilité** : Suivi précis des coûts (RH, infrastructures, licences, coûts satellites), calcul du ROI (Retour sur Investissement) et devis.
- 📤 **Centre d'Exportation** : Génération de rapports pour l'ensemble des modules.

---

## 🛠️ Stack Technique

- **Backend** : [Python](https://www.python.org/) avec le framework [Flask](https://flask.palletsprojects.com/).
- **Frontend** : HTML5, CSS3, JavaScript (templates rendus côté serveur).
- **Stockage de Données** : Base de données locale basée sur des fichiers JSON (`/data/`) pour une portabilité maximale et simplifier les déploiements.
- **Déploiement** : Conteneurisation via Docker, optimisée pour les plateformes comme [Hugging Face Spaces](https://huggingface.co/spaces). Serveur de production via Gunicorn.

---

## 📂 Structure du Projet

```text
├── app/                  # Code source principal (Blueprint, templates, static)
│   ├── routes.py         # Définition des routes de l'API et de l'interface
│   ├── templates/        # Vues HTML de l'application
│   └── static/           # Ressources statiques (CSS, JS, uploads)
├── data/                 # Stockage des données au format JSON
├── Dockerfile            # Configuration pour la conteneurisation
├── requirements.txt      # Dépendances Python
├── app.py                # Point d'entrée de l'application
└── README.md             # Documentation du projet
```

---

## 🚀 Installation et Lancement en Local

Pour exécuter ce projet localement sur votre machine :

### 1. Cloner le dépôt et accéder au dossier
```bash
git clone <votre-url-de-depot>
cd "Pilotage projet d'études"
```

### 2. Créer et activer un environnement virtuel
```bash
python -m venv venv
# Sous Windows :
venv\Scripts\activate
# Sous macOS/Linux :
source venv/bin/activate
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Démarrer l'application
```bash
python app.py
```
L'application sera accessible sur `http://localhost:7860`.

---

## 🐳 Déploiement via Docker

Pour lancer l'application de manière isolée avec Docker :

```bash
docker build -t vocalis-pm .
docker run -p 7860:7860 vocalis-pm
```

*(Note : Le projet est pré-configuré pour un déploiement instantané sur Hugging Face Spaces)*

---

## ⚖️ Propriété Intellectuelle

Cette application et son code source sont la propriété exclusive de **Jean-Corentin LOIRAT**.  
Ils ne sont **pas libres de droit**. Toute utilisation, reproduction, modification, distribution ou copie, totale ou partielle, est strictement interdite sans l'autorisation explicite de l'auteur.
