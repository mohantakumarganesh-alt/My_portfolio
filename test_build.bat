@echo off
REM Test Django Blog Build Locally
REM This helps verify everything works before Render deployment

echo ================================
echo Django Blog Build Test
echo ================================

cd /d d:\portfolio\projects_code\blog_app

echo.
echo [1/4] Installing requirements...
pip install -r requirements.txt

echo.
echo [2/4] Running migrations...
python manage.py migrate

echo.
echo [3/4] Creating static files...
python manage.py collectstatic --noinput

echo.
echo [4/4] Testing Django setup...
python manage.py check

echo.
echo ================================
echo Build Test Complete!
echo ================================
echo.
echo If no errors above, your app is ready for Render deployment.
echo.
pause
