#!/usr/bin/env python3
"""
Gerador de Gráficos - Análise Expresso Itaporanga
Cria visualizações gráficas dos dados de entregas
"""

import json
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import os

def configurar_matplotlib():
    """Configura matplotlib para melhor aparência"""
    plt.style.use('default')
    plt.rcParams['figure.figsize'] = (12, 8)
    plt.rcParams['font.size'] = 10
    plt.rcParams['axes.titlesize'] = 14
    plt.rcParams['axes.labelsize'] = 12
    plt.rcParams['xtick.labelsize'] = 10
    plt.rcParams['ytick.labelsize'] = 10
    plt.rcParams['legend.fontsize'] = 10

def criar_grafico_status(dados, output_dir):
    """Cria gráfico de distribuição de status"""
    status_data = dados['distribuicao_status']
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Gráfico de pizza
    labels = list(status_data.keys())
    sizes = list(status_data.values())
    colors = ['#28a745', '#ffc107', '#17a2b8', '#dc3545']
    
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
    ax1.set_title('Distribuição de Status das Entregas', fontweight='bold')
    
    # Gráfico de barras
    bars = ax2.bar(labels, sizes, color=colors)
    ax2.set_title('Quantidade por Status', fontweight='bold')
    ax2.set_ylabel('Número de Entregas')
    
    # Adicionar valores nas barras
    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'{int(height)}', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/distribuicao_status.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("✅ Gráfico de status criado: distribuicao_status.png")

def criar_grafico_produtos(dados, output_dir):
    """Cria gráfico de distribuição de produtos"""
    produtos_data = dados['distribuicao_produtos']
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    labels = list(produtos_data.keys())
    sizes = list(produtos_data.values())
    colors = plt.cm.Set3(np.linspace(0, 1, len(labels)))
    
    bars = ax.bar(labels, sizes, color=colors)
    ax.set_title('Distribuição de Produtos Transportados', fontweight='bold', fontsize=16)
    ax.set_ylabel('Número de Entregas', fontsize=12)
    ax.set_xlabel('Tipo de Produto', fontsize=12)
    
    # Adicionar valores nas barras
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                f'{int(height)}', ha='center', va='bottom', fontweight='bold')
    
    # Rotacionar labels do eixo x
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/distribuicao_produtos.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("✅ Gráfico de produtos criado: distribuicao_produtos.png")

def criar_grafico_dias_semana(dados, output_dir):
    """Cria gráfico de entregas por dia da semana"""
    dias_data = dados['entregas_por_dia_semana']
    
    # Ordenar dias da semana
    ordem_dias = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    dias_pt = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
    
    dias_ordenados = []
    valores_ordenados = []
    labels_pt = []
    
    for i, dia in enumerate(ordem_dias):
        if dia in dias_data:
            dias_ordenados.append(dia)
            valores_ordenados.append(dias_data[dia])
            labels_pt.append(dias_pt[i])
        else:
            dias_ordenados.append(dia)
            valores_ordenados.append(0)
            labels_pt.append(dias_pt[i])
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    bars = ax.bar(labels_pt, valores_ordenados, color='#007bff', alpha=0.8)
    ax.set_title('Entregas por Dia da Semana', fontweight='bold', fontsize=16)
    ax.set_ylabel('Número de Entregas', fontsize=12)
    ax.set_xlabel('Dia da Semana', fontsize=12)
    
    # Adicionar valores nas barras
    for bar in bars:
        height = bar.get_height()
        if height > 0:
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                    f'{int(height)}', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/entregas_por_dia_semana.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("✅ Gráfico de dias da semana criado: entregas_por_dia_semana.png")

