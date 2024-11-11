@echo off
if not exist "save" mkdir "save"

:: Activer l'environnement virtuel (si nécessaire)
call venv/Scripts/Activate

:: Lancer le jeu en mode fenêtré caché
start "" pythonw main.py

:: Fermer cette fenêtre de commande
exit