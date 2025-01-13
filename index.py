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

def atualizar_estoque(estoque): # função para escrever e atualizar dados no csv
    with open('./media/estoque.csv', mode='w', newline='') as arq: # newline para desabilitar quebra de linha ao manipular csv
        writer = csv.writer(arq) # writer para escrever no arquivo
        writer.writerow(['ID', 'Nome', 'Valor', 'Quantidade'])
        writer.writerows(estoque) # atualiza estoque quando chamada a função

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
        writer = csv.writer(arq)
        writer.writerow([novo_id, nome, valor, quantidade])

# funções básicas

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

def exibir_mensagem(titulo, mensagem): # função para exibir avisos
    win = criar_janela(titulo, 400, 200)

    # texto da mensagem
    texto = Text(Point(5, 6), mensagem)
    texto.setSize(14)
    texto.draw(win)

    # botão ok
    btn_ok = Rectangle(Point(4, 2), Point(6, 3))
    btn_ok.setFill('lawn green')
    btn_ok.draw(win)
    Text(Point(5, 2.5), 'OK').draw(win)

    while True:
        click = win.checkMouse()
        if click and 4 <= click.getX() <= 6 and 2 <= click.getY() <= 3: # verifica se o botão foi clicado
            win.close()
            return

# funções funcionalidades

def janela_verificar_estoque():  # função para visualizar o estoque disponível
    estoque = ler_estoque()
    estoque_pesquisado = estoque[:]  # lista de itens filtrados, inicialmente igual ao estoque completo

    def desenhar_pagina(win, pagina):  # função para desenhar a página
        win.delete('all')  # limpa a janela

        # título
        titulo = Text(Point(5, 9.5), f'Estoque - Página {pagina}')
        titulo.setSize(20)
        titulo.setStyle('bold')
        titulo.draw(win)

        # desenhando retângulo para células do cabeçalho
        retangulo_header = Rectangle(Point(0, 8.2), Point(11, 9))
        retangulo_header.setFill('aqua')
        retangulo_header.draw(win)

        # cabeçalho
        Text(Point(1, 8.6), 'ID').draw(win)
        Text(Point(3.5, 8.6), 'Nome').draw(win)
        Text(Point(6, 8.6), 'Valor').draw(win)
        Text(Point(8.5, 8.6), 'Quantidade').draw(win)

        # desenhar os itens com base na página
        y = 7.8

        if pagina == 1:
            itens_pagina = estoque_pesquisado[:10]  # primeiros 10 itens
        else:
            itens_pagina = estoque_pesquisado[10:20]  # itens 11 a 20

        for item in itens_pagina:
            Text(Point(1, y - 0.05), item[0]).draw(win)  # ID
            Text(Point(3.5, y - 0.05), item[1]).draw(win)  # Nome
            Text(Point(6, y - 0.05), f'R${float(item[2]):.2f}').draw(win)  # Valor
            Text(Point(8.5, y - 0.05), item[3]).draw(win)  # Quantidade
            y -= 0.6

        # botões de navegação
        if pagina == 2:  # botão para página anterior
            botao_anterior = Rectangle(Point(1, 1.2), Point(1.5, 1.8))
            botao_anterior.setFill('lightgray')
            botao_anterior.draw(win)
            Text(botao_anterior.getCenter(), '<').draw(win)

        if pagina == 1:  # botão para próxima página
            botao_proxima = Rectangle(Point(8, 1.2), Point(8.5, 1.8))
            botao_proxima.setFill('lightgray')
            botao_proxima.draw(win)
            Text(botao_proxima.getCenter(), '>').draw(win)

        # campo de pesquisa
        Text(Point(3.3, 1.5), 'Pesquisar:').draw(win)
        input_pesquisa = Entry(Point(5, 1.5), 20)
        input_pesquisa.draw(win)

        # botão para realizar a pesquisa
        botao_pesquisar = Rectangle(Point(6.2, 1.3), Point(6.7, 1.7))
        botao_pesquisar.setFill('lawn green')
        botao_pesquisar.draw(win)
        Text(botao_pesquisar.getCenter(), '🔎').draw(win)

        return input_pesquisa

    # cria a janela
    win = criar_janela('Verificar Estoque', 800, 600)
    input_pesquisa = desenhar_pagina(win, 1)  # inicia na página 1

    while True:
        click = win.checkMouse()
        key = win.checkKey()

        if key == 'Escape':  # fecha a janela ao pressionar esc
            win.close()
            return

        if click:  # verifica cliques para navegação ou pesquisa
            x, y = click.getX(), click.getY()

            # navega para a página 1 (anterior)
            if 1 <= x <= 2 and 1.2 <= y <= 1.8:
                input_pesquisa = desenhar_pagina(win, 1)

            # navega para a página 2 (próxima)
            elif 8 <= x <= 9 and 1.2 <= y <= 1.8:
                input_pesquisa = desenhar_pagina(win, 2)

            # realiza a pesquisa ao clicar no botão de pesquisa
            elif 6.2 <= x <= 6.7 and 1.3 <= y <= 1.7:
                texto_pesquisa = input_pesquisa.getText().strip().lower()  # texto do campo de pesquisa
                estoque_pesquisado = []  # cria uma lista vazia para armazenar os itens filtrados
                for item in estoque:  # percorre cada item no estoque
                    if texto_pesquisa in item[1].lower():  # verifica se o texto pesquisado está no nome do item
                        estoque_pesquisado.append(item)  # adiciona o item à lista filtrada
                input_pesquisa = desenhar_pagina(win, 1)  # reinicia para a página 1

