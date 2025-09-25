#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para criar entregas de simulação no sistema Expresso Itaporanga
"""

import sys
import os
sys.path.append('/home/ubuntu/site_integrado_expresso/src')

from app import app, db, Entrega
from datetime import datetime, timedelta
import random

# Dados de simulação realistas
entregas_simulacao = [
    {
        'remetente_nome': 'João Silva Santos',
        'remetente_endereco': 'Rua das Flores, 123, Centro',
        'remetente_cidade': 'Recife - PE',
        'destinatario_nome': 'Maria Oliveira Costa',
        'destinatario_endereco': 'Av. Paulista, 1000, Bela Vista',
        'destinatario_cidade': 'São Paulo - SP',
        'tipo_produto': 'Eletrônicos',
        'peso': 2.5,
        'valor_declarado': 850.00,
        'status': 'entregue'
    },
    {
        'remetente_nome': 'Pedro Almeida Lima',
        'remetente_endereco': 'Rua do Comércio, 456, Boa Viagem',
        'remetente_cidade': 'Recife - PE',
        'destinatario_nome': 'Ana Carolina Ferreira',
        'destinatario_endereco': 'Rua Augusta, 2500, Consolação',
        'destinatario_cidade': 'São Paulo - SP',
        'tipo_produto': 'Roupas',
        'peso': 1.2,
        'valor_declarado': 320.00,
        'status': 'em_transito'
    },
    {
        'remetente_nome': 'Carlos Eduardo Rocha',
        'remetente_endereco': 'Av. Boa Viagem, 789, Boa Viagem',
        'remetente_cidade': 'Recife - PE',
        'destinatario_nome': 'Juliana Santos Moreira',
        'destinatario_endereco': 'Rua Oscar Freire, 150, Jardins',
        'destinatario_cidade': 'São Paulo - SP',
        'tipo_produto': 'Documentos',
        'peso': 0.3,
        'valor_declarado': 50.00,
        'status': 'entregue'
    },
    {
        'remetente_nome': 'Fernanda Costa Ribeiro',
        'remetente_endereco': 'Rua da Aurora, 321, Santo Amaro',
        'remetente_cidade': 'Recife - PE',
        'destinatario_nome': 'Roberto Silva Nunes',
        'destinatario_endereco': 'Av. Faria Lima, 3000, Itaim Bibi',
        'destinatario_cidade': 'São Paulo - SP',
        'tipo_produto': 'Medicamentos',
        'peso': 0.8,
        'valor_declarado': 180.00,
        'status': 'entregue'
    },
    {
        'remetente_nome': 'Antonio José Barbosa',
        'remetente_endereco': 'Rua do Sol, 654, Casa Amarela',
        'remetente_cidade': 'Recife - PE',
        'destinatario_nome': 'Camila Rodrigues Lima',
        'destinatario_endereco': 'Rua Haddock Lobo, 800, Cerqueira César',
        'destinatario_cidade': 'São Paulo - SP',
        'tipo_produto': 'Livros',
        'peso': 3.2,
        'valor_declarado': 150.00,
        'status': 'pendente'
    },
    {
        'remetente_nome': 'Luciana Mendes Souza',
        'remetente_endereco': 'Av. Conde da Boa Vista, 987, Boa Vista',
        'remetente_cidade': 'Recife - PE',
        'destinatario_nome': 'Diego Alves Pereira',
        'destinatario_endereco': 'Rua Teodoro Sampaio, 1200, Pinheiros',
        'destinatario_cidade': 'São Paulo - SP',
        'tipo_produto': 'Eletrônicos',
        'peso': 4.1,
        'valor_declarado': 1200.00,
        'status': 'em_transito'
    },
    {
        'remetente_nome': 'Rafael Santos Oliveira',
        'remetente_endereco': 'Rua Imperial, 147, São José',
        'remetente_cidade': 'Recife - PE',
        'destinatario_nome': 'Beatriz Carvalho Silva',
        'destinatario_endereco': 'Av. Rebouças, 2200, Pinheiros',
        'destinatario_cidade': 'São Paulo - SP',
        'tipo_produto': 'Roupas',
        'peso': 2.0,
        'valor_declarado': 450.00,
        'status': 'entregue'
    },
    {
        'remetente_nome': 'Gabriela Lima Torres',
        'remetente_endereco': 'Rua da Harmonia, 258, Casa Forte',
        'remetente_cidade': 'Recife - PE',
        'destinatario_nome': 'Thiago Monteiro Costa',
        'destinatario_endereco': 'Rua da Consolação, 3500, Consolação',
        'destinatario_cidade': 'São Paulo - SP',
        'tipo_produto': 'Outros',
        'peso': 1.5,
        'valor_declarado': 280.00,
        'status': 'entregue'
    },
    {
        'remetente_nome': 'Marcos Vinícius Lopes',
        'remetente_endereco': 'Av. Agamenon Magalhães, 741, Derby',
        'remetente_cidade': 'Recife - PE',
        'destinatario_nome': 'Larissa Fernandes Rocha',
        'destinatario_endereco': 'Rua Bela Cintra, 1800, Consolação',
        'destinatario_cidade': 'São Paulo - SP',
        'tipo_produto': 'Eletrônicos',
        'peso': 0.9,
        'valor_declarado': 650.00,
        'status': 'pendente'
    },
    {
        'remetente_nome': 'Patrícia Alves Martins',
        'remetente_endereco': 'Rua do Futuro, 369, Graças',
        'remetente_cidade': 'Recife - PE',
        'destinatario_nome': 'Leonardo Silva Barbosa',
        'destinatario_endereco': 'Av. Brigadeiro Faria Lima, 4500, Itaim Bibi',
        'destinatario_cidade': 'São Paulo - SP',
        'tipo_produto': 'Medicamentos',
        'peso': 0.6,
        'valor_declarado': 95.00,
        'status': 'devolvida'
    }
]

def criar_entregas_simulacao():
    """Cria entregas de simulação no banco de dados"""
    
    with app.app_context():
        print("🚀 Iniciando criação de entregas de simulação...")
        
        # Limpar entregas existentes (opcional)
        Entrega.query.delete()
        db.session.commit()
        print("✅ Banco de dados limpo")
        
        entregas_criadas = 0
        
        for i, dados in enumerate(entregas_simulacao, 1):
            try:
                # Criar datas realistas
                dias_atras = random.randint(1, 30)
                data_criacao = datetime.now() - timedelta(days=dias_atras)
                
                # Gerar código de rastreamento único
                codigo_rastreamento = f"EI{str(i).zfill(8)}"
                
                # Criar nova entrega
                entrega = Entrega(
                    codigo_rastreamento=codigo_rastreamento,
                    remetente_nome=dados['remetente_nome'],
                    remetente_endereco=dados['remetente_endereco'],
                    remetente_cidade=dados['remetente_cidade'],
                    destinatario_nome=dados['destinatario_nome'],
                    destinatario_endereco=dados['destinatario_endereco'],
                    destinatario_cidade=dados['destinatario_cidade'],
                    tipo_produto=dados['tipo_produto'],
                    peso=dados['peso'],
                    valor_declarado=dados['valor_declarado'],
                    status=dados['status'],
                    data_criacao=data_criacao
                )
                
                db.session.add(entrega)
                entregas_criadas += 1
                
                print(f"📦 Entrega {i}/10 criada: {codigo_rastreamento} - {dados['remetente_nome']} → {dados['destinatario_nome']} ({dados['status']})")
                
            except Exception as e:
                print(f"❌ Erro ao criar entrega {i}: {e}")
        
        # Salvar todas as entregas
        try:
            db.session.commit()
            print(f"\n🎉 {entregas_criadas} entregas de simulação criadas com sucesso!")
            
            # Estatísticas
            total = Entrega.query.count()
            pendentes = Entrega.query.filter_by(status='pendente').count()
            em_transito = Entrega.query.filter_by(status='em_transito').count()
            entregues = Entrega.query.filter_by(status='entregue').count()
            devolvidas = Entrega.query.filter_by(status='devolvida').count()
            
            print(f"\n📊 ESTATÍSTICAS DO SISTEMA:")
            print(f"   📦 Total de Entregas: {total}")
            print(f"   ⏳ Pendentes: {pendentes}")
            print(f"   🚚 Em Trânsito: {em_transito}")
            print(f"   ✅ Entregues: {entregues}")
            print(f"   ↩️ Devolvidas: {devolvidas}")
            
            if total > 0:
                taxa_sucesso = (entregues / total) * 100
                print(f"   🎯 Taxa de Sucesso: {taxa_sucesso:.1f}%")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Erro ao salvar entregas: {e}")

if __name__ == "__main__":
    criar_entregas_simulacao()

