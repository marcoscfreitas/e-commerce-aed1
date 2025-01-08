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
        arq.write('<table>\n<tr><th>ID</th><th>Nome</th><th>Valor</th><th>Quantidade</th></tr>\n')

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

def janela_verificar_estoque():  # função para visualizar o estoque disponível
    estoque = ler_estoque()
    itens_por_pagina = 10  # número de itens que cabem em uma página
    pagina_atual = 0  # índice da página atual
    total_paginas = (len(estoque) - 1) // itens_por_pagina + 1  # cálculo do total de páginas

    def desenhar_pagina(win, pagina):
        win.delete('all')  # limpa a janela para redesenhar
        
        # design do título
        titulo = Text(Point(5, 9.5), 'Estoque Atual')
        titulo.setSize(18)
        titulo.setStyle('bold')
        titulo.draw(win)

        # desenhando retângulos para células do cabeçalho
        retangulo_id = Rectangle(Point(0, 8.2), Point(10, 9))  # ID
        retangulo_id.setFill('lightblue')
        retangulo_id.setOutline('lightblue')
        retangulo_id.draw(win)

        # texto para cabeçalho
        Text(Point(1, 8.6), 'ID').draw(win)
        Text(Point(3.5, 8.6), 'Nome').draw(win)
        Text(Point(6, 8.6), 'Valor').draw(win)
        Text(Point(8.5, 8.6), 'Quantidade').draw(win)

        # desenhar itens da página
        inicio = pagina * itens_por_pagina
        fim = inicio + itens_por_pagina
        itens_pagina = estoque[inicio:fim]

        y = 7.8
        for item in itens_pagina:
            Text(Point(1, y - 0.05), item[0]).draw(win)  # id
            Text(Point(3.5, y - 0.05), item[1]).draw(win)  # nome
            Text(Point(6, y - 0.05), f'R${float(item[2]):.2f}').draw(win)  # valor formatado
            Text(Point(8.5, y - 0.05), item[3]).draw(win)  # quantidade
            y -= 0.6

        # desenhar botões de navegação
            botao_esquerda = Text(Point(1, 0.4), '<')
            botao_esquerda.setSize(20)
            botao_esquerda.setStyle('bold')
            botao_esquerda.draw(win)

            botao_direita = Text(Point(9, 0.4), '>')
            botao_direita.setSize(20)
            botao_direita.setStyle('bold')
            botao_direita.draw(win)

    win = criar_janela('Verificar Estoque', 800, 600)

    desenhar_pagina(win, pagina_atual)

    while True:
        clique = win.checkMouse() # Verifica se houve clique
        key = win.checkKey() # Verifica se uma tecla foi pressionada

        if key == 'Escape': # Fecha a janela ao pressionar Escape
            win.close()
            return

        if clique:  # Se um clique ocorreu
            x, y = clique.getX(), clique.getY()
            if 0.5 <= x <= 1.5 and 0.2 <= y <= 0.6 and pagina_atual > 0:  # botão esquerda
                pagina_atual -= 1
                desenhar_pagina(win, pagina_atual)
            elif 8.5 <= x <= 9.5 and 0.2 <= y <= 0.6 and pagina_atual < total_paginas - 1:  # botão direita
                pagina_atual += 1
                desenhar_pagina(win, pagina_atual)
    win.close()

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
    Text(Point(8.8, 8.6), 'Comprar').draw(win)

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

        # verificação de clique no botão 'finalizar'
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
            item[3] = nova_qtd
            escrever_estoque(estoque) # atualiza o estoque no csv
            win.close()
            exibir_mensagem('Sucesso', 'Compra realizada com sucesso!') # abre nova janela com mensagem de sucesso
            return

