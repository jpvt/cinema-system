import streamlit as st
import datetime
import requests
import json
import math

ENDPOINT = 'http://localhost:8080/v1/graphql'
headers = {'x-hasura-admin-secret': 'marceloVaiDar10'}

def itemsStr(obj):
    r = ''
    for item in obj:
        r += f'{item["descricao"]}: R${item["valor_item"]:.2f}\n'
        # r += f'**{item["descricao"]}**: R\${item["valor_item"]:.2f}\\\n'
    return r

st.set_page_config(
     page_title='Cinema Sauro',
     layout="wide",
     initial_sidebar_state="collapsed",
)

# TODO: checar double click dos botões
# TODO: filtrar por dia ou fazer um sort de dia e horário
def getCarrinho(carrinho):
    carrinho_str = ""
    total = 0.0
    print(carrinho)
    for key in carrinho.keys():
        carrinho_str += f"{key} - R${carrinho[key]['valor_item']:.2f} - {carrinho[key]['quantidade']}\n"
        total += carrinho[key]['valor_item'] * carrinho[key]['quantidade']
    carrinho_str += f"Total - R${total:.2f}"

    return carrinho_str

def addToCarrinho(item, carrinho):
    st.session_state.last_key = item["descricao"]
    if item["descricao"] not in carrinho.keys():
        carrinho[item["descricao"]] = {"quantidade": 1, "valor_item": item["valor_item"]}
    else:
        carrinho[item["descricao"]]["quantidade"] += 1

def undoCarrinho(carrinho):
    if carrinho:
        if carrinho[list(carrinho)[-1]]['quantidade'] == 1:
            del carrinho[list(carrinho)[-1]]
        else:
            carrinho[list(carrinho)[-1]]['quantidade'] -= 1
    # if st.session_state.last_key in carrinho.keys():
    #     carrinho.remove(st.session_state.last_key)

def clearCarrinho():
    st.session_state.carrinho = {}

def show_seats(occupied, seats, columns = 16):
    r = '\\  '
    rows = seats//columns
    for i in range(columns):
        r += f'{i+1} '
    r += '\n'
    for i in range(rows):
        char = chr(ord("A")+(rows-(i+1)))
        r += f'{char}. '
        for j in range(columns):
            r += '*' if f'{char}{j+1}' in occupied else 'O'
            r += ' '*(math.floor(math.log(j+1,10))+1)
        r += '\n'
    r += '\n\t\tTELA'
    
    return r

def tipo_de_ingresso(movie_id):
    print('1. Adulto')
    print('2. Estudante')
    print('3. Infantil')
    print('4. Idoso')
    print('5. Flamenguista')

def initialize_data():
    if 'carrinho' not in st.session_state:
        st.session_state.last_key = ""
        st.session_state.customer_data = {}
        st.session_state.carrinho = {}
        st.session_state.page = "compras"

initialize_data()

st.title("Cinema Sauro")

st.sidebar.title("Telas")
select = st.sidebar.selectbox('Escolha a tela que deseja visualizar:', ["Loja","Gerenciamento"])

page = "compras"

