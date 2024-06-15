from datetime import datetime
import sqlite3

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
            data_venda TEXT NOT NULL,
            ano_mes TEXT NOT NULL  -- Nova coluna para ano e mês
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            preco REAL NOT NULL,
            quantidade INTEGER NOT NULL
        )
    ''')

    conn.commit()
    return conn, cursor


def consultar_produto(nome):
    conn, cursor = conectar_db()
    cursor.execute('SELECT * FROM produtos WHERE nome = ?', (nome,))
    produto = cursor.fetchone()
    conn.close()
    return produto

def cadastrar_venda(item, preco, quantidade, tipo_quantidade, tipo_pagamento):
    conn, cursor = conectar_db()
    data_venda = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    ano_mes = datetime.now().strftime('%Y-%m')
    cursor.execute('''
        INSERT INTO vendas (item, preco, quantidade, tipo_quantidade, tipo_pagamento, data_venda, ano_mes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (item, preco, quantidade, tipo_quantidade, tipo_pagamento, data_venda, ano_mes))
    conn.commit()
    conn.close()



def obter_vendas():
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

def cadastrar_produto(nome, quantidade, preco):
    conn, cursor = conectar_db()
    cursor.execute('''
        INSERT INTO produtos (nome, quantidade, preco)
        VALUES (?, ?, ?)
    ''', (nome, quantidade, preco))
    conn.commit()
    conn.close()

def obter_todos_produtos():
    conn, cursor = conectar_db()
    cursor.execute('SELECT * FROM produtos')
    produtos = cursor.fetchall()
    conn.close()
    
    # Filtrar os produtos para excluir aqueles com valores não numéricos na coluna de preço
    produtos_filtrados = [produto for produto in produtos if is_numeric(produto[3])]
    
    return produtos_filtrados

def is_numeric(value):
    try:
        float(value)
        return True
    except ValueError:
        return False



def obter_produto(nome, quantidade, preco):
    conn, cursor = conectar_db()
    cursor.execute('SELECT * FROM produtos WHERE LOWER(nome) = LOWER(?) AND quantidade = ? AND preco = ?', (nome, quantidade, preco))
    produto = cursor.fetchone()
    conn.close()
    return produto

def cadastrar_produto_se_necessario(item, quantidade, preco):
    produto = obter_produto(item)
    if not produto:
        cadastrar_produto(item, quantidade, preco)

def excluir_produto_db(nome):
    conn, cursor = conectar_db()
    cursor.execute('DELETE FROM produtos WHERE LOWER(nome) = LOWER(?)', (nome,))
    conn.commit()
    conn.close()

def alterar_produto_db(produto_id, nome, quantidade, preco):
    conn, cursor = conectar_db()
    cursor.execute('''
        UPDATE produtos
        SET nome = ?, quantidade = ?, preco = ?
        WHERE id = ?
    ''', (nome, quantidade, preco, produto_id))
    conn.commit()
    conn.close()    


def atualizar_estoque(nome, quantidade):
    conn, cursor = conectar_db()
    cursor.execute('''
        UPDATE produtos
        SET quantidade = quantidade + ?
        WHERE nome = ?
    ''', (quantidade, nome))
    conn.commit()
    conn.close()

def obter_todas_vendas_cadastradas():
    conn, cursor = conectar_db()
    cursor.execute('SELECT nome FROM produtos ')
    vendas = cursor.fetchall()
    conn.close()
    return vendas

# Função para obter vendas por mês
def obter_vendas_por_mes(mes_numero, ano):
    conn, cursor = conectar_db()
    mes_ano = f"{ano}-{mes_numero:02d}"
    cursor.execute('SELECT * FROM vendas WHERE ano_mes = ?', (mes_ano,))
    vendas = cursor.fetchall()
    conn.close()
    return vendas