def janela_cadastrar_item(): # função para cadastrar um novo item
    win = criar_janela('Cadastrar Item', 400, 300)

    # design do título
    titulo = Text(Point(5, 9), 'Cadastrar Novo Item')
    titulo.setSize(20)
    titulo.setStyle('bold')
    titulo.draw(win)

    # campos para preenchimento do item
    Text(Point(2.7, 7), 'Nome:').draw(win)
    input_nome = Entry(Point(5.7, 7), 19)
    input_nome.draw(win)

    Text(Point(2.7, 6), 'Valor:').draw(win)
    input_valor = Entry(Point(4.3, 6), 7)
    input_valor.draw(win)

    Text(Point(2.7, 5), 'Qtd.:').draw(win)
    input_qtd = Entry(Point(4.05, 5), 5)
    input_qtd.draw(win)

    # botão enviar
    button_enviar = Rectangle(Point(4, 1.7), Point(6, 2.7))
    button_enviar.setFill('lawn green')
    button_enviar.draw(win)
    Text(Point(5, 2.2), 'Enviar').draw(win)

    # mensagem de erro
    texto_erro = Text(Point(5, 3.5), '') # inicialmente vazio e usado para exibir mensagens de erro
    texto_erro.setFill('red')
    texto_erro.setSize(12)
    texto_erro.draw(win)

    while True:
        click = win.checkMouse()
        key = win.checkKey()

        if key == 'Escape':
            win.close()
            return

        if click and 4 <= click.getX() <= 6 and 1.7 <= click.getY() <= 2.7:
            nome = input_nome.getText().strip()
            valor = input_valor.getText().strip()
            qtd = input_qtd.getText().strip()

            if nome == '':
                texto_erro.setText('O nome não pode ser vazio!') # verifica se o campo nome está vazio
                continue
            try:
                valor = float(valor)
                if valor <= 0:
                    raise ValueError
            except ValueError:
                texto_erro.setText('Valor inválido! Use números positivos.') # verifica se o valor é um número positivo
                continue
            try:
                quantidade = int(qtd)
                if quantidade <= 0:
                    raise ValueError
            except ValueError:
                texto_erro.setText('Quantidade inválida! Use números inteiros.') # verifica se a quantidade é um número inteiro
                continue

            # adiciona o item ao estoque caso nao haja erros
            adicionar_item(nome, valor, quantidade)
            texto_erro.setText('')  # limpa mensagem de erro antes de fechar a janela
            win.close()

            # exibe mensagem de sucesso
            exibir_mensagem('Sucesso','Item cadastrado com sucesso!')
            return

