#!/usr/bin/env python3
"""
Script simple para generar hash de contraseña
Guarda como: generate_hash.py
Ejecuta: python generate_hash.py
"""

from passlib.context import CryptContext

# Configurar bcrypt
ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Generar hash para admin123
password = "admin123"
nuevo_hash = ctx.hash(password)

print("🔐 HASH GENERADO PARA CONTRASEÑA: admin123")
print("="*60)
print(f"Hash: {nuevo_hash}")
print()
print("📋 SQL PARA ACTUALIZAR EN PGADMIN:")
print("="*60)
print(f"UPDATE users SET hashed_password = '{nuevo_hash}' WHERE email = 'admin@prepa25.com.mx';")
print()
print("✅ Copia y pega el UPDATE exactamente como aparece arriba")
print("💡 Después prueba login con: admin@prepa25.com.mx / admin123")