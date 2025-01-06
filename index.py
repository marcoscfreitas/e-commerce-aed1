from graphics import *
import csv
import os
import webbrowser

# funções p facilitar manipulação do csv

def ler_estoque():  # função para ler e retornar o estoque do arquivo csv
    with open('./media/estoque.csv', mode='r') as arq:
        linhas = arq.readlines()  # lê todas as linhas do arquivo
    linhas_sem_cabecalho = linhas[1:] # remove o cabeçalho
    estoque = []
    for linha in linhas_sem_cabecalho:
        dados = linha.strip().split(',')
        estoque.append(dados)
    return estoque

def escrever_estoque(estoque): # função para escrever e atualizar dados no csv
    with open('./media/estoque.csv', mode='w', newline='') as arq:
        arq = csv.writer(arq) # writer para escrever no arquivo
        arq.writerow(['ID', 'Nome', 'Valor', 'Quantidade'])
        arq.writerows(estoque) # atualiza estoque quando chamada a função

def adicionar_item(nome, valor, quantidade):  # função para adicionar um novo item ao estoque
    estoque = ler_estoque()
    # gerar novo id para o item adicionado
    if len(estoque) == 0:  # se estiver vazio id será 1
        novo_id = 1
    else:  # caso contrário, somar 1 ao último id
        ultimo_item = estoque[-1]
        ultimo_id = int(ultimo_item[0])
        novo_id = ultimo_id + 1
    # adiciona o novo item no csv
    with open('./media/estoque.csv', mode='a', newline='') as arq:
        arq = csv.writer(arq)
        arq.writerow([novo_id, nome, valor, quantidade])

# funções para design das janelas e interfaces