def gerar_lista(): # função para gerar uma lista de itens em html para o usuário
    estoque = ler_estoque()
    file_path = 'generated_list/estoque.html'
    with open(file_path, mode='w') as arq:
        arq.write('''<html><head><title>Estoque</title>\n
            <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #1a1a1a;
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
                color: white;
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
                color: white;
                text-align: center;
                font-size: 24px;
                margin-bottom: 20px;
            }
        </style>\n
        </head><body>\n
        <h1>Estoque</h1>\n
        <table>\n<tr><th>ID</th><th>Nome</th><th>Valor</th><th>Quantidade</th></tr>\n''')

        for item in estoque:
            arq.write(f'<tr><td>{item[0]}</td><td>{item[1]}</td><td>R${float(item[2]):.2f}</td><td>{item[3]}</td></tr>\n')
        arq.write('</table>\n</body></html>')

    # webbrowser para abrir o arquivo html gerado no navegador
    webbrowser.open(f'file://{os.path.abspath(file_path)}')

def janela_realizar_compra():  # função para visualizar e realizar a compra de um item
    estoque = ler_estoque()
    estoque_pesquisado = estoque[:]  # lista filtrada, inicialmente igual ao estoque completo

    def desenhar_pagina(win, pagina):  # função para desenhar a página
        win.delete('all')

        # design do título
        titulo = Text(Point(5, 9.5), f'Comprar - Página {pagina}')
        titulo.setSize(20)
        titulo.setStyle('bold')
        titulo.draw(win)

        # desenhando retângulo para células do cabeçalho
        retangulo_header = Rectangle(Point(0, 8.2), Point(11, 9))
        retangulo_header.setFill('aqua')
        retangulo_header.draw(win)

        # desenhando cabeçalho
        Text(Point(1, 8.6), 'ID').draw(win)
        Text(Point(2.5, 8.6), 'Nome').draw(win)
        Text(Point(4.5, 8.6), 'Valor').draw(win)
        Text(Point(6.8, 8.6), 'Quantidade').draw(win)

        # desenha os itens da página atual
        y = 7.8
        botoes_compra = []

        if pagina == 1:
            itens_pagina = estoque_pesquisado[:10]  # primeiros 10 itens
        else:
            itens_pagina = estoque_pesquisado[10:20]  # itens 11 a 20

        for item in itens_pagina:
            Text(Point(1, y - 0.05), item[0]).draw(win)  # id
            Text(Point(2.5, y - 0.05), item[1]).draw(win)  # nome
            Text(Point(4.5, y - 0.05), f'R${float(item[2]):.2f}').draw(win)  # valor
            Text(Point(6.8, y - 0.05), item[3]).draw(win)  # quantidade

            # botão de compra
            botao_comprar = Rectangle(Point(8.2, y - 0.25), Point(9.3, y + 0.25))
            botao_comprar.setFill('lawn green')
            botao_comprar.draw(win)
            Text(Point(8.75, y), 'Comprar').draw(win)
            botoes_compra.append([botao_comprar, item[0]])  # adiciona o botão e o id do item à lista de botões

            y -= 0.6

        # desenhar botões de navegação
        if pagina == 2:  # botão para página anterior
            botao_anterior = Rectangle(Point(1, 1.2), Point(1.5, 1.8))
            botao_anterior.setFill('lightgray')
            botao_anterior.draw(win)
            Text(botao_anterior.getCenter(), '<').draw(win)

        if pagina == 1:  # botão para próxima página
            botao_proxima = Rectangle(Point(8, 1.2), Point(8.5, 1.8))
            botao_proxima.setFill('lightgray')
            botao_proxima.draw(win)
            Text(botao_proxima.getCenter(), '>').draw(win)

        # Campo de pesquisa
        Text(Point(3.3, 1.5), 'Pesquisar:').draw(win)
        input_pesquisa = Entry(Point(5, 1.5), 20)
        input_pesquisa.draw(win)

        # Botão de pesquisa
        botao_pesquisar = Rectangle(Point(6.2, 1.3), Point(6.7, 1.7))
        botao_pesquisar.setFill('lawn green')
        botao_pesquisar.draw(win)
        Text(botao_pesquisar.getCenter(), '🔎').draw(win)

        return botoes_compra, input_pesquisa

    # cria a janela
    win = criar_janela('Realizar Compra', 800, 600)
    botoes_compra, input_pesquisa = desenhar_pagina(win, 1)  # inicializa na página 1

    while True:
        click = win.checkMouse()
        key = win.checkKey()

        if key == 'Escape':  # fecha a janela ao pressionar esc
            win.close()
            return

        if click:  # verifica cliques para navegação ou ações
            x, y = click.getX(), click.getY()

            # botão para página 1 (anterior)
            if 1 <= x <= 2 and 1.2 <= y <= 1.8:
                botoes_compra, input_pesquisa = desenhar_pagina(win, 1)

            # botão para página 2 (próxima)
            elif 8 <= x <= 9 and 1.2 <= y <= 1.8:
                botoes_compra, input_pesquisa = desenhar_pagina(win, 2)

            # botão de pesquisa
            elif 6.2 <= x <= 6.7 and 1.3 <= y <= 1.7:
                texto_pesquisa = input_pesquisa.getText().strip().lower()
                estoque_pesquisado = []
                for item in estoque:
                    if texto_pesquisa in item[1].lower():
                        estoque_pesquisado.append(item)
                botoes_compra, input_pesquisa = desenhar_pagina(win, 1)  # volta para a página 1

            # botão de compra
            for botao in botoes_compra:
                botao_comprar, item_id = botao
                if botao_comprar.getP1().getX() <= x <= botao_comprar.getP2().getX() and botao_comprar.getP1().getY() <= y <= botao_comprar.getP2().getY():
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
    Text(Point(5, 7), f'Quantos(as) "{item[1]}" deseja comprar?\n(Qtd disponível: {item[3]})').draw(win)
    input_qtd = Entry(Point(5, 5), 10)
    input_qtd.draw(win)

    # botão finalizar
    botao_finalizar = Rectangle(Point(4, 1.1), Point(6, 2.5))
    botao_finalizar.setFill('lawn green')
    botao_finalizar.draw(win)
    Text(Point(5, 1.8), 'Finalizar').draw(win)

    # mensagem para exibir erros, inicialmente vazia
    texto_erro = Text(Point(5, 3.5), '')
    texto_erro.setFill('red')
    texto_erro.setSize(12)
    texto_erro.draw(win)

    while True:
        click = win.checkMouse()
        key = win.checkKey()
        if key == 'Escape':
            win.close()
            return

        # verificação de clique no botão 'finalizar'
        if click and 4 <= click.getX() <= 6 and 1.1 <= click.getY() <= 2.5:
            quantidade = input_qtd.getText().strip()

            # verificação se o campo está vazio ou contém uma quantidade inválida
            if not quantidade:
                texto_erro.setText('O campo de quantidade não pode estar vazio!') # verifica se o campo de quantidade está vazio
                continue
            try:
                quantidade = int(quantidade)
                if quantidade <= 0:
                    texto_erro.setText('A quantidade deve ser maior que zero!') # verifica se a quantidade é maior que zero
                    continue
            except ValueError:
                texto_erro.setText('A quantidade deve ser um número inteiro válido!') # verifica se a quantidade é um número inteiro
                continue
            if quantidade > int(item[3]):
                texto_erro.setText('Quantidade insuficiente para a compra!') # verifica se a quantidade é maior que a disponível
                continue

            # atualiza o estoque com a quantidade diminuída
            nova_qtd = int(item[3]) - quantidade
            item[3] = nova_qtd
            atualizar_estoque(estoque) # atualiza o estoque no csv
            win.close()
            exibir_mensagem('Sucesso', 'Compra realizada com sucesso!') # abre nova janela com mensagem de sucesso
            return

