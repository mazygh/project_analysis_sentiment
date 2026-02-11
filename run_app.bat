@echo off
echo ========================================
echo  Lanceur d'Application Sentiment Analysis
echo ========================================
echo.

echo Verification de l'environnement...
python --version
if errorlevel 1 (
    echo ERREUR: Python n'est pas installe ou n'est pas dans le PATH
    pause
    exit /b 1
)

echo.
echo Installation des dependances...
pip install -r requirements.txt

echo.
echo Lancement de l'application...
echo L'application va s'ouvrir dans votre navigateur...
echo.

streamlit run sentiment_analysis_app.py

pause