def gerar_lista(): # função para gerar uma lista de itens em html para o usuário
    estoque = ler_estoque()
    file_path = 'generated_list/estoque.html'
    with open(file_path, mode='w') as arq:
        arq.write('<html><head><title>Estoque</title>\n')
        arq.write('''<style>
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
        arq.write('</head><body>\n')
        arq.write('<h1>Estoque Atual</h1>\n')
        arq.write("<table>\n<tr><th>ID</th><th>Nome</th><th>Valor</th><th>Quantidade</th></tr>\n")

        for item in estoque:
            arq.write(f'<tr><td>{item[0]}</td><td>{item[1]}</td><td>R${float(item[2]):.2f}</td><td>{item[3]}</td></tr>\n')
        arq.write('</table>\n</body></html>')

    # webbrowser para abrir o arquivo html gerado no navegador
    webbrowser.open(f'file://{os.path.abspath(file_path)}')

def criar_janela(titulo, largura, altura): # função para criar uma nova janela secundaria
    win = GraphWin(titulo, largura, altura) # chama titulo largura e altura de acordo com o desejado de outras funções
    win.setCoords(0, 0, 10, 10)
    return win

def fechar_com_tecla(win): # função para fechar a janela ao pressionar Esc
    while True:
        key = win.checkKey()
        if key == 'Escape':
            win.close()
            return

def janela_verificar_estoque(): # função para visualizar o estoque disponivel
    estoque = ler_estoque()
    win = criar_janela('Verificar Estoque', 800, 500)

    # design do título
    titulo = Text(Point(5, 9.5), 'Estoque Atual')
    titulo.setSize(18)
    titulo.setStyle('bold')
    titulo.draw(win)

    # desenhando retangulos para células do cabeçalho
    retangulo_id = Rectangle(Point(0.5, 8.2), Point(2.9, 9))  # ID
    retangulo_id.setFill('lightblue')
    retangulo_id.setOutline('lightblue')
    retangulo_id.draw(win)

    retangulo_nome = Rectangle(Point(2.9, 8.2), Point(5.1, 9))  # nome
    retangulo_nome.setFill('lightblue')
    retangulo_nome.setOutline('lightblue')
    retangulo_nome.draw(win)

    retangulo_valor = Rectangle(Point(5.1, 8.2), Point(8.1, 9))  # valor
    retangulo_valor.setFill('lightblue')
    retangulo_valor.setOutline('lightblue')
    retangulo_valor.draw(win)

    retangulo_quantidade = Rectangle(Point(8.1, 8.2), Point(9.5, 9))  # quantidade
    retangulo_quantidade.setFill('lightblue')
    retangulo_quantidade.setOutline('lightblue')
    retangulo_quantidade.draw(win)

    # texto para cabeçalho
    Text(Point(1.3, 8.6), 'ID').draw(win)
    Text(Point(3.3, 8.6), 'Nome').draw(win)
    Text(Point(5.5, 8.6), 'Valor').draw(win)
    Text(Point(8.1, 8.6), 'Quantidade').draw(win)

    # estilizando para ficar em formato tabela mais decente e organizado
    contorno = Rectangle(Point(0.5, 9), Point(9.5, 0.5))  # coordenadas do retângulo para contornar a área
    contorno.setWidth(2)
    contorno.draw(win)

    # linha horizontal para separar o cabeçalho
    linha = Line(Point(0.5, 8.2), Point(9.5, 8.2))
    linha.setWidth(2)
    linha.draw(win)

    # linhas verticais para estilizar tabela e separar colunas
    linha_vertical_1 = Line(Point(2.2, 9), Point(2.2, 0.5))  # coluna id
    linha_vertical_1.setWidth(2)
    linha_vertical_1.draw(win)

    linha_vertical_2 = Line(Point((2.2 * 2), 9), Point((2.2 * 2), 0.5))  # coluna nome
    linha_vertical_2.setWidth(2)
    linha_vertical_2.draw(win)

    linha_vertical_3 = Line(Point((2.2 * 3), 9), Point((2.2 * 3), 0.5))  # coluna valor
    linha_vertical_3.setWidth(2)
    linha_vertical_3.draw(win)

    # escrever linhas da tabela
    y = 7.8
    for item in estoque:
        Text(Point(1.3, y-0.05), item[0]).draw(win)  # id
        Text(Point(3.3, y-0.05), item[1]).draw(win)  # nome
        Text(Point(5.5, y-0.05), f'R${float(item[2]):.2f}').draw(win)  # valor format
        Text(Point(8.1, y-0.05), item[3]).draw(win)  # quantidade
        y -= 0.6  # diminui y para descer linha

    fechar_com_tecla(win) # caso pressionado esc, o while loop é quebrado e a janela é fechada

def janela_cadastrar_peca(): # função para cadastrar uma nova peça
    win = criar_janela('Cadastrar Peça', 400, 300)

    # design do título
    titulo = Text(Point(5, 9), 'Cadastrar Nova Peça')
    titulo.setSize(18)
    titulo.setStyle('bold')
    titulo.draw(win)

    # campos para preenchimento da peça
    Text(Point(2.7, 7), 'Nome:').draw(win)
    nome_entry = Entry(Point(5.7, 7), 19)
    nome_entry.draw(win)

    Text(Point(2.7, 6), 'Valor:').draw(win)
    valor_entry = Entry(Point(4.3, 6), 7)
    valor_entry.draw(win)

    Text(Point(2.7, 5), 'Qtd.:').draw(win)
    qtd_entry = Entry(Point(4.05, 5), 5)
    qtd_entry.draw(win)

    # botão enviar
    enviar_btn = Rectangle(Point(4, 1.7), Point(6, 2.7))
    enviar_btn.setFill('yellow green')
    enviar_btn.draw(win)
    Text(Point(5, 2.2), 'Enviar').draw(win)

    # mensagem de erro
    erro_text = Text(Point(5, 3.5), '') # inicialmente vazio e usado para exibir mensagens de erro
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
                erro_text.setText('O nome não pode ser vazio!') # verifica se o campo nome está vazio
                continue

            try:
                valor = float(valor_text)
                if valor <= 0:
                    raise ValueError
            except ValueError:
                erro_text.setText('Valor inválido! Use números positivos.') # verifica se o valor é um número positivo
                continue

            try:
                quantidade = int(qtd_text)
                if quantidade <= 0:
                    raise ValueError
            except ValueError:
                erro_text.setText('Quantidade inválida! Use números inteiros.') # verifica se a quantidade é um número inteiro
                continue

            # adiciona a peça ao estoque caso nao haja erros
            adicionar_item(nome, valor, quantidade)
            erro_text.setText('')  # limpa mensagem de erro antes de fechar a janela
            win.close()

            # exibe mensagem de sucesso
            exibir_mensagem('Sucesso','Peça cadastrada com sucesso!')
            return

def janela_realizar_compra():  # função para visualizar e realizar a compra de um item
    estoque = ler_estoque()
    win = criar_janela('Realizar Compra', 800, 500)

    # design do título
    titulo = Text(Point(5, 9.5), 'Itens Disponíveis para Compra')
    titulo.setSize(18)
    titulo.setStyle('bold')
    titulo.draw(win)

    # desenhando retangulos para células do cabeçalho
    retangulo_id = Rectangle(Point(0.5, 8.2), Point(2.0, 9))  # coluna id
    retangulo_id.setFill('lightblue')
    retangulo_id.setOutline('lightblue')
    retangulo_id.draw(win)

    retangulo_nome = Rectangle(Point(2.0, 8.2), Point(5.0, 9))  # coluna nome
    retangulo_nome.setFill('lightblue')
    retangulo_nome.setOutline('lightblue')
    retangulo_nome.draw(win)

    retangulo_valor = Rectangle(Point(5.0, 8.2), Point(7.5, 9))  # coluna valor
    retangulo_valor.setFill('lightblue')
    retangulo_valor.setOutline('lightblue')
    retangulo_valor.draw(win)

    retangulo_quantidade = Rectangle(Point(7.5, 8.2), Point(8.5, 9))  # coluna quantidade
    retangulo_quantidade.setFill('lightblue')
    retangulo_quantidade.setOutline('lightblue')
    retangulo_quantidade.draw(win)

    retangulo_botao = Rectangle(Point(8.5, 8.2), Point(9.5, 9))  # coluna com botão de compra
    retangulo_botao.setFill('lightblue')
    retangulo_botao.setOutline('lightblue')
    retangulo_botao.draw(win)

    # texto para cabeçalho
    Text(Point(1, 8.6), 'ID').draw(win)
    Text(Point(2.5, 8.6), 'Nome').draw(win)
    Text(Point(4.5, 8.6), 'Valor').draw(win)
    Text(Point(6.8, 8.6), 'Quantidade').draw(win)
    Text(Point(9.0, 8.6), 'Comprar').draw(win)

    # estilizando para ficar em formato tabela mais decente e organizado
    contorno = Rectangle(Point(0.5, 9), Point(9.5, 0.5))  # coordenadas do retângulo para contornar a área
    contorno.setWidth(2)
    contorno.draw(win)

    # linha horizontal para separar o cabeçalho
    linha = Line(Point(0.5, 8.2), Point(9.5, 8.2))
    linha.setWidth(2)
    linha.draw(win)

    # linhas verticais para estilizar tabela e separar colunas
    linha_vertical_1 = Line(Point(1.5, 9), Point(1.5, 0.5))  # coluna id
    linha_vertical_1.setWidth(2)
    linha_vertical_1.draw(win)

    linha_vertical_2 = Line(Point(3.5, 9), Point(3.5, 0.5))  # coluna nome
    linha_vertical_2.setWidth(2)
    linha_vertical_2.draw(win)

    linha_vertical_3 = Line(Point(5.5, 9), Point(5.5, 0.5))  # coluna valor
    linha_vertical_3.setWidth(2)
    linha_vertical_3.draw(win)

    linha_vertical_4 = Line(Point(8.0, 9), Point(8.0, 0.5))  # coluna quantidade
    linha_vertical_4.setWidth(2)
    linha_vertical_4.draw(win)

    # linhas da tabela e botões
    y = 7.8
    buttons = []
    for item in estoque:
        Text(Point(1, y-0.05), item[0]).draw(win)  # id
        Text(Point(2.5, y-0.05), item[1]).draw(win)  # nome
        Text(Point(4.5, y-0.05), f'R${float(item[2]):.2f}').draw(win)  # valor
        Text(Point(6.8, y-0.05), item[3]).draw(win)  # quantidade

        # botão de compra
        btn_comprar = Rectangle(Point(8.2, y - 0.25), Point(9.3, y + 0.25))
        btn_comprar.setFill('yellow green')
        btn_comprar.draw(win)
        Text(Point(8.75, y), 'Comprar').draw(win)
        buttons.append([btn_comprar, item[0]])  # armazena o botão e o id do item
        #print(buttons)
        y -= 0.6  # diminui y para descer linha

    while True:
        click = win.checkMouse()
        key = win.checkKey()
        if key == 'Escape':
            win.close()
            return

        for button in buttons:
            #print(button)
            btn_comprar = button[0] # armazena o botao para verificar se foi clicado
            item_id = button[1] # armazena o id do item para enviar para função de realizar compra
            if click and btn_comprar.getP1().getX() <= click.getX() <= btn_comprar.getP2().getX() and btn_comprar.getP1().getY() <= click.getY() <= btn_comprar.getP2().getY(): # verifica se o botão foi clicado
                win.close()
                realizar_compra(item_id)
                return

def realizar_compra(item_id):  # Função para realizar a compra de um item
    estoque = ler_estoque()

    for i in estoque: # for para percorrer o estoque e encontrar o item com o id correspondente
        if i[0] == item_id:
            item = i
            break

    win = criar_janela('Quantidade', 400, 200)
    Text(Point(5, 7), f'Comprar {item[1]} (Qtd disponível: {item[3]})').draw(win)
    qtd_entry = Entry(Point(5, 5), 10)
    qtd_entry.draw(win)

    # botão finalizar
    btn_finalizar = Rectangle(Point(4, 1.1), Point(6, 2.5))
    btn_finalizar.setFill('yellow green')
    btn_finalizar.draw(win)
    Text(Point(5, 1.8), 'Finalizar').draw(win)

    # mensagem para exibir erros, inicialmente vazia
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

        # verificação de clique no botão "finalizar"
        if click and 4 <= click.getX() <= 6 and 1.1 <= click.getY() <= 2.5:
            quantidade_text = qtd_entry.getText().strip()

            # verificação se o campo está vazio ou contém uma quantidade inválida
            if not quantidade_text:
                erro_text.setText('O campo de quantidade não pode estar vazio!') # verifica se o campo de quantidade está vazio
                continue

            try:
                quantidade = int(quantidade_text)
                if quantidade <= 0:
                    erro_text.setText('A quantidade deve ser maior que zero!') # verifica se a quantidade é maior que zero
                    continue
            except ValueError:
                erro_text.setText('A quantidade deve ser um número inteiro válido!') # verifica se a quantidade é um número inteiro
                continue

            if quantidade > int(item[3]):
                erro_text.setText('Quantidade insuficiente para a compra!') # verifica se a quantidade é maior que a disponível
                continue

            # atualiza o estoque com a quantidade diminuída
            nova_qtd = int(item[3]) - quantidade
            if nova_qtd == 0:
                for i in estoque: # for para percorrer o estoque e encontrar o item com o id correspondente
                    if i[0] == item_id:
                        estoque.remove(i)  # remove o item do estoque
                        break
            else:
                item[3] = nova_qtd
            escrever_estoque(estoque) # atualiza o estoque no csv
            win.close()
            exibir_mensagem('Sucesso', 'Compra realizada com sucesso!') # abre nova janela com mensagem de sucesso
            return


def exibir_mensagem(titulo, mensagem): # função para exibir avisos
    win = criar_janela(titulo, 400, 200)

    # texto da mensagem
    texto = Text(Point(5, 6), mensagem)
    texto.setSize(14)
    texto.draw(win)

    # botão ok
    btn_ok = Rectangle(Point(4, 2), Point(6, 3))
    btn_ok.setFill('yellow green')
    btn_ok.draw(win)
    Text(Point(5, 2.5), 'OK').draw(win)

    while True:
        click = win.checkMouse()
        if click and 4 <= click.getX() <= 6 and 2 <= click.getY() <= 3: # verifica se o botão foi clicado
            win.close()
            return

def main(): # função principal de navegação
    # criar janela principal maior
    win = GraphWin('Narrowhead Store', 500, 400)
    win.setCoords(0, 0, 12, 10)

    # carregar e exibir a imagem do logo no topo
    logo = Image(Point(6, 6.9), 'media/logo.png')
    logo.draw(win)

    # botões da primeira linha
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

    # botões da segunda linha
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

    # loop principal para interação
    while not win.isClosed():
        click = win.checkMouse()
        if click:
            x = click.getX()
            y = click.getY()
            if 1.5 <= x <= 5.5 and 2.5 <= y <= 3.7: # verifica se o clique foi feito dentro do botão 1
                janela_verificar_estoque()
            elif 6.5 <= x <= 10.5 and 2.5 <= y <= 3.7: # verifica se o clique foi feito dentro do botão 2
                janela_cadastrar_peca()
            elif 1.5 <= x <= 5.5 and 1 <= y <= 2.2: # verifica se o clique foi feito dentro do botão 3
                gerar_lista()
            elif 6.5 <= x <= 10.5 and 1 <= y <= 2.2: # verifica se o clique foi feito dentro do botão 4
                janela_realizar_compra()

if __name__ == '__main__': # chama a função main
    main()