def lista_pendencias():
    estoque = ler_estoque()
    pendencias = []

    for item in estoque:
        if int(item[3]) == 0:
            pendencias.append(item)

    win = criar_janela('Lista de Pendências', 800, 600)
    win.delete('all')

    # design do título
    titulo = Text(Point(5, 9.5), 'Itens Esgotados')
    titulo.setSize(20)
    titulo.setStyle('bold')
    titulo.draw(win)

    # desenhando retângulo para células do cabeçalho
    retangulo_header = Rectangle(Point(0, 8.2), Point(11, 9))
    retangulo_header.setFill('aqua')
    retangulo_header.draw(win)

    # cabeçalho
    Text(Point(1, 8.6), 'ID').draw(win)
    Text(Point(2.5, 8.6), 'Nome').draw(win)
    Text(Point(4.5, 8.6), 'Valor').draw(win)
    Text(Point(6.8, 8.6), 'Quantidade').draw(win)

    y = 7.8
    botoes_repor = []
    botoes_excluir = []
    for item in pendencias:
        Text(Point(1, y), item[0]).draw(win)
        Text(Point(2.5, y), item[1]).draw(win)
        Text(Point(4.5, y), f'R${float(item[2]):.2f}').draw(win)
        Text(Point(6.8, y), item[3]).draw(win)

        # botão de "Repor"
        botao_repor = Rectangle(Point(8.1, y - 0.25), Point(8.7, y + 0.25))
        botao_repor.setFill('lawn green')
        botao_repor.draw(win)
        Text(Point(8.4, y), 'Repor').draw(win)
        botoes_repor.append([botao_repor, item[0]])

        # botão de "Excluir"
        botao_excluir = Rectangle(Point(8.8, y - 0.25), Point(9.4, y + 0.25))
        botao_excluir.setFill('red')
        botao_excluir.draw(win)
        Text(Point(9.1, y), 'Excluir').draw(win)
        botoes_excluir.append([botao_excluir, item[0]])

        y -= 0.6

    while True:
        click = win.checkMouse()
        key = win.checkKey()

        if key == 'Escape':
            win.close()
            return

        if click:
            x, y = click.getX(), click.getY()

            # atribui o id do item ao botão de repor e caso seja clicado, chama a função repor_item
            for botao_repor in botoes_repor:
                item_id = botao_repor[1]
                if botao_repor[0].getP1().getX() <= x <= botao_repor[0].getP2().getX() and botao_repor[0].getP1().getY() <= y <= botao_repor[0].getP2().getY():
                    win.close()
                    repor_item(item_id)
                    return

            # atribui o id do item ao botão de excluir e caso seja clicado, chama a função excluir_item
            for botao_excluir in botoes_excluir:
                item_id = botao_excluir[1]
                if botao_excluir[0].getP1().getX() <= x <= botao_excluir[0].getP2().getX() and botao_excluir[0].getP1().getY() <= y <= botao_excluir[0].getP2().getY():
                    win.close()
                    excluir_item(item_id)
                    return