def lista_pendencias():  # função para visualizar itens zerados
    estoque = ler_estoque()
    pendencias = [item for item in estoque if int(item[3]) == 0]

    win = criar_janela('Lista de Pendências', 800, 600)

    # design do título
    titulo = Text(Point(5, 9.5), 'Itens Esgotados')
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

    retangulo_botao_acao = Rectangle(Point(8.5, 8.2), Point(9.5, 9))  # coluna com botão de repor
    retangulo_botao_acao.setFill('lightblue')
    retangulo_botao_acao.setOutline('lightblue')
    retangulo_botao_acao.draw(win)


    # texto para cabeçalho
    Text(Point(1, 8.6), 'ID').draw(win)
    Text(Point(2.5, 8.6), 'Nome').draw(win)
    Text(Point(4.5, 8.6), 'Valor').draw(win)
    Text(Point(6.8, 8.6), 'Quantidade').draw(win)
    Text(Point(8.8, 8.6), 'Ação').draw(win)

    # linhas da tabela e botões
    y = 7.8
    buttons_repor = []
    buttons_excluir = []
    for item in pendencias:
        Text(Point(1, y-0.05), item[0]).draw(win)  # id
        Text(Point(2.5, y-0.05), item[1]).draw(win)  # nome
        Text(Point(4.5, y-0.05), f'R${float(item[2]):.2f}').draw(win)  # valor
        Text(Point(6.8, y-0.05), item[3]).draw(win)  # quantidade

        # botão de repor
        btn_repor = Rectangle(Point(8.1, y - 0.25), Point(8.7, y + 0.25))
        btn_repor.setFill('yellow green')
        btn_repor.draw(win)
        Text(btn_repor.getCenter(), 'Repor').draw(win)
        buttons_repor.append([btn_repor, item[0]])  # armazena o botão e o id do item

        # botão de excluir
        btn_excluir = Rectangle(Point(8.8, y - 0.25), Point(9.4, y + 0.25))
        btn_excluir.setFill('red')
        btn_excluir.draw(win)
        Text(btn_excluir.getCenter(), 'Excluir').draw(win)
        buttons_excluir.append([btn_excluir, item[0]])  # armazena o botão e o id do item

        y -= 0.6  # diminui y para descer linhaquantas

    while True:
        click = win.checkMouse()
        key = win.checkKey()
        if key == 'Escape':
            win.close()
            return

        for button in buttons_repor:
            btn_repor = button[0]  # armazena o botao para verificar se foi clicado
            item_id = button[1]  # armazena o id do item para enviar para função de repor
            if click and btn_repor.getP1().getX() <= click.getX() <= btn_repor.getP2().getX() and btn_repor.getP1().getY() <= click.getY() <= btn_repor.getP2().getY():  # verifica se o botão foi clicado
                win.close()
                repor_item(item_id)
                return

        for button in buttons_excluir:
            btn_excluir = button[0]  # armazena o botao para verificar se foi clicado
            item_id = button[1]  # armazena o id do item para enviar para função de excluir
            if click and btn_excluir.getP1().getX() <= click.getX() <= btn_excluir.getP2().getX() and btn_excluir.getP1().getY() <= click.getY() <= btn_excluir.getP2().getY():  # verifica se o botão foi clicado
                win.close()
                excluir_item(item_id)
                return

def repor_item(item_id):  # Função para repor a quantidade de um item
    estoque = ler_estoque()

    for i in estoque:  # for para percorrer o estoque e encontrar o item com o id correspondente
        if i[0] == item_id:
            item = i
            break

    win = criar_janela('Repor Quantidade', 400, 200)
    Text(Point(5, 7), f'Quantas unidades deseja repor de {item[1]}?').draw(win)
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

        # verificação de clique no botão 'finalizar'
        if click and 4 <= click.getX() <= 6 and 1.1 <= click.getY() <= 2.5:
            quantidade_text = qtd_entry.getText().strip()

            # verificação se o campo está vazio ou contém uma quantidade inválida
            if not quantidade_text:
                erro_text.setText('O campo de quantidade não pode estar vazio!')  # verifica se o campo de quantidade está vazio
                continue

            try:
                quantidade = int(quantidade_text)
                if quantidade <= 0:
                    erro_text.setText('A quantidade deve ser maior que zero!')  # verifica se a quantidade é maior que zero
                    continue
            except ValueError:
                erro_text.setText('A quantidade deve ser um número inteiro válido!')  # verifica se a quantidade é um número inteiro
                continue

            # atualiza o estoque com a quantidade reposta
            nova_qtd = int(item[3]) + quantidade
            item[3] = nova_qtd
            escrever_estoque(estoque)  # atualiza o estoque no csv
            win.close()
            exibir_mensagem('Sucesso', 'Quantidade reposta com sucesso!')  # abre nova janela com mensagem de sucesso
            return