if select == "Loja":
    if st.session_state.page == "compras":
        body = {'query': 'query MyQuery { app_sessoes {  data_sessao  dia_da_semana  tempo_final  tempo_inicio  total_vendido  valor_inteira  filme {   nome   atores_principais   categoria   censura   descricao  }  ingressos {  assento  }  sala { capacidade   id_sala  } }}'}
        sessions = requests.post(ENDPOINT, json=body, headers=headers)

        body = {'query': 'query MyQuery { app_itens {  descricao  valor_item }}'}
        items = requests.post(ENDPOINT, json=body, headers=headers)

        col1, col2 = st.columns(2)

        col1.subheader('Loja')
        select_mode = col1.selectbox('Para onde deseja ir?', ['Bilheteria', 'Lanchonete'])

        if select_mode == 'Bilheteria':
            col1.subheader("Filmes em cartaz")
            for index, sessao in enumerate(sessions.json()['data']['app_sessoes']):
                col1.code(f'''{sessao['filme']['nome']}
        Censura: {sessao['filme']['censura']} 
        Gênero: {sessao['filme']['categoria']}
        Horário da sessão: {sessao['dia_da_semana']} | {datetime.datetime.strptime(sessao['data_sessao'], '%Y-%m-%d'):%d/%m/%Y} | {sessao['tempo_inicio']}
        Preço inteira: {sessao['valor_inteira']}
                ''')
                col1.number_input('Quantidade', key=f'q_{index}', format="%d", step=1, min_value=0, max_value=5)
                if col1.button('Continuar', key=f'c_{index}'):
                    print('oi')
                    pass

        # col1.code(show_seats([ticket['assento'] for ticket in sessions.json()['data']['app_sessoes'][1]['ingressos']], sessions.json()['data']['app_sessoes'][1]['sala']['capacidade']))
        # col1.code(json.dumps(sessions.json()['data']['app_sessoes'], indent=2))
        elif select_mode == "Lanchonete":
            col1.subheader('Lanchonete')
            col1.code(itemsStr(items.json()['data']['app_itens']))
            selected_item = col1.selectbox('Não perca a oportunidade, adicione um lanche ao seu pedido!', [item['descricao'] for item in items.json()['data']['app_itens']])
            if col1.button('Adicionar ao Carrinho'):
                for index, item in enumerate(items.json()['data']['app_itens']):
                    if selected_item == item["descricao"]:
                        addToCarrinho(item, st.session_state.carrinho)

        col2.subheader('Carrinho')
        col2.code(getCarrinho(st.session_state.carrinho))

        if col2.button('Fazer checkout'):
            st.session_state.page = "checkout"
        if col2.button('Desfazer'):
            undoCarrinho(st.session_state.carrinho)
        if col2.button('Limpar Carrinho'):
            clearCarrinho()
            

    elif st.session_state.page == "checkout":

        st.subheader('Preencher informações de compra')

        if st.button('Voltar para compras'):
            st.session_state.page = "compras"
        
        with st.form("my_form"):
            col1, col2 = st.columns(2)
            
            nome = col1.text_input(label='Nome')
            CPF = col1.text_input(label='CPF')
            telefone = col1.text_input(label='Telefone')
            forma_de_pagamento = col1.selectbox(label="Forma de pagamento", options=["crédito", "débito", "dinheiro", "pix"])

            # Every form must have a submit button.

            col2.subheader('Carrinho')
            col2.code(getCarrinho(st.session_state.carrinho))

            submitted = col2.form_submit_button("Finalizar compra")
            if submitted:
                print(nome, CPF, telefone)
                st.session_state.customer_data = {"nome": nome, "CPF": CPF, "telefone": telefone}
                st.session_state.page = f"thank_you"

    elif st.session_state.page == "thank_you":
        st.subheader(f"Obrigado por comprar conosco, {st.session_state.customer_data['nome']}!")
        if st.button('Fazer nova compra'):
            st.session_state.page = "compras"