def repor_item(item_id):  # função para repor a quantidade de um item
    estoque = ler_estoque()

    for i in estoque:  # for para percorrer o estoque e encontrar o item com o id correspondente
        if i[0] == item_id:
            item = i
            break

    win = criar_janela('Repor Quantidade', 400, 200)
    Text(Point(5, 7), f'Quantas unidades deseja repor de {item[1]}?').draw(win)
    input_qtd = Entry(Point(5, 5), 10)
    input_qtd.draw(win)

    # botão finalizar
    botao_finalizar = Rectangle(Point(4, 1.1), Point(6, 2.5))
    botao_finalizar.setFill('lawn green')
    botao_finalizar.draw(win)
    Text(Point(5, 1.8), 'Finalizar').draw(win)

    # mensagem para exibir erros, inicialmente vazia
    texto_erro = Text(Point(5, 3.5), '')
    texto_erro.setFill('red')
    texto_erro.setSize(12)
    texto_erro.draw(win)

    while True:
        click = win.checkMouse()
        key = win.checkKey()
        if key == 'Escape':
            win.close()
            return

        # verificação de clique no botão 'finalizar'
        if click and 4 <= click.getX() <= 6 and 1.1 <= click.getY() <= 2.5:
            quantidade = input_qtd.getText().strip()

            # verificação se o campo está vazio ou contém uma quantidade inválida
            if not quantidade:
                texto_erro.setText('O campo de quantidade não pode estar vazio!')  # verifica se o campo de quantidade está vazio
                continue
            try:
                quantidade = int(quantidade)
                if quantidade <= 0:
                    texto_erro.setText('A quantidade deve ser maior que zero!')  # verifica se a quantidade é maior que zero
                    continue
            except ValueError:
                texto_erro.setText('A quantidade deve ser um número inteiro válido!')  # verifica se a quantidade é um número inteiro
                continue

            # atualiza o estoque com a quantidade reposta
            nova_qtd = int(item[3]) + quantidade
            item[3] = nova_qtd
            atualizar_estoque(estoque)  # atualiza o estoque no csv
            win.close()
            exibir_mensagem('Sucesso', 'Quantidade reposta com sucesso!')  # abre nova janela com mensagem de sucesso
            return

