@echo off
echo Master Duel Frame Replacer - Build Script
echo ===================================

echo.
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Building executable...
pyinstaller --onefile --windowed --add-data ".venv\Lib\site-packages\UnityPy;UnityPy/" --name "MD Frame Replacer" --icon "./assets/icon.ico" --add-data "./assets;assets" asset_replacer.py

if exist "dist\MD Frame Replacer.exe" (
    echo.
    echo Build successful!
    echo Executable created: dist\UnityAssetReplacer.exe
    
    echo @echo off > run.bat
    echo "dist\MD Frame Replacer.exe" >> run.bat
    echo pause >> run.bat
    
    echo.
    echo You can now run dist\MD Frame Replacer.exe
    echo Or use run.bat for easy execution
) else (
    echo.
    echo Build failed! Check the output above for errors.
)

echo.
pause