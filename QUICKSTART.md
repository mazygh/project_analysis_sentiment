# 🚀 Guide de Démarrage Rapide

## Installation en 3 étapes

### Étape 1 : Installer Python
Si vous n'avez pas Python, téléchargez-le depuis [python.org](https://www.python.org/downloads/)
- Version requise : Python 3.8 ou supérieur

### Étape 2 : Installer les dépendances
Ouvrez un terminal dans le dossier de l'application et exécutez :

```bash
pip install -r requirements.txt
```

### Étape 3 : Lancer l'application

**Option A - Avec le script automatique :**

Windows :
```bash
run_app.bat
```

Linux/Mac :
```bash
chmod +x run_app.sh
./run_app.sh
```

**Option B - Manuellement :**
```bash
streamlit run sentiment_analysis_app.py
```

## 🎯 Utilisation Rapide

1. **L'application s'ouvre automatiquement** dans votre navigateur
   - Si non, allez sur : http://localhost:8501

2. **Analysez votre premier texte :**
   - Tapez un texte dans la zone de saisie
   - Cliquez sur "Analyser le Sentiment"
   - Consultez les résultats !

3. **Essayez les exemples :**
   - Sélectionnez un exemple dans la barre latérale
   - Observez les différences de sentiment

## 🔧 Résolution de problèmes

### L'application ne démarre pas
```bash
# Vérifier la version de Python
python --version  # ou python3 --version

# Réinstaller les dépendances
pip install --upgrade -r requirements.txt
```

### Erreur de mémoire
- Assurez-vous d'avoir au moins 2 GB de RAM disponible
- Fermez les autres applications

### Le modèle ne charge pas
- Vérifiez votre connexion Internet (pour télécharger le modèle)
- Le premier lancement peut prendre quelques minutes

## 📚 Documentation Complète

Pour plus d'informations, consultez le fichier [README.md](README.md)

## 💡 Conseils

- **Premier lancement** : Peut prendre 2-3 minutes pour télécharger le modèle
- **Performance** : Le modèle est mis en cache après le premier chargement
- **Texte court** : Meilleurs résultats avec 1-3 phrases
- **Langue** : Optimisé pour l'anglais

## 🆘 Besoin d'aide ?

Si vous rencontrez des problèmes :
1. Consultez la section "Troubleshooting" du README
2. Vérifiez les logs dans le terminal
3. Ouvrez une issue sur GitHub
