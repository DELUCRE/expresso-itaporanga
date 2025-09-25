#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Testes automatizados para a aplicação Expresso Itaporanga
"""

import unittest
import json
import sys
import os
from datetime import datetime

# Adicionar o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from app import app, db, Usuario, Entrega
from werkzeug.security import generate_password_hash

class ExpressoItaporangaTestCase(unittest.TestCase):
    """Classe base para testes da aplicação"""
    
    def setUp(self):
        """Configurar ambiente de teste"""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['WTF_CSRF_ENABLED'] = False
        
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        
        # Criar tabelas
        db.create_all()
        
        # Criar usuário de teste
        self.criar_usuario_teste()
        
        # Criar entrega de teste
        self.criar_entrega_teste()
    
    def tearDown(self):
        """Limpar ambiente de teste"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def criar_usuario_teste(self):
        """Criar usuário para testes"""
        usuario_teste = Usuario(
            username='teste',
            password_hash=generate_password_hash('senha123'),
            perfil='admin',
            ativo=True
        )
        db.session.add(usuario_teste)
        db.session.commit()
        return usuario_teste
    
    def criar_entrega_teste(self):
        """Criar entrega para testes"""
        entrega_teste = Entrega(
            codigo_rastreamento='EI1234567890',
            remetente_nome='João Silva',
            remetente_endereco='Rua A, 123',
            remetente_cidade='São Paulo/SP',
            destinatario_nome='Maria Santos',
            destinatario_endereco='Rua B, 456',
            destinatario_cidade='Itaporanga/PB',
            tipo_produto='Documentos',
            peso=0.5,
            valor_declarado=100.00,
            status='pendente'
        )
        db.session.add(entrega_teste)
        db.session.commit()
        return entrega_teste

