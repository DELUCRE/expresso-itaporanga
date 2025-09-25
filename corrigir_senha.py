#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para corrigir a senha do usuário admin
"""

import sys
import os
sys.path.append('/home/ubuntu/site_integrado_expresso/src')

from app import app, db, Usuario
from werkzeug.security import generate_password_hash

def corrigir_senha_admin():
    """Corrige a senha do usuário admin para usar hash"""
    
    with app.app_context():
        print("🔧 Corrigindo senha do usuário admin...")
        
        # Buscar usuário admin
        admin = Usuario.query.filter_by(username='admin').first()
        
        if admin:
            # Gerar hash da senha
            senha_hash = generate_password_hash('admin123')
            
            # Atualizar senha
            admin.password_hash = senha_hash
            db.session.commit()
            
            print("✅ Senha do admin corrigida com hash!")
            print(f"   Username: {admin.username}")
            print(f"   Hash: {admin.password_hash[:20]}...")
        else:
            print("❌ Usuário admin não encontrado")

if __name__ == "__main__":
    corrigir_senha_admin()

