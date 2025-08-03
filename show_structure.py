#!/usr/bin/env python3
"""
Script simple para mostrar estructura del proyecto
Ejecutar: python show_structure.py
"""

import os
from pathlib import Path

def show_tree(directory, prefix="", max_depth=4, current_depth=0):
    """Muestra estructura de directorios como árbol"""
    if current_depth > max_depth:
        return
    
    # Archivos/carpetas a ignorar
    ignore = {
        'node_modules', '__pycache__', '.git', 'dist', 'build', 
        '.pytest_cache', '.vscode', '.idea', 'venv', 'env'
    }
    
    items = []
    try:
        for item in sorted(Path(directory).iterdir()):
            if item.name not in ignore and not item.name.startswith('.'):
                items.append(item)
    except PermissionError:
        return
    
    for i, item in enumerate(items):
        is_last = i == len(items) - 1
        current_prefix = "└── " if is_last else "├── "
        print(f"{prefix}{current_prefix}{item.name}")
        
        if item.is_dir():
            next_prefix = prefix + ("    " if is_last else "│   ")
            show_tree(item, next_prefix, max_depth, current_depth + 1)

def show_key_files():
    """Muestra archivos clave del proyecto"""
    key_files = [
        # Backend
        "backend/main.py",
        "backend/app/main.py", 
        "backend/app/auth/router.py",
        "backend/app/auth/models.py",
        "backend/app/database.py",
        "backend/requirements.txt",
        
        # Frontend  
        "frontend/src/App.jsx",
        "frontend/src/main.jsx",
        "frontend/src/components/auth/Login.jsx",
        "frontend/src/contexts/AuthContext.jsx",
        "frontend/package.json",
        
        # Config
        "docker-compose.yml",
        ".env",
        ".env.example"
    ]
    
    print("\n" + "="*60)
    print("📋 ARCHIVOS CLAVE - ESTADO")
    print("="*60)
    
    for file_path in key_files:
        exists = Path(file_path).exists()
        status = "✅" if exists else "❌"
        print(f"{status} {file_path}")

def generate_content_commands():
    """Genera comandos para mostrar contenido de archivos"""
    print("\n" + "="*60)
    print("📄 COMANDOS PARA VER CONTENIDO")
    print("="*60)
    
    # Solo archivos que existen
    existing_files = []
    files_to_check = [
        "backend/main.py",
        "backend/app/main.py",
        "backend/app/auth/router.py", 
        "frontend/src/App.jsx",
        "frontend/src/components/auth/Login.jsx",
        "docker-compose.yml"
    ]
    
    for file_path in files_to_check:
        if Path(file_path).exists():
            existing_files.append(file_path)
    
    print("\n# Copia y pega estos comandos:")
    for file_path in existing_files:
        safe_name = file_path.replace("/", "_").replace(".", "_").upper()
        print(f"echo '=== {safe_name} ===' && cat '{file_path}'")

def main():
    print("🔍 ESTRUCTURA DEL PROYECTO - EVALUACIÓN DOCENTE")
    print("="*60)
    print(f"📁 Directorio: {Path.cwd()}")
    print("="*60)
    
    # Mostrar árbol de archivos
    show_tree(Path.cwd())
    
    # Mostrar estado de archivos clave
    show_key_files()
    
    # Generar comandos para ver contenido
    generate_content_commands()
    
    print("\n" + "="*60)
    print("✅ ESTRUCTURA GENERADA")
    print("Comparte esta salida y los archivos que indique")
    print("="*60)

if __name__ == "__main__":
    main()