def criar_dashboard_resumo(dados, output_dir):
    """Cria dashboard com resumo dos principais indicadores"""
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    
    # 1. Status das entregas (pizza)
    status_data = dados['distribuicao_status']
    labels = list(status_data.keys())
    sizes = list(status_data.values())
    colors = ['#28a745', '#ffc107', '#17a2b8', '#dc3545']
    
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
    ax1.set_title('Status das Entregas', fontweight='bold')
    
    # 2. Produtos mais transportados
    produtos_data = dados['distribuicao_produtos']
    prod_labels = list(produtos_data.keys())
    prod_sizes = list(produtos_data.values())
    
    bars2 = ax2.bar(prod_labels, prod_sizes, color='#17a2b8', alpha=0.8)
    ax2.set_title('Produtos Transportados', fontweight='bold')
    ax2.set_ylabel('Quantidade')
    plt.setp(ax2.get_xticklabels(), rotation=45, ha='right')
    
    # 3. Indicadores principais
    indicadores = dados['indicadores']
    ind_labels = ['Taxa de\nSucesso (%)', 'Tempo Médio\n(horas)', 'Valor Total\n(R$)', 'Peso Total\n(kg)']
    ind_values = [
        indicadores['taxa_sucesso'],
        indicadores['tempo_medio_processamento'],
        indicadores['total_valor_declarado'],
        indicadores['peso_total']
    ]
    
    bars3 = ax3.bar(ind_labels, ind_values, color=['#28a745', '#ffc107', '#007bff', '#6f42c1'])
    ax3.set_title('Indicadores Principais', fontweight='bold')
    
    # Adicionar valores nas barras
    for i, (bar, value) in enumerate(zip(bars3, ind_values)):
        height = bar.get_height()
        label = ind_labels[i]
        
        if 'R$' in label:
            text = f'R$ {value:.1f}'
        elif 'kg' in label:
            text = f'{value:.1f} kg'
        elif '%' in label:
            text = f'{value:.1f}%'
        else:
            text = f'{value:.0f}h'
        
        ax3.text(bar.get_x() + bar.get_width()/2., height + max(ind_values)*0.01,
                text, ha='center', va='bottom', fontweight='bold')
    
    # 4. Entregas por dia da semana
    dias_data = dados['entregas_por_dia_semana']
    dias_labels = list(dias_data.keys())
    dias_values = list(dias_data.values())
    
    bars4 = ax4.bar(dias_labels, dias_values, color='#fd7e14', alpha=0.8)
    ax4.set_title('Entregas por Dia da Semana', fontweight='bold')
    ax4.set_ylabel('Quantidade')
    plt.setp(ax4.get_xticklabels(), rotation=45, ha='right')
    
    # Título geral
    fig.suptitle('Dashboard Analítico - Expresso Itaporanga', fontsize=18, fontweight='bold', y=0.98)
    
    plt.tight_layout()
    plt.subplots_adjust(top=0.93)
    plt.savefig(f'{output_dir}/dashboard_resumo.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("✅ Dashboard resumo criado: dashboard_resumo.png")

def main():
    """Função principal"""
    # Carregar dados da análise
    json_path = '/home/ubuntu/relatorio_analise_completa.json'
    
    if not os.path.exists(json_path):
        print(f"❌ Arquivo de dados não encontrado: {json_path}")
        return
    
    with open(json_path, 'r', encoding='utf-8') as f:
        dados = json.load(f)
    
    # Criar diretório para gráficos
    output_dir = '/home/ubuntu/site_integrado_expresso/graficos_analise'
    os.makedirs(output_dir, exist_ok=True)
    
    # Configurar matplotlib
    configurar_matplotlib()
    
    print("🎨 GERANDO VISUALIZAÇÕES GRÁFICAS")
    print("=" * 50)
    
    # Gerar todos os gráficos
    criar_grafico_status(dados, output_dir)
    criar_grafico_produtos(dados, output_dir)
    criar_grafico_dias_semana(dados, output_dir)
    criar_dashboard_resumo(dados, output_dir)
    
    print(f"\n✅ Todos os gráficos foram salvos em: {output_dir}")
    print("🎯 VISUALIZAÇÕES CONCLUÍDAS COM SUCESSO!")

if __name__ == "__main__":
    main()

