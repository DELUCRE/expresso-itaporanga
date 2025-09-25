#!/usr/bin/env python3
"""
Análise Avançada de Dados - Expresso Itaporanga
Sistema de análise de dados para insights operacionais e estratégicos
"""

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import json
import os

# Configuração de estilo para gráficos
plt.style.use('default')
plt.rcParams['figure.figsize'] = (10, 6)

class AnalisadorEntregas:
    def __init__(self, db_path):
        self.db_path = db_path
        self.df_entregas = None
        self.carregar_dados()
    
    def carregar_dados(self):
        """Carrega dados do banco SQLite para DataFrame pandas"""
        try:
            conn = sqlite3.connect(self.db_path)
            query = """
            SELECT 
                id,
                codigo_rastreamento,
                remetente_nome,
                remetente_cidade,
                destinatario_nome,
                destinatario_cidade,
                tipo_produto,
                peso,
                valor_declarado,
                status,
                data_criacao,
                data_atualizacao
            FROM entrega
            ORDER BY data_criacao DESC
            """
            
            self.df_entregas = pd.read_sql_query(query, conn)
            
            # Converter datas
            self.df_entregas['data_criacao'] = pd.to_datetime(self.df_entregas['data_criacao'])
            self.df_entregas['data_atualizacao'] = pd.to_datetime(self.df_entregas['data_atualizacao'])
            
            # Calcular tempo de processamento
            self.df_entregas['tempo_processamento'] = (
                self.df_entregas['data_atualizacao'] - self.df_entregas['data_criacao']
            ).dt.total_seconds() / 3600  # em horas
            
            conn.close()
            print(f"✅ Dados carregados: {len(self.df_entregas)} entregas")
            
        except Exception as e:
            print(f"❌ Erro ao carregar dados: {e}")
    
    def analise_distribuicao_status(self):
        """Análise da distribuição de status das entregas"""
        print("\n📊 ANÁLISE DE DISTRIBUIÇÃO DE STATUS")
        print("=" * 50)
        
        status_counts = self.df_entregas['status'].value_counts()
        status_percentual = (status_counts / len(self.df_entregas) * 100).round(2)
        
        for status, count in status_counts.items():
            percentual = status_percentual[status]
            print(f"{status.upper():<15}: {count:>3} entregas ({percentual:>5.1f}%)")
        
        return status_counts
    
    def analise_produtos(self):
        """Análise dos tipos de produtos mais transportados"""
        print("\n📦 ANÁLISE DE PRODUTOS TRANSPORTADOS")
        print("=" * 50)
        
        produtos_counts = self.df_entregas['tipo_produto'].value_counts()
        produtos_percentual = (produtos_counts / len(self.df_entregas) * 100).round(2)
        
        for produto, count in produtos_counts.items():
            percentual = produtos_percentual[produto]
            print(f"{produto.upper():<15}: {count:>3} entregas ({percentual:>5.1f}%)")
        
        return produtos_counts
    
    def analise_rotas(self):
        """Análise das rotas mais utilizadas"""
        print("\n🗺️  ANÁLISE DE ROTAS")
        print("=" * 50)
        
        # Criar coluna de rota
        self.df_entregas['rota'] = (
            self.df_entregas['remetente_cidade'] + ' → ' + 
            self.df_entregas['destinatario_cidade']
        )
        
        rotas_counts = self.df_entregas['rota'].value_counts()
        
        for rota, count in rotas_counts.head(5).items():
            percentual = (count / len(self.df_entregas) * 100)
            print(f"{rota:<30}: {count:>3} entregas ({percentual:>5.1f}%)")
        
        return rotas_counts
    
    def analise_temporal(self):
        """Análise temporal das entregas"""
        print("\n📅 ANÁLISE TEMPORAL")
        print("=" * 50)
        
        # Entregas por dia da semana
        self.df_entregas['dia_semana'] = self.df_entregas['data_criacao'].dt.day_name()
        dias_counts = self.df_entregas['dia_semana'].value_counts()
        
        print("Entregas por dia da semana:")
        for dia, count in dias_counts.items():
            print(f"{dia:<10}: {count:>3} entregas")
        
        # Entregas por mês
        self.df_entregas['mes'] = self.df_entregas['data_criacao'].dt.strftime('%Y-%m')
        meses_counts = self.df_entregas['mes'].value_counts().sort_index()
        
        print("\nEntregas por mês:")
        for mes, count in meses_counts.items():
            print(f"{mes}: {count:>3} entregas")
        
        return dias_counts, meses_counts
    
    def analise_performance(self):
        """Análise de performance operacional"""
        print("\n⚡ ANÁLISE DE PERFORMANCE")
        print("=" * 50)
        
        # Tempo médio de processamento por status
        tempo_por_status = self.df_entregas.groupby('status')['tempo_processamento'].agg([
            'mean', 'median', 'std', 'min', 'max'
        ]).round(2)
        
        print("Tempo de processamento por status (em horas):")
        print(tempo_por_status)
        
        # Estatísticas gerais
        total_entregas = len(self.df_entregas)
        entregues = len(self.df_entregas[self.df_entregas['status'] == 'entregue'])
        taxa_sucesso = (entregues / total_entregas * 100)
        
        print(f"\n📈 INDICADORES GERAIS:")
        print(f"Total de entregas: {total_entregas}")
        print(f"Entregas concluídas: {entregues}")
        print(f"Taxa de sucesso: {taxa_sucesso:.1f}%")
        print(f"Tempo médio de processamento: {self.df_entregas['tempo_processamento'].mean():.1f}h")
        
        return tempo_por_status
    
    def analise_valor_peso(self):
        """Análise de valor declarado e peso das entregas"""
        print("\n💰 ANÁLISE DE VALOR E PESO")
        print("=" * 50)
        
        # Remover valores nulos
        df_clean = self.df_entregas.dropna(subset=['valor_declarado', 'peso'])
        
        if len(df_clean) > 0:
            print(f"Valor declarado médio: R$ {df_clean['valor_declarado'].mean():.2f}")
            print(f"Valor declarado total: R$ {df_clean['valor_declarado'].sum():.2f}")
            print(f"Peso médio: {df_clean['peso'].mean():.2f} kg")
            print(f"Peso total: {df_clean['peso'].sum():.2f} kg")
            
            # Análise por tipo de produto
            valor_por_produto = df_clean.groupby('tipo_produto')['valor_declarado'].agg([
                'mean', 'sum', 'count'
            ]).round(2)
            
            print("\nValor por tipo de produto:")
            print(valor_por_produto)
        else:
            print("Dados de valor e peso não disponíveis")
    
    def gerar_relatorio_completo(self):
        """Gera relatório completo de análise"""
        print("\n" + "="*60)
        print("🚚 RELATÓRIO COMPLETO DE ANÁLISE - EXPRESSO ITAPORANGA")
        print("="*60)
        print(f"Data da análise: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"Período analisado: {self.df_entregas['data_criacao'].min().strftime('%d/%m/%Y')} a {self.df_entregas['data_criacao'].max().strftime('%d/%m/%Y')}")
        
        # Executar todas as análises
        status_dist = self.analise_distribuicao_status()
        produtos_dist = self.analise_produtos()
        rotas_dist = self.analise_rotas()
        dias_counts, meses_counts = self.analise_temporal()
        performance = self.analise_performance()
        self.analise_valor_peso()
        
        # Salvar resultados em JSON
        resultados = {
            'data_analise': datetime.now().isoformat(),
            'total_entregas': len(self.df_entregas),
            'distribuicao_status': status_dist.to_dict(),
            'distribuicao_produtos': produtos_dist.to_dict(),
            'rotas_principais': rotas_dist.head(5).to_dict(),
            'entregas_por_dia_semana': dias_counts.to_dict(),
            'entregas_por_mes': meses_counts.to_dict(),
            'indicadores': {
                'taxa_sucesso': (len(self.df_entregas[self.df_entregas['status'] == 'entregue']) / len(self.df_entregas) * 100),
                'tempo_medio_processamento': float(self.df_entregas['tempo_processamento'].mean()),
                'total_valor_declarado': float(self.df_entregas['valor_declarado'].sum()) if not self.df_entregas['valor_declarado'].isna().all() else 0,
                'peso_total': float(self.df_entregas['peso'].sum()) if not self.df_entregas['peso'].isna().all() else 0
            }
        }
        
        # Salvar em arquivo JSON
        with open('/home/ubuntu/relatorio_analise_completa.json', 'w', encoding='utf-8') as f:
            json.dump(resultados, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Relatório salvo em: /home/ubuntu/relatorio_analise_completa.json")
        
        return resultados

def main():
    """Função principal"""
    db_path = '/home/ubuntu/site_integrado_expresso/src/instance/expresso_itaporanga.db'
    
    if not os.path.exists(db_path):
        print(f"❌ Banco de dados não encontrado: {db_path}")
        return
    
    # Criar analisador
    analisador = AnalisadorEntregas(db_path)
    
    # Gerar relatório completo
    resultados = analisador.gerar_relatorio_completo()
    
    print("\n🎯 ANÁLISE CONCLUÍDA COM SUCESSO!")
    print("Todos os dados foram processados e o relatório foi gerado.")

if __name__ == "__main__":
    main()

