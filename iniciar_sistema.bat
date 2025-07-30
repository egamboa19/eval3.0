@echo off
echo Iniciando Sistema de Evaluacion - prepa 25
echo.

echo Verificando dependencias...
cd backend
python -c "import fastapi" 2>nul || (echo Instalando dependencias backend... && pip install -r requirements.txt)

echo Iniciando backend...
start "Backend API" python -m uvicorn app.main:app --host 0.0.0.0 --port 8000

timeout /t 5

echo Verificando frontend...
cd ../frontend
npm list react >nul 2>&1 || (echo Instalando dependencias frontend... && npm install)

echo Iniciando frontend...
start "Frontend" npm start

echo.
echo ====================================
echo Sistema iniciado correctamente:
echo - Backend: http://localhost:8000
echo - Frontend: http://localhost:3000
echo - Docs API: http://localhost:8000/docs
echo.
echo Credenciales de administrador:
echo - Email: admin@prepa25.com.mx
echo - Password: admin123
echo ====================================
echo.
echo Para detener: Cierra las ventanas o presiona Ctrl+C
pause
