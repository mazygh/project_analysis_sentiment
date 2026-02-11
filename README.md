# 🎭 Application d'Analyse de Sentiment avec DistilBERT

Une interface web interactive et moderne pour l'analyse de sentiment en temps réel utilisant DistilBERT et Streamlit.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.29.0-red.svg)
![Transformers](https://img.shields.io/badge/Transformers-4.35.2-orange.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 📋 Table des Matières

- [Fonctionnalités](#fonctionnalités)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Architecture](#architecture)
- [Captures d'écran](#captures-décran)
- [Modèle](#modèle)
- [Développement](#développement)
- [Contribution](#contribution)
- [License](#license)

## ✨ Fonctionnalités

### 🎯 Analyse de Sentiment
- **Prédiction en temps réel** : Analyse instantanée du sentiment (positif/négatif)
- **Scores de confiance** : Visualisation du niveau de confiance du modèle
- **Probabilités détaillées** : Distribution des probabilités pour chaque classe

### 📊 Visualisations Interactives
- **Jauge de confiance** : Graphique en jauge pour le niveau de confiance
- **Graphique en barres** : Comparaison des probabilités positif/négatif
- **Statistiques en temps réel** : Suivi de l'historique des analyses

### 🎨 Interface Utilisateur
- **Design moderne et responsive** : Interface élégante avec CSS personnalisé
- **Mode exemples** : Textes pré-définis pour tester rapidement
- **Historique des analyses** : Conservation des 5 dernières analyses
- **Sidebar informative** : Informations sur le modèle et statistiques

### 🔧 Fonctionnalités Techniques
- **Mise en cache du modèle** : Chargement optimisé avec `@st.cache_resource`
- **Gestion d'erreurs** : Messages d'erreur clairs et informatifs
- **Support multi-modèles** : Possibilité d'utiliser différents modèles

## 🚀 Installation

### Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de packages Python)
- 2 GB de RAM minimum (pour le modèle)

### Étapes d'installation

1. **Cloner le repository (ou télécharger les fichiers)**

```bash
git clone <votre-repo>
cd sentiment-analysis-app
```

2. **Créer un environnement virtuel (recommandé)**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. **Installer les dépendances**

```bash
pip install -r requirements.txt
```

## 💻 Utilisation

### Lancement de l'application

```bash
streamlit run sentiment_analysis_app.py
```

L'application s'ouvrira automatiquement dans votre navigateur à l'adresse `http://localhost:8501`

### Utilisation de l'interface

1. **Entrer le texte à analyser**
   - Tapez ou collez votre texte dans la zone de saisie
   - Ou sélectionnez un exemple pré-défini

2. **Cliquer sur "Analyser le Sentiment"**
   - Le modèle analyse le texte
   - Les résultats s'affichent avec visualisations

3. **Interpréter les résultats**
   - **Sentiment** : Positif ou Négatif
   - **Confiance** : Pourcentage de confiance du modèle
   - **Probabilités** : Distribution détaillée

### Exemples d'utilisation

#### Exemple 1 : Texte positif
```
Input: "I love this product! It's absolutely amazing."
Output: Sentiment POSITIF (97.9% confiance)
```

#### Exemple 2 : Texte négatif
```
Input: "This is terrible. I hate it completely."
Output: Sentiment NÉGATIF (98.0% confiance)
```

## 🏗️ Architecture

### Structure du projet

```
sentiment-analysis-app/
│
├── sentiment_analysis_app.py    # Application Streamlit principale
├── requirements.txt              # Dépendances Python
├── README.md                     # Documentation
│
└── sentiment-distilbert/         # Modèle (optionnel, si local)
    ├── config.json
    ├── pytorch_model.bin
    └── tokenizer files
```

### Composants principaux

#### 1. Chargement du Modèle
```python
@st.cache_resource
def load_model(model_name):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    return tokenizer, model
```

#### 2. Prédiction
```python
def get_prediction(text, tokenizer, model):
    input_ids = tokenizer.encode(text, return_tensors='pt')
    output = model(input_ids)
    probs = torch.nn.functional.softmax(output.logits, dim=-1)
    # ... traitement des résultats
```

#### 3. Visualisations
- **Jauge de confiance** : Plotly Gauge Chart
- **Graphique en barres** : Plotly Bar Chart

## 📊 Modèle

### DistilBERT

**DistilBERT** est une version compressée de BERT (Bidirectional Encoder Representations from Transformers).

#### Caractéristiques :
- **Taille** : 66M paramètres (vs 110M pour BERT-base)
- **Vitesse** : 60% plus rapide que BERT
- **Performance** : Conserve 97% des capacités de BERT
- **Mémoire** : Utilise 40% moins de mémoire

#### Performance du modèle :
- **Précision** : ~90.6%
- **F1-Score** : ~90.6%
- **Classes** : Positif / Négatif

#### Modèle pré-entraîné utilisé :
```
distilbert-base-uncased-finetuned-sst-2-english
```

Ce modèle est fine-tuné sur le dataset SST-2 (Stanford Sentiment Treebank).

## 🛠️ Développement

### Personnalisation

#### Modifier les couleurs
Dans le fichier `sentiment_analysis_app.py`, section CSS :
```python
st.markdown("""
    <style>
    .sentiment-positive {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        # Changez ces valeurs pour personnaliser
    }
    </style>
""", unsafe_allow_html=True)
```

#### Utiliser un modèle personnalisé

1. **Entraîner votre modèle** (voir notebook d'origine)
2. **Sauvegarder le modèle**
```python
trainer.save_model("mon-modele-custom")
```
3. **Utiliser dans l'application**
```python
model_name = "mon-modele-custom"
```

### Déploiement

#### Streamlit Cloud (Gratuit)

1. Créer un compte sur [Streamlit Cloud](https://streamlit.io/cloud)
2. Connecter votre repository GitHub
3. Sélectionner le fichier principal : `sentiment_analysis_app.py`
4. Déployer !

#### Autres options :
- **Heroku** : Nécessite un `Procfile`
- **AWS EC2** : Instance avec Python
- **Docker** : Créer un Dockerfile

### Extensions possibles

- 🌍 **Multi-langues** : Ajouter support pour d'autres langues
- 📊 **Analyse batch** : Analyser plusieurs textes à la fois
- 💾 **Export des résultats** : Télécharger l'historique en CSV
- 🎨 **Visualisations avancées** : Word clouds, analyse temporelle
- 🔗 **API REST** : Créer une API pour intégration externe
- 🎯 **Multi-classes** : Support pour plus de 2 sentiments (neutre, etc.)

## 📝 Notes techniques

### Optimisations

- **Mise en cache** : Le modèle est chargé une seule fois
- **Truncation** : Textes limités à 512 tokens
- **Batch processing** : Possibilité d'ajouter traitement par lots

### Limites

- **Langue** : Optimisé pour l'anglais (SST-2 dataset)
- **Longueur** : Maximum 512 tokens (environ 300-400 mots)
- **Contexte** : Sentiment général, pas d'analyse d'aspects spécifiques
- **Sarcasme** : Peut avoir des difficultés avec le sarcasme/ironie

## 🤝 Contribution

Les contributions sont les bienvenues ! Pour contribuer :

1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit vos changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📄 License

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 👥 Auteurs

- **Votre Nom** - Développement initial

## 🙏 Remerciements

- [Hugging Face](https://huggingface.co/) pour les modèles Transformers
- [Streamlit](https://streamlit.io/) pour le framework web
- [Plotly](https://plotly.com/) pour les visualisations
- La communauté open-source

## 📧 Contact

Pour toute question ou suggestion :
- Email : votre.email@example.com
- GitHub : [@votre-username](https://github.com/votre-username)

---

**⭐ Si vous trouvez ce projet utile, n'oubliez pas de lui donner une étoile !**
