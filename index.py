from graphics import *
import csv
import os
import webbrowser

# Funções de manipulação do CSV

def ler_estoque():  # Função para ler e retornar o estoque do arquivo CSV
    with open('./media/estoque.csv', mode='r') as file:
        linhas = file.readlines()  # Lê todas as linhas do arquivo
    linhas_sem_cabecalho = linhas[1:]
    estoque = []
    for linha in linhas_sem_cabecalho:
        dados = linha.strip().split(',')
        estoque.append(dados)
    return estoque

def escrever_estoque(estoque): # função para escrever os dados no arquivo CSV
    with open('./media/estoque.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['ID', 'Nome', 'Valor', 'Quantidade'])
        writer.writerows(estoque)

def adicionar_item(nome, valor, quantidade): # função para adicionar um novo item ao estoque
    estoque = ler_estoque()
    novo_id = int(estoque[-1][0]) + 1 if estoque else 1
    with open('./media/estoque.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([novo_id, nome, valor, quantidade])

# Funções de interface

def gerar_lista(): # função para gerar uma lista de itens em html para o usuário
    estoque = ler_estoque()
    if not os.path.exists('generated_list'):
        os.makedirs('generated_list')
    file_path = 'generated_list/estoque.html'
    with open(file_path, mode='w') as file:
        file.write('<html><head><title>Estoque</title>\n')
        file.write('''<style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                display: flex;
                flex-direction: column;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            table {
                width: 60%;
                border-collapse: collapse;
                margin-top: 20px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                border-radius: 8px;
                overflow: hidden;
            }
            th, td {
                padding: 12px;
                text-align: center;
                border: 1px solid #ddd;
            }
            th {
                background-color: #5bc0de;
                font-size: 16px;
            }
            td {
                font-size: 14px;
            }
            h1 {
                text-align: center;
                font-size: 24px;
                margin-bottom: 20px;
            }
        </style>\n''')
        file.write('</head><body>\n')
        file.write('<h1>Estoque Atual</h1>\n')
        file.write("<table>\n<tr><th>ID</th><th>Nome</th><th>Valor</th><th>Quantidade</th></tr>\n")

        for item in estoque:
            file.write(f'<tr><td>{item[0]}</td><td>{item[1]}</td><td>R${float(item[2]):.2f}</td><td>{item[3]}</td></tr>\n')
        file.write('</table>\n</body></html>')

    # Abrir o arquivo gerado no navegador
    webbrowser.open(f'file://{os.path.abspath(file_path)}')

def criar_janela(titulo, largura, altura): # função para criar uma nova janela secundaria
    win = GraphWin(titulo, largura, altura)
    win.setCoords(0, 0, 10, 10)
    return win

def fechar_com_tecla(win): # função para fechar a janela ao pressionar Esc ou Enter
    while True:
        key = win.checkKey()
        if key == 'Escape':
            win.close()
            return

def janela_verificar_estoque(): # função para visualizar o estoque disponivel
    estoque = ler_estoque()
    win = criar_janela('Verificar Estoque', 800, 500)

    # Título
    titulo = Text(Point(5, 9.5), 'Estoque Atual')
    titulo.setSize(18)
    titulo.setStyle('bold')
    titulo.draw(win)

    # Cor do cabeçalho
    cor_cabecalho = 'lightblue'

    # Desenhando os retângulos de fundo para as células do cabeçalho
    retangulo_id = Rectangle(Point(0.5, 8.2), Point(2.9, 9))  # ID
    retangulo_id.setFill(cor_cabecalho)
    retangulo_id.setOutline(cor_cabecalho)
    retangulo_id.draw(win)

    retangulo_nome = Rectangle(Point(2.9, 8.2), Point(5.1, 9))  # Nome
    retangulo_nome.setFill(cor_cabecalho)
    retangulo_nome.setOutline(cor_cabecalho)
    retangulo_nome.draw(win)

    retangulo_valor = Rectangle(Point(5.1, 8.2), Point(8.1, 9))  # Valor
    retangulo_valor.setFill(cor_cabecalho)
    retangulo_valor.setOutline(cor_cabecalho)
    retangulo_valor.draw(win)

    retangulo_quantidade = Rectangle(Point(8.1, 8.2), Point(9.5, 9))  # Quantidade
    retangulo_quantidade.setFill(cor_cabecalho)
    retangulo_quantidade.setOutline(cor_cabecalho)
    retangulo_quantidade.draw(win)

    # Cabeçalho da tabela
    Text(Point(1.3, 8.6), 'ID').draw(win)
    Text(Point(3.3, 8.6), 'Nome').draw(win)
    Text(Point(5.5, 8.6), 'Valor').draw(win)
    Text(Point(8.1, 8.6), 'Quantidade').draw(win)

    # Desenhando o contorno quadrado ao redor da tabela
    contorno = Rectangle(Point(0.5, 9), Point(9.5, 0.5))  # Coordenadas do retângulo para contornar a área
    contorno.setWidth(2)  # Define a largura da borda
    contorno.draw(win)

    # Linha horizontal para separar o cabeçalho
    linha = Line(Point(0.5, 8.2), Point(9.5, 8.2))
    linha.setWidth(2)
    linha.draw(win)

    # Desenhando as linhas verticais para separar as colunas
    largura_coluna = 2.2  # Largura das colunas
    linha_vertical_1 = Line(Point(largura_coluna, 9), Point(largura_coluna, 0.5))  # Coluna 1 (ID)
    linha_vertical_1.setWidth(2)
    linha_vertical_1.draw(win)

    linha_vertical_2 = Line(Point(largura_coluna * 2, 9), Point(largura_coluna * 2, 0.5))  # Coluna 2 (Nome)
    linha_vertical_2.setWidth(2)
    linha_vertical_2.draw(win)

    linha_vertical_3 = Line(Point(largura_coluna * 3, 9), Point(largura_coluna * 3, 0.5))  # Coluna 3 (Valor)
    linha_vertical_3.setWidth(2)
    linha_vertical_3.draw(win)

    # Linhas da tabela
    y = 7.8
    for item in estoque:
        Text(Point(1.3, y-0.05), item[0]).draw(win)  # ID
        Text(Point(3.3, y-0.05), item[1]).draw(win)  # Nome
        Text(Point(5.5, y-0.05), f'R${float(item[2]):.2f}').draw(win)  # Valor formatado
        Text(Point(8.1, y-0.05), item[3]).draw(win)  # Quantidade
        y -= 0.6  # Descer para a próxima linha

    fechar_com_tecla(win)

def janela_cadastrar_peca(): # função para cadastrar uma nova peça
    win = criar_janela('Cadastrar Peça', 400, 300)

    # Título
    titulo = Text(Point(5, 9), 'Cadastrar Nova Peça')
    titulo.setSize(18)
    titulo.setStyle('bold')
    titulo.draw(win)

    # Campos
    Text(Point(2.7, 7), 'Nome:').draw(win)
    nome_entry = Entry(Point(5.7, 7), 19)
    nome_entry.draw(win)

    Text(Point(2.7, 6), 'Valor:').draw(win)
    valor_entry = Entry(Point(4.3, 6), 7)
    valor_entry.draw(win)

    Text(Point(2.7, 5), 'Qtd.:').draw(win)
    qtd_entry = Entry(Point(4.05, 5), 5)
    qtd_entry.draw(win)

    # Botão enviar
    enviar_btn = Rectangle(Point(4, 1.7), Point(6, 2.7))
    enviar_btn.setFill('yellow green')
    enviar_btn.draw(win)
    Text(Point(5, 2.2), 'Enviar').draw(win)

    # Mensagem de erro
    erro_text = Text(Point(5, 3.5), '')
    erro_text.setFill('red')
    erro_text.setSize(12)
    erro_text.draw(win)

    while True:
        click = win.checkMouse()
        key = win.checkKey()

        if key == 'Escape':
            win.close()
            return

        if click and 4 <= click.getX() <= 6 and 1.7 <= click.getY() <= 2.7:
            nome = nome_entry.getText().strip()
            valor_text = valor_entry.getText().strip()
            qtd_text = qtd_entry.getText().strip()

            if not nome:
                erro_text.setText('O nome não pode ser vazio!')
                continue

            try:
                valor = float(valor_text)
                if valor <= 0:
                    raise ValueError
            except ValueError:
                erro_text.setText('Valor inválido! Use números positivos.')
                continue

            try:
                quantidade = int(qtd_text)
                if quantidade <= 0:
                    raise ValueError
            except ValueError:
                erro_text.setText('Quantidade inválida! Use números inteiros.')
                continue

            # Adiciona a peça ao estoque
            adicionar_item(nome, valor, quantidade)
            erro_text.setText('')  # Limpa mensagens de erro
            win.close()

            # Exibe mensagem de sucesso
            exibir_mensagem('Sucesso','Peça cadastrada com sucesso!')
            return

def janela_realizar_compra(): # função para visualizar e realizar a compra de um item
    estoque = ler_estoque()
    win = criar_janela('Realizar Compra', 800, 500)

    # Título
    titulo = Text(Point(5, 9.5), 'Itens Disponíveis para Compra')
    titulo.setSize(18)
    titulo.setStyle('bold')
    titulo.draw(win)

    # Cor do cabeçalho
    cor_cabecalho = 'lightblue'

    # Desenhando os retângulos de fundo para as células do cabeçalho
    retangulo_id = Rectangle(Point(0.5, 8.2), Point(2.0, 9))  # ID ajustado
    retangulo_id.setFill(cor_cabecalho)
    retangulo_id.setOutline(cor_cabecalho)
    retangulo_id.draw(win)

    retangulo_nome = Rectangle(Point(2.0, 8.2), Point(5.0, 9))  # Nome ajustado
    retangulo_nome.setFill(cor_cabecalho)
    retangulo_nome.setOutline(cor_cabecalho)
    retangulo_nome.draw(win)

    retangulo_valor = Rectangle(Point(5.0, 8.2), Point(7.5, 9))  # Valor ajustado
    retangulo_valor.setFill(cor_cabecalho)
    retangulo_valor.setOutline(cor_cabecalho)
    retangulo_valor.draw(win)

    retangulo_quantidade = Rectangle(Point(7.5, 8.2), Point(8.5, 9))  # Quantidade ajustada
    retangulo_quantidade.setFill(cor_cabecalho)
    retangulo_quantidade.setOutline(cor_cabecalho)
    retangulo_quantidade.draw(win)

    retangulo_botao = Rectangle(Point(8.5, 8.2), Point(9.5, 9))  # Botão
    retangulo_botao.setFill(cor_cabecalho)
    retangulo_botao.setOutline(cor_cabecalho)
    retangulo_botao.draw(win)

    # Cabeçalho da tabela
    Text(Point(1, 8.6), 'ID').draw(win)
    Text(Point(2.5, 8.6), 'Nome').draw(win)
    Text(Point(4.5, 8.6), 'Valor').draw(win)
    Text(Point(6.8, 8.6), 'Quantidade').draw(win)
    Text(Point(9.0, 8.6), 'Comprar').draw(win)

    # Desenhando o contorno quadrado ao redor da tabela
    contorno = Rectangle(Point(0.5, 9), Point(9.5, 0.5))  # Coordenadas do retângulo para contornar a área
    contorno.setWidth(2)  # Define a largura da borda
    contorno.draw(win)

    # Linha horizontal para separar o cabeçalho
    linha = Line(Point(0.5, 8.2), Point(9.5, 8.2))
    linha.setWidth(2)
    linha.draw(win)

    # Desenhando as linhas verticais para separar as colunas
    linha_vertical_1 = Line(Point(1.5, 9), Point(1.5, 0.5))  # Coluna 1 (ID ajustada)
    linha_vertical_1.setWidth(2)
    linha_vertical_1.draw(win)

    linha_vertical_2 = Line(Point(3.5, 9), Point(3.5, 0.5))  # Coluna 2 (Nome ajustada)
    linha_vertical_2.setWidth(2)
    linha_vertical_2.draw(win)

    linha_vertical_3 = Line(Point(5.5, 9), Point(5.5, 0.5))  # Coluna 3 (Valor ajustada)
    linha_vertical_3.setWidth(2)
    linha_vertical_3.draw(win)

    linha_vertical_4 = Line(Point(8.0, 9), Point(8.0, 0.5))  # Coluna 4 (Quantidade ajustada)
    linha_vertical_4.setWidth(2)
    linha_vertical_4.draw(win)

    # Linhas da tabela e botões
    y = 7.8
    buttons = []
    for item in estoque:
        Text(Point(1, y-0.05), item[0]).draw(win)  # ID
        Text(Point(2.5, y-0.05), item[1]).draw(win)  # Nome
        Text(Point(4.5, y-0.05), f'R${float(item[2]):.2f}').draw(win)  # Valor formatado
        Text(Point(6.8, y-0.05), item[3]).draw(win)  # Quantidade

        # Botão 'Comprar'
        btn_comprar = Rectangle(Point(8.2, y - 0.25), Point(9.3, y + 0.25))
        btn_comprar.setFill('yellow green')
        btn_comprar.draw(win)
        Text(Point(8.75, y), 'Comprar').draw(win)
        buttons.append((btn_comprar, item[0]))  # Salvar botão e ID para interações
        y -= 0.6  # Descer para a próxima linha

    while True:
        click = win.checkMouse()
        key = win.checkKey()
        if key == 'Escape':
            win.close()
            return

        for btn, item_id in buttons:
            if click and btn.getP1().getX() <= click.getX() <= btn.getP2().getX() and \
               btn.getP1().getY() <= click.getY() <= btn.getP2().getY():
                win.close()
                realizar_compra(item_id)
                return

def realizar_compra(item_id):  # Função para realizar a compra de um item
    estoque = ler_estoque()

    # Procura o item correspondente ao ID
    for i in estoque:
        if i[0] == item_id:
            item = i
            break

    win = criar_janela('Quantidade', 400, 200)
    Text(Point(5, 7), f'Comprar {item[1]} (Qtd disponível: {item[3]})').draw(win)
    qtd_entry = Entry(Point(5, 5), 10)
    qtd_entry.draw(win)

    # Botão finalizar
    btn_finalizar = Rectangle(Point(4, 1.1), Point(6, 2.5))
    btn_finalizar.setFill('yellow green')
    btn_finalizar.draw(win)
    Text(Point(5, 1.8), 'Finalizar').draw(win)

    # Mensagem de erro
    erro_text = Text(Point(5, 3.5), '')
    erro_text.setFill('red')
    erro_text.setSize(12)
    erro_text.draw(win)

    while True:
        click = win.checkMouse()
        key = win.checkKey()
        if key == 'Escape':
            win.close()
            return

        # Verificação de clique no botão "Finalizar"
        if click and 4 <= click.getX() <= 6 and 1.1 <= click.getY() <= 2.5:
            quantidade_text = qtd_entry.getText().strip()

            # Verificação se o campo está vazio ou contém uma quantidade inválida
            if not quantidade_text:
                erro_text.setText('O campo de quantidade não pode estar vazio!')
                continue

            try:
                quantidade = int(quantidade_text)
                if quantidade <= 0:
                    erro_text.setText('A quantidade deve ser maior que zero!')
                    continue
            except ValueError:
                erro_text.setText('A quantidade deve ser um número inteiro válido!')
                continue

            # Verificação de quantidade disponível no estoque
            if quantidade > int(item[3]):
                erro_text.setText('Quantidade insuficiente para a compra!')
                continue

            # Atualização do estoque
            nova_qtd = int(item[3]) - quantidade
            if nova_qtd == 0:
                estoque = [i for i in estoque if i[0] != item_id]
            else:
                item[3] = nova_qtd
            escrever_estoque(estoque)

            win.close()
            exibir_mensagem('Sucesso', 'Compra realizada com sucesso!')
            return


def exibir_mensagem(titulo, mensagem): # função para exibir avisos
    win = criar_janela(titulo, 400, 200)

    # Exibir mensagem
    texto = Text(Point(5, 6), mensagem)
    texto.setSize(14)
    texto.draw(win)

    # Botão OK
    btn_ok = Rectangle(Point(4, 2), Point(6, 3))
    btn_ok.setFill('yellow green')
    btn_ok.draw(win)
    Text(Point(5, 2.5), 'OK').draw(win)

    while True:
        click = win.checkMouse()
        key = win.checkKey()
        if click and 4 <= click.getX() <= 6 and 2 <= click.getY() <= 3:
            win.close()
            return

def main(): # função principal de navegação
    # Criar janela principal maior e retangular
    win = GraphWin('Narrowhead Store', 500, 400)
    win.setCoords(0, 0, 12, 10)

    # Carregar e exibir a imagem do logo no topo
    logo = Image(Point(6, 6.9), 'media/logo.png')
    logo.draw(win)

    # Botões da primeira linha
    btn_verificar = Rectangle(Point(1.5, 2.5), Point(5.5, 3.7))
    btn_verificar.setFill('grey')
    btn_verificar.draw(win)
    texto_verificar = Text(Point(3.5, 3.1), 'Verificar Estoque')
    texto_verificar.setSize(12)
    texto_verificar.setStyle('bold')
    texto_verificar.draw(win)

    btn_cadastrar = Rectangle(Point(6.5, 2.5), Point(10.5, 3.7))
    btn_cadastrar.setFill('grey')
    btn_cadastrar.draw(win)
    texto_cadastrar = Text(Point(8.5, 3.1), 'Cadastrar Peça')
    texto_cadastrar.setSize(12)
    texto_cadastrar.setStyle('bold')
    texto_cadastrar.draw(win)

    # Botões da segunda linha
    btn_gerar_lista = Rectangle(Point(1.5, 1), Point(5.5, 2.2))
    btn_gerar_lista.setFill('grey')
    btn_gerar_lista.draw(win)
    texto_gerar_lista = Text(Point(3.5, 1.6), 'Gerar Lista')
    texto_gerar_lista.setSize(12)
    texto_gerar_lista.setStyle('bold')
    texto_gerar_lista.draw(win)

    btn_comprar = Rectangle(Point(6.5, 1), Point(10.5, 2.2))
    btn_comprar.setFill('grey')
    btn_comprar.draw(win)
    texto_comprar = Text(Point(8.5, 1.6), 'Realizar Compra')
    texto_comprar.setSize(12)
    texto_comprar.setStyle('bold')
    texto_comprar.draw(win)

    # Loop principal para interação
    while not win.isClosed():
        click = win.checkMouse()
        if click:
            x, y = click.getX(), click.getY()
            if 1.5 <= x <= 5.5 and 2.5 <= y <= 3.7:
                janela_verificar_estoque()
            elif 6.5 <= x <= 10.5 and 2.5 <= y <= 3.7:
                janela_cadastrar_peca()
            elif 1.5 <= x <= 5.5 and 1 <= y <= 2.2:
                gerar_lista()
            elif 6.5 <= x <= 10.5 and 1 <= y <= 2.2:
                janela_realizar_compra()

if __name__ == '__main__': # chamada da função principal
    main()