def excluir_item(item_id):  # função para excluir um item do estoque
    estoque = ler_estoque()

    for i in estoque:  # for para percorrer o estoque e encontrar o item com o id correspondente
        if i[0] == item_id:
            estoque.remove(i)
            break

    atualizar_estoque(estoque)  # atualiza o estoque no csv
    exibir_mensagem('Sucesso', 'Item excluído com sucesso!')  # abre nova janela com mensagem de sucesso

# funçoes principais para navegação

def main(): # função principal de navegação
    # criar janela principal maior
    win = GraphWin('Narrowhead Store', 1300, 700)
    win.setCoords(0, 0, 12, 10)

    # carregar e exibir a imagem do logo no topo
    logo = Image(Point(6, 5), 'media/logo.png')
    logo.draw(win)

    # botão verificar estoque
    botao_verificar = Rectangle(Point(7.75, 8), Point(11.75, 9.2))
    botao_verificar.setFill('grey')
    botao_verificar.draw(win)
    texto_verificar = Text(botao_verificar.getCenter(), 'Verificar Estoque')
    texto_verificar.setSize(18)
    texto_verificar.setStyle('bold')
    texto_verificar.draw(win)

    # botão cadastrar item
    botao_cadastrar = Rectangle(Point(7.75, 6.5), Point(11.75, 7.7))
    botao_cadastrar.setFill('grey')
    botao_cadastrar.draw(win)
    texto_cadastrar = Text(botao_cadastrar.getCenter(), 'Cadastrar Item')
    texto_cadastrar.setSize(18)
    texto_cadastrar.setStyle('bold')
    texto_cadastrar.draw(win)

    # botão gerar lista
    botao_gerar = Rectangle(Point(7.75, 5), Point(11.75, 6.2))
    botao_gerar.setFill('grey')
    botao_gerar.draw(win)
    texto_gerar = Text(botao_gerar.getCenter(), 'Gerar Lista')
    texto_gerar.setSize(18)
    texto_gerar.setStyle('bold')
    texto_gerar.draw(win)

    # botão realizar compra
    botao_comprar = Rectangle(Point(7.75, 3.5), Point(11.75, 4.7))
    botao_comprar.setFill('grey')
    botao_comprar.draw(win)
    texto_comprar = Text(botao_comprar.getCenter(), 'Realizar Compra')
    texto_comprar.setSize(18)
    texto_comprar.setStyle('bold')
    texto_comprar.draw(win)

    # botao lista de pendencias
    botao_buscar = Rectangle(Point(7.75, 2), Point(11.75, 3.2))
    botao_buscar.setFill('grey')
    botao_buscar.draw(win)
    texto_buscar = Text(botao_buscar.getCenter(), 'Lista Pendencias')
    texto_buscar.setSize(18)
    texto_buscar.setStyle('bold')
    texto_buscar.draw(win)

   # loop principal para interação
    while not win.isClosed():
        click = win.checkMouse()
        if click:
            x = click.getX()
            y = click.getY()
            if 7.75 <= x <= 11.75 and 8 <= y <= 9.2: # verifica se o clique foi feito dentro do botão 'Verificar Estoque'
                janela_verificar_estoque()
            elif 7.75 <= x <= 11.75 and 6.5 <= y <= 7.7: # verifica se o clique foi feito dentro do botão 'Cadastrar Item'
                janela_cadastrar_item()
            elif 7.75 <= x <= 11.75 and 5 <= y <= 6.2: # verifica se o clique foi feito dentro do botão 'Gerar Lista'
                gerar_lista()
            elif 7.75 <= x <= 11.75 and 3.5 <= y <= 4.7: # verifica se o clique foi feito dentro do botão 'Realizar Compra'
                janela_realizar_compra()
            elif 7.75 <= x <= 11.75 and 2 <= y <= 3.2: # verifica se o clique foi feito dentro do botão 'Lista Pendencias'
                lista_pendencias()

if __name__ == '__main__': # chama a função main
    main()