@echo off
:: Se place dans le dossier où se trouve le fichier .bat
cd /d "%~dp0"

:: Lance Python sur le script situé dans le même dossier
"C:\Program Files\Siril\python\python.exe" "Messier_generator.py"

if %errorlevel% neq 0 (
    echo.
    echo [ERREUR] Le script 'Messier_generator.py' est introuvable dans : %cd%
    echo Verifiez que le nom du fichier est exactement 'Messier_generator.py'
    pause
) else (
    echo Planche mise a jour !
    start planche_messier.html
)