class TestRotasInstitucionais(ExpressoItaporangaTestCase):
    """Testes para as rotas do site institucional"""
    
    def test_pagina_inicial(self):
        """Testar se a página inicial carrega corretamente"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Expresso Itaporanga', response.data)
        self.assertIn(b'Nossa Equipe', response.data)
    
    def test_pagina_sobre(self):
        """Testar se a página sobre carrega corretamente"""
        response = self.app.get('/sobre')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sobre a Expresso Itaporanga', response.data)
        self.assertIn(b'Nossa Hist\xc3\xb3ria', response.data)
    
    def test_pagina_servicos(self):
        """Testar se a página de serviços carrega corretamente"""
        response = self.app.get('/servicos')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Nossos Servi\xc3\xa7os', response.data)
        self.assertIn(b'Porto Seguro', response.data)
    
    def test_pagina_contato(self):
        """Testar se a página de contato carrega corretamente"""
        response = self.app.get('/contato')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Entre em Contato', response.data)
        self.assertIn(b'comercial@expressoitaporanga.com.br', response.data)

class TestAPIEntregas(ExpressoItaporangaTestCase):
    """Testes para a API de entregas"""
    
    def test_listar_entregas(self):
        """Testar listagem de entregas via API"""
        response = self.app.get('/api/entregas')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIsInstance(data['data'], list)
        self.assertGreater(data['total'], 0)
    
    def test_buscar_entrega_por_codigo(self):
        """Testar busca de entrega por código de rastreamento"""
        response = self.app.get('/api/entregas/EI1234567890')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['data']['codigo_rastreamento'], 'EI1234567890')
        self.assertEqual(data['data']['remetente_nome'], 'João Silva')
    
    def test_buscar_entrega_inexistente(self):
        """Testar busca de entrega que não existe"""
        response = self.app.get('/api/entregas/INEXISTENTE')
        self.assertEqual(response.status_code, 404)
        
        data = json.loads(response.data)
        self.assertFalse(data['success'])
        self.assertIn('não encontrada', data['error'])
    
    def test_criar_entrega(self):
        """Testar criação de nova entrega via API"""
        nova_entrega = {
            'remetente_nome': 'Pedro Costa',
            'remetente_endereco': 'Rua C, 789',
            'remetente_cidade': 'Recife/PE',
            'destinatario_nome': 'Ana Lima',
            'destinatario_endereco': 'Rua D, 321',
            'destinatario_cidade': 'São Paulo/SP',
            'tipo_produto': 'Eletrônicos',
            'peso': 2.5,
            'valor_declarado': 500.00,
            'observacoes': 'Frágil'
        }
        
        response = self.app.post('/api/entregas',
                                data=json.dumps(nova_entrega),
                                content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('codigo_rastreamento', data['data'])
        self.assertEqual(data['data']['status'], 'pendente')
    
    def test_criar_entrega_dados_incompletos(self):
        """Testar criação de entrega com dados incompletos"""
        entrega_incompleta = {
            'remetente_nome': 'Pedro Costa'
            # Faltam campos obrigatórios
        }
        
        response = self.app.post('/api/entregas',
                                data=json.dumps(entrega_incompleta),
                                content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        
        data = json.loads(response.data)
        self.assertFalse(data['success'])
        self.assertIn('obrigatório', data['error'])
    
    def test_atualizar_status_entrega(self):
        """Testar atualização de status da entrega"""
        novo_status = {'status': 'em_transito'}
        
        response = self.app.put('/api/entregas/EI1234567890/status',
                               data=json.dumps(novo_status),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['data']['status'], 'em_transito')
    
    def test_atualizar_status_invalido(self):
        """Testar atualização com status inválido"""
        status_invalido = {'status': 'status_inexistente'}
        
        response = self.app.put('/api/entregas/EI1234567890/status',
                               data=json.dumps(status_invalido),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        
        data = json.loads(response.data)
        self.assertFalse(data['success'])
        self.assertIn('inválido', data['error'])

class TestAPIEstatisticas(ExpressoItaporangaTestCase):
    """Testes para a API de estatísticas"""
    
    def test_obter_estatisticas(self):
        """Testar obtenção de estatísticas gerais"""
        response = self.app.get('/api/estatisticas')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        
        estatisticas = data['data']
        self.assertIn('total_entregas', estatisticas)
        self.assertIn('entregas_por_status', estatisticas)
        self.assertIn('taxa_sucesso', estatisticas)
        self.assertIn('top_cidades_destino', estatisticas)
        
        # Verificar se os dados fazem sentido
        self.assertGreaterEqual(estatisticas['total_entregas'], 1)
        self.assertIsInstance(estatisticas['taxa_sucesso'], (int, float))

class TestAPIContato(ExpressoItaporangaTestCase):
    """Testes para a API de contato"""
    
    def test_processar_contato_valido(self):
        """Testar processamento de formulário de contato válido"""
        dados_contato = {
            'nome': 'João Silva',
            'email': 'joao@email.com',
            'telefone': '(11) 99999-9999',
            'assunto': 'orcamento',
            'mensagem': 'Gostaria de solicitar um orçamento.'
        }
        
        response = self.app.post('/api/contato',
                                data=json.dumps(dados_contato),
                                content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('sucesso', data['message'])
    
    def test_processar_contato_dados_incompletos(self):
        """Testar processamento de contato com dados incompletos"""
        dados_incompletos = {
            'nome': 'João Silva'
            # Faltam campos obrigatórios
        }
        
        response = self.app.post('/api/contato',
                                data=json.dumps(dados_incompletos),
                                content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        
        data = json.loads(response.data)
        self.assertFalse(data['success'])
        self.assertIn('obrigatório', data['message'])

class TestAPIDocumentacao(ExpressoItaporangaTestCase):
    """Testes para a documentação da API"""
    
    def test_documentacao_api(self):
        """Testar se a documentação da API está disponível"""
        response = self.app.get('/api/docs')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('title', data)
        self.assertIn('version', data)
        self.assertIn('endpoints', data)
        self.assertIn('status_validos', data)
        self.assertIn('exemplo_entrega', data)

class TestValidacoes(ExpressoItaporangaTestCase):
    """Testes para validações de dados"""
    
    def test_codigo_rastreamento_unico(self):
        """Testar se códigos de rastreamento são únicos"""
        # Criar primeira entrega
        entrega1_data = {
            'remetente_nome': 'Teste 1',
            'remetente_endereco': 'Rua 1',
            'remetente_cidade': 'Cidade 1',
            'destinatario_nome': 'Dest 1',
            'destinatario_endereco': 'Rua Dest 1',
            'destinatario_cidade': 'Cidade Dest 1',
            'tipo_produto': 'Produto 1'
        }
        
        response1 = self.app.post('/api/entregas',
                                 data=json.dumps(entrega1_data),
                                 content_type='application/json')
        
        # Criar segunda entrega
        entrega2_data = {
            'remetente_nome': 'Teste 2',
            'remetente_endereco': 'Rua 2',
            'remetente_cidade': 'Cidade 2',
            'destinatario_nome': 'Dest 2',
            'destinatario_endereco': 'Rua Dest 2',
            'destinatario_cidade': 'Cidade Dest 2',
            'tipo_produto': 'Produto 2'
        }
        
        response2 = self.app.post('/api/entregas',
                                 data=json.dumps(entrega2_data),
                                 content_type='application/json')
        
        # Verificar se ambas foram criadas com sucesso
        self.assertEqual(response1.status_code, 201)
        self.assertEqual(response2.status_code, 201)
        
        # Verificar se os códigos são diferentes
        data1 = json.loads(response1.data)
        data2 = json.loads(response2.data)
        
        codigo1 = data1['data']['codigo_rastreamento']
        codigo2 = data2['data']['codigo_rastreamento']
        
        self.assertNotEqual(codigo1, codigo2)
        self.assertTrue(codigo1.startswith('EI'))
        self.assertTrue(codigo2.startswith('EI'))

def run_tests():
    """Executar todos os testes"""
    # Descobrir e executar todos os testes
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    
    # Executar testes com verbosidade
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Retornar código de saída baseado no resultado
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    exit_code = run_tests()
    sys.exit(exit_code)
