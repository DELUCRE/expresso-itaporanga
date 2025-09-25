#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para inicializar o banco de dados do sistema Expresso Itaporanga
"""

import sys
import os
sys.path.append('/home/ubuntu/site_integrado_expresso/src')

from app import app, db, Usuario, Entrega

def inicializar_banco():
    """Inicializa o banco de dados e cria as tabelas"""
    
    with app.app_context():
        print("🚀 Inicializando banco de dados...")
        
        # Criar todas as tabelas
        db.create_all()
        print("✅ Tabelas criadas com sucesso!")
        
        # Verificar se usuário admin já existe
        admin_existente = Usuario.query.filter_by(username='admin').first()
        
        if not admin_existente:
            # Criar usuário admin
            admin = Usuario(username='admin', password_hash='admin123')
            db.session.add(admin)
            db.session.commit()
            print("✅ Usuário admin criado!")
        else:
            print("ℹ️ Usuário admin já existe")
        
        print("🎉 Banco de dados inicializado com sucesso!")

if __name__ == "__main__":
    inicializar_banco()

