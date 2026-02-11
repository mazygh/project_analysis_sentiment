#!/bin/bash

echo "========================================"
echo " Lanceur d'Application Sentiment Analysis"
echo "========================================"
echo ""

echo "Vérification de l'environnement..."
python3 --version
if [ $? -ne 0 ]; then
    echo "ERREUR: Python n'est pas installé"
    exit 1
fi

echo ""
echo "Installation des dépendances..."
pip3 install -r requirements.txt

echo ""
echo "Lancement de l'application..."
echo "L'application va s'ouvrir dans votre navigateur..."
echo ""

streamlit run sentiment_analysis_app.py
