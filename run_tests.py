#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para executar todos os testes da aplicação Expresso Itaporanga
"""

import sys
import os
import unittest

# Adicionar o diretório raiz ao path
sys.path.insert(0, os.path.dirname(__file__))

def main():
    """Função principal para executar os testes"""
    print("=" * 60)
    print("EXECUTANDO TESTES - EXPRESSO ITAPORANGA")
    print("=" * 60)
    
    # Descobrir todos os testes
    loader = unittest.TestLoader()
    start_dir = os.path.join(os.path.dirname(__file__), 'tests')
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    # Executar testes
    runner = unittest.TextTestRunner(
        verbosity=2,
        stream=sys.stdout,
        buffer=True
    )
    
    result = runner.run(suite)
    
    # Mostrar resumo
    print("\n" + "=" * 60)
    print("RESUMO DOS TESTES")
    print("=" * 60)
    print(f"Testes executados: {result.testsRun}")
    print(f"Sucessos: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Falhas: {len(result.failures)}")
    print(f"Erros: {len(result.errors)}")
    
    if result.failures:
        print("\nFALHAS:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback.split('AssertionError: ')[-1].split('\\n')[0]}")
    
    if result.errors:
        print("\nERROS:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback.split('\\n')[-2]}")
    
    # Calcular taxa de sucesso
    if result.testsRun > 0:
        success_rate = ((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun) * 100
        print(f"\nTaxa de sucesso: {success_rate:.1f}%")
    
    print("=" * 60)
    
    # Retornar código de saída
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
