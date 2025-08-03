#!/usr/bin/env python3
"""
Script para leer archivos del proyecto en Windows
Ejecutar: python read_files.py
"""

import os
from pathlib import Path

def read_file_safe(file_path):
    """Lee un archivo de forma segura"""
    try:
        if Path(file_path).exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            return f"❌ Archivo no encontrado: {file_path}"
    except Exception as e:
        return f"❌ Error leyendo {file_path}: {str(e)}"

def print_separator(title):
    """Imprime separador con título"""
    print("\n" + "="*60)
    print(f"📄 {title}")
    print("="*60)

def main():
    print("🔍 CONTENIDO DE ARCHIVOS - EVALUACIÓN DOCENTE")
    
    # Backend files
    backend_files = [
        ("BACKEND MAIN", "backend/app/main.py"),
        ("CONFIG", "backend/app/core/config.py"), 
        ("DATABASE", "backend/app/core/database.py"),
        ("SECURITY", "backend/app/core/security.py"),
        ("USER MODEL", "backend/app/models/user.py"),
        ("AUTH SCHEMA", "backend/app/schemas/auth.py"),
        ("API ROUTER", "backend/app/api/api_v1/api.py"),
        ("REQUIREMENTS", "backend/requirements.txt")
    ]
    
    # Frontend files
    frontend_files = [
        ("APP JS", "frontend/src/App.js"),
        ("AUTH CONTEXT", "frontend/src/contexts/AuthContext.js"),
        ("API SERVICE", "frontend/src/services/api.js"),
        ("LOGIN PAGE", "frontend/src/pages/Login.js"),
        ("PROTECTED ROUTE", "frontend/src/components/auth/ProtectedRoute.js"),
        ("PACKAGE JSON", "frontend/package.json")
    ]
    
    # Config files
    config_files = [
        ("ENV FILE", ".env"),
        ("SCHEMA SQL", "database/01_create_schema.sql"),
        ("SEEDS SQL", "database/02_insert_seeds.sql")
    ]
    
    # Leer todos los archivos
    all_files = backend_files + frontend_files + config_files
    
    for title, file_path in all_files:
        print_separator(title)
        content = read_file_safe(file_path)
        print(content)
    
    print("\n" + "="*60)
    print("✅ LECTURA COMPLETADA")
    print("="*60)

if __name__ == "__main__":
    main()