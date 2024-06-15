import tkinter as tk
from interface import iniciar_interface, gerar_relatorio_dia
from operations import obter_vendas, gerar_relatorio_dia

def main():
    vendas = obter_vendas()
    iniciar_interface()
    gerar_relatorio_dia(vendas)

    
if __name__ == "__main__":
    main()
