import sqlite3
import csv
import shutil
import os

from datetime import date, datetime, timedelta
from tkinter import filedialog, messagebox

def conectar_db():
    conn = sqlite3.connect('vendas.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vendas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item TEXT NOT NULL,
            preco REAL NOT NULL,
            quantidade INTEGER NOT NULL,
            tipo_quantidade TEXT NOT NULL,
            tipo_pagamento TEXT NOT NULL,
            data_venda TEXT NOT NULL
        )
    ''')
    conn.commit()
    return conn, cursor

def cadastrar_venda(item, preco, quantidade, tipo_quantidade, tipo_pagamento):
    conn, cursor = conectar_db()
    data_venda = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    cursor.execute('''
        INSERT INTO vendas (item, preco, quantidade, tipo_quantidade, tipo_pagamento, data_venda)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (item, preco, quantidade, tipo_quantidade, tipo_pagamento, data_venda))
    conn.commit()
    conn.close()

def obter_vendas():
    conn, cursor = conectar_db()
    cursor.execute('SELECT * FROM vendas')
    vendas = cursor.fetchall()
    conn.close()
    return vendas

def obter_dados_venda():
    conn, cursor = conectar_db()
    cursor.execute('SELECT * FROM vendas')
    vendas = cursor.fetchall()
    conn.close()
    return vendas

def excluir_venda_db(venda_id):
    conn, cursor = conectar_db()
    cursor.execute('DELETE FROM vendas WHERE id = ?', (venda_id,))
    conn.commit()
    conn.close()

def alterar_venda_db(venda_id, item, preco, quantidade, tipo_quantidade, tipo_pagamento):
    conn, cursor = conectar_db()
    cursor.execute('''
        UPDATE vendas
        SET item = ?, preco = ?, quantidade = ?, tipo_quantidade = ?, tipo_pagamento = ?
        WHERE id = ?
    ''', (item, preco, quantidade, tipo_quantidade, tipo_pagamento, venda_id))
    conn.commit()
    conn.close()

def gerar_relatorio_dia(vendas):
    today = datetime.today().strftime('%Y-%m-%d')
    vendas_dia = [venda for venda in vendas if venda[6].startswith(today)]
    
    relatorio = []

    for venda in vendas_dia:
        preco_formatado = f"{venda[2]:.2f}".replace(".", ",")
        venda_formatada = (*venda[:2], preco_formatado, *venda[3:])
        relatorio.append(venda_formatada)
    
    return relatorio

def exportar_vendas_para_csv(file_path):
    vendas = obter_vendas()
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Item", "Preço (R$)", "Quantidade", "Tipo de Quantidade", "Tipo de Pagamento", "Data da Venda"])
        for venda in vendas:
            writer.writerow(venda)

def backup_manual():
    # Diretório do banco de dados
    diretorio_db = 'vendas.db'

    # Diretório para salvar o backup
    diretorio_backup = 'backup/'

    # Criar o diretório de backup se não existir
    if not os.path.exists(diretorio_backup):
        os.makedirs(diretorio_backup)

    # Nome do arquivo de backup com timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')  # Use datetime.now() corretamente
    arquivo_backup = f'{diretorio_backup}backup_{timestamp}.db'

    # Copiar o banco de dados para o arquivo de backup
    shutil.copy2(diretorio_db, arquivo_backup)

    # Mensagem de sucesso
    messagebox.showinfo("Backup Realizado", f"Backup realizado com sucesso em: {arquivo_backup}")


    # Conectar ao banco de dados
    conn = sqlite3.connect('vendas.db')
    cursor = conn.cursor()

    # Obter o primeiro e o último dia do mês atual
    primeiro_dia_mes = date.today().replace(day=1)
    ultimo_dia_mes = date.today().replace(day=1, month=date.today().month % 12 + 1) - timedelta(days=1)

    # Consulta SQL para obter as vendas do mês atual
    consulta = '''
        SELECT * FROM vendas
        WHERE data_venda BETWEEN ? AND ?
    '''

    # Executar a consulta SQL
    cursor.execute(consulta, (primeiro_dia_mes, ultimo_dia_mes))

    # Recuperar as vendas do mês atual
    vendas_mes_atual = cursor.fetchall()

    # Fechar a conexão com o banco de dados
    conn.close()

    # Retornar as vendas do mês atual
    return vendas_mes_atual