elif select == "Gerenciamento":
    select_mode = st.selectbox('Que modo de gerenciamento deseja utilizar?', ['Adicionar Filmes','Remover Filmes', 'Adicionar Sessões', 'Remover Sessões'])

    if select_mode == 'Adicionar Filmes':
        col1, col2 = st.columns(2)
        
        col1.subheader('Filmes Cadastrados')
        body = {'query': 'query MyQuery { app_filmes {  id_filme  nome   atores_principais   categoria   censura duracao produtora nacional descricao }}'}
        movies = requests.post(ENDPOINT, json=body, headers=headers)
        for index, movie in enumerate(movies.json()['data']['app_filmes']):
            col1.code(f'''{movie['id_filme']} - {movie['nome']}
    Censura: {movie['censura']} 
    Gênero: {movie['categoria']}
    atores_principais: {movie['atores_principais']}
    duracao: {movie['duracao']}
    produtora: {movie['produtora']}
    nacional: {movie['nacional']}
    descricao: {movie['descricao']}
            ''')

        col2.subheader('Cadastro de Filme')
        form = col2.form("form_cadastro_filme", True)     
        nome = form.text_input(label='Nome')
        categoria = form.text_input(label='Categoria')
        censura = form.text_input(label='Censura')
        atores_principais = form.text_input(label='Atores Principais')
        duracao = form.text_input(label='Duração')
        produtora = form.text_input(label='Produtora')
        nacional = form.selectbox(label="Nacional?", options=["True", "False"])
        descricao = form.text_input(label='Descrição')

        submitted = form.form_submit_button("Finalizar Cadastro")
        if submitted:
            new_movie = {
                'nome': nome,
                'categoria': categoria,
                'censura': censura,
                'atores_principais': atores_principais,
                'duracao': duracao,
                'produtora': produtora,
                'nacional': nacional,
                'descricao': descricao
            }
            print('Novo filme: ', new_movie)

    elif select_mode == 'Remover Filmes':
        st.subheader('Filmes Cadastrados')

        body = {'query': 'query MyQuery { app_filmes {  id_filme  nome   atores_principais   categoria   censura duracao produtora nacional descricao }}'}
        movies = requests.post(ENDPOINT, json=body, headers=headers)
        for index, movie in enumerate(movies.json()['data']['app_filmes']):
            st.code(f'''{movie['id_filme']} - {movie['nome']}
    Censura: {movie['censura']} 
    Gênero: {movie['categoria']}
    atores_principais: {movie['atores_principais']}
    duracao: {movie['duracao']}
    produtora: {movie['produtora']}
    nacional: {movie['nacional']}
    descricao: {movie['descricao']}
            ''')

            if st.button('Remover', key=f's_{index}'):
                #TODO Query to delete this movie
                print(f"Removendo {movie['id_filme']} - {movie['nome']}")
                pass

    elif select_mode == 'Adicionar Sessões':
        col1, col2 = st.columns(2)
        col1.subheader('Sessões Cadastradas')
        col2.subheader('Cadastro de Sessão')

        body = {'query': 'query MyQuery { app_sessoes { id_sessao data_sessao  dia_da_semana  tempo_final  tempo_inicio  total_vendido  valor_inteira  filme {   nome   atores_principais   categoria   censura   descricao  } sala { capacidade   id_sala  } }}'}
        sessions = requests.post(ENDPOINT, json=body, headers=headers)

        for index, sessao in enumerate(sessions.json()['data']['app_sessoes']):
            st.code(f'''{sessao['id_sessao']} - {sessao['filme']['nome']}
    Censura: {sessao['filme']['censura']} 
    Gênero: {sessao['filme']['categoria']}
    Horário da sessão: {sessao['dia_da_semana']} | {datetime.datetime.strptime(sessao['data_sessao'], '%Y-%m-%d'):%d/%m/%Y} | {sessao['tempo_inicio']}
    Preço inteira: {sessao['valor_inteira']}
            ''')

    elif select_mode == 'Remover Sessões':
        st.subheader('Sessões Cadastradas')

        body = {'query': 'query MyQuery { app_sessoes {  id_sessao data_sessao  dia_da_semana  tempo_final  tempo_inicio  total_vendido  valor_inteira  filme {   nome   atores_principais   categoria   censura   descricao  } sala { capacidade   id_sala  } }}'}
        sessions = requests.post(ENDPOINT, json=body, headers=headers)

        for index, sessao in enumerate(sessions.json()['data']['app_sessoes']):
            st.code(f'''{sessao['id_sessao']} - {sessao['filme']['nome']}
    Censura: {sessao['filme']['censura']} 
    Gênero: {sessao['filme']['categoria']}
    Horário da sessão: {sessao['dia_da_semana']} | {datetime.datetime.strptime(sessao['data_sessao'], '%Y-%m-%d'):%d/%m/%Y} | {sessao['tempo_inicio']}
    Preço inteira: {sessao['valor_inteira']}
            ''')

            if st.button('Remover', key=f's_{index}'):
                #TODO Query to delete this session
                print(f"Removendo {sessao['id_sessao']} - {sessao['filme']['nome']}")
                pass

