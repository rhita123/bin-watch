#  BinWatch – Suivi intelligent des poubelles publiques

BinWatch est une plateforme web développée dans le cadre du Master Camp Data 2025 à l’Efrei.  
Son objectif est de prévenir les dépôts sauvages en détectant automatiquement l’état des poubelles(pleines ou vides) à partir d’images envoyées par les citoyens.
---

##  Contexte

La prolifération des déchets abandonnés dans l’espace public est en grande partie due à un manque de surveillance en temps réel.  
Les poubelles pleines ou débordantes deviennent souvent les points de départ de dépôts sauvages.

BinWatch propose une solution simple, efficace et à faible coût pour :
- Suivre l'état des poubelles à distance,
- Anticiper les risques de débordement,
- Améliorer la planification des tournées de ramassage.

---

##  Objectifs

- Permettre l’upload et l’annotation d’images de poubelles.
- Extraire automatiquement des caractéristiques visuelles (taille, couleur, contraste…).
- Simuler une classification (pleine/vide) via des règles conditionnelles.
- Visualiser dynamiquement les données via dashboard,cartes,graphiques.
-  Assurer une version multilingue (FR / EN) de la plateforme.

---

##  Fonctionnalités

### Upload & Annotation
- Formulaire de téléversement (PNG, JPG)
- Annotation manuelle : `pleine` / `vide`
- Sauvegarde de métadonnées (dimensions, taille, couleur, contraste…)

### Classification conditionnelle
- Règles simples appliquées automatiquement à l’upload (ex: couleur < 100 ⇒ pleine)

### Visualisation
- Dashboard interactif avec :
  - Total d’images
  - Pourcentage pleines / vides
  - Courbes temporelles
  - Filtres dynamiques
- Carte Leaflet des emplacements (avec markers)
- Graphiques avec Chart.js

### Multilingue
- Sélecteur de langue FR / EN avec Flask-Babel
- Interface automatiquement traduite

---

##  Technologies utilisées

| Côté | Technologies |
|------|--------------|
| Backend | Python, Flask, SQLite |
| Traitement images | Pillow, os, OpenCV |
| Frontend | HTML, CSS, Bootstrap, Chart.js, Leaflet |
| Visualisation | Matplotlib, Chart.js |
| Multilingue | Flask-Babel |
| Stockage | Dossiers images + base SQLite |

---

##  Lancer le projet en local

### 1. Cloner le dépôt

```bash
git clone <url_du_repo>
cd BinWatch
```

### 2. Créer un environnement virtuel 

```bash
python -m venv venv
source venv/bin/activate  # Sur Windows : venv\Scripts\activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Compiler les fichiers de traduction

```bash
pybabel compile -d translations
```

### 5. Lancer le serveur Flask

```bash
flask run
```

Puis ouvre [http://localhost:5000](http://localhost:5000) dans le navigateur 