def excluir_item(item_id):  # Função para excluir um item do estoque
    estoque = ler_estoque()

    for i in estoque:  # for para percorrer o estoque e encontrar o item com o id correspondente
        if i[0] == item_id:
            estoque.remove(i)
            break

    escrever_estoque(estoque)  # atualiza o estoque no csv
    exibir_mensagem('Sucesso', 'Item excluído com sucesso!')  # abre nova janela com mensagem de sucesso
    estoque = ler_estoque()

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
    win = GraphWin('Narrowhead Store', 1300, 700)
    win.setCoords(0, 0, 12, 10)

    # carregar e exibir a imagem do logo no topo
    # logo = Image(Point(6, 6.9), 'media/logo.png')
    # logo.draw(win)

    # botões da primeira linha
    btn_verificar = Rectangle(Point(7.5, 8), Point(11.5, 9.2))
    btn_verificar.setFill('grey')
    btn_verificar.draw(win)
    texto_verificar = Text(btn_verificar.getCenter(), 'Verificar Estoque')
    texto_verificar.setSize(18)
    texto_verificar.setStyle('bold')
    texto_verificar.draw(win)

    btn_cadastrar = Rectangle(Point(7.5, 6.5), Point(11.5, 7.7))
    btn_cadastrar.setFill('grey')
    btn_cadastrar.draw(win)
    texto_cadastrar = Text(btn_cadastrar.getCenter(), 'Cadastrar Peça')
    texto_cadastrar.setSize(18)
    texto_cadastrar.setStyle('bold')
    texto_cadastrar.draw(win)

    # botões da segunda linha
    btn_gerar_lista = Rectangle(Point(7.5, 5), Point(11.5, 6.2))
    btn_gerar_lista.setFill('grey')
    btn_gerar_lista.draw(win)
    texto_gerar_lista = Text(btn_gerar_lista.getCenter(), 'Gerar Lista')
    texto_gerar_lista.setSize(18)
    texto_gerar_lista.setStyle('bold')
    texto_gerar_lista.draw(win)

    btn_comprar = Rectangle(Point(7.5, 3.5), Point(11.5, 4.7))
    btn_comprar.setFill('grey')
    btn_comprar.draw(win)
    texto_comprar = Text(btn_comprar.getCenter(), 'Realizar Compra')
    texto_comprar.setSize(18)
    texto_comprar.setStyle('bold')
    texto_comprar.draw(win)

    # botao lista de pendencias
    btn_buscar_estoque = Rectangle(Point(7.5, 2), Point(11.5, 3.2))
    btn_buscar_estoque.setFill('grey')
    btn_buscar_estoque.draw(win)
    texto_buscar_estoque = Text(btn_buscar_estoque.getCenter(), 'Lista Pendencias')
    texto_buscar_estoque.setSize(18)
    texto_buscar_estoque.setStyle('bold')
    texto_buscar_estoque.draw(win)

   # loop principal para interação
    while not win.isClosed():
        click = win.checkMouse()
        if click:
            x = click.getX()
            y = click.getY()
            if 7.5 <= x <= 11.5 and 8 <= y <= 9.2: # verifica se o clique foi feito dentro do botão 'Verificar Estoque'
                janela_verificar_estoque()
            elif 7.5 <= x <= 11.5 and 6.5 <= y <= 7.7: # verifica se o clique foi feito dentro do botão 'Cadastrar Peça'
                janela_cadastrar_peca()
            elif 7.5 <= x <= 11.5 and 5 <= y <= 6.2: # verifica se o clique foi feito dentro do botão 'Gerar Lista'
                gerar_lista()
            elif 7.5 <= x <= 11.5 and 3.5 <= y <= 4.7: # verifica se o clique foi feito dentro do botão 'Realizar Compra'
                janela_realizar_compra()
            elif 7.5 <= x <= 11.5 and 2 <= y <= 3.2: # verifica se o clique foi feito dentro do botão 'Lista Pendencias'
                lista_pendencias()

if __name__ == '__main__': # chama a função main
    main()