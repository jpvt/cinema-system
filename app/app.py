import streamlit as st
import datetime
import requests
import json
import math
# from flask import Flask

# app = Flask(__name__)

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
def getCart(carrinho):
    carrinho_str = ""
    total = 0.0

    for key in carrinho.keys():
        carrinho_str += f"{key:<32}R${carrinho[key]['valor_item']:.2f} (x{carrinho[key]['quantidade']})\n"
        total += carrinho[key]['valor_item'] * carrinho[key]['quantidade']

    if not carrinho.keys():
        carrinho_str += 'Seu carrinho está vazio!\n'

    carrinho_str += f'{"-"*48}\n'
    carrinho_str += f"Total{'':<27}R${total:.2f}"

    return carrinho_str

def addToCart(item, carrinho):
    st.session_state.last_key = item["descricao"]
    if item["descricao"] not in carrinho.keys():
        carrinho[item["descricao"]] = {"quantidade": 1, "valor_item": item["valor_item"]}
    else:
        carrinho[item["descricao"]]["quantidade"] += 1

def undoCart(carrinho):
    if carrinho:
        if carrinho[list(carrinho)[-1]]['quantidade'] == 1:
            del carrinho[list(carrinho)[-1]]
        else:
            carrinho[list(carrinho)[-1]]['quantidade'] -= 1

def clearCart():
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
select_tela = st.sidebar.selectbox('Escolha a tela que deseja visualizar:', ["Loja","Gerenciamento"])

page = "compras"

match select_tela:
    case 'Loja':
        if st.session_state.page == "compras":
            nl = '\n'
            body = {'query': 'query MyQuery { app_filmes {  sessoes {   data_sessao   dia_da_semana   tempo_inicio   valor_inteira   sala {    capacidade    id_sala   }  }  nome  id_filme  censura  categoria }}'}
            movies = requests.post(ENDPOINT, json=body, headers=headers)

            body = {'query': 'query MyQuery { app_itens {  descricao  valor_item }}'}
            items = requests.post(ENDPOINT, json=body, headers=headers)

            col1, col2 = st.columns(2)

            col1.subheader('Loja')
            select_mode = col1.selectbox('Para onde deseja ir?', ['Bilheteria', 'Lanchonete'])

            if select_mode == 'Bilheteria':
                col1.subheader("Filmes em cartaz")
                for index, movie in enumerate(movies.json()['data']['app_filmes']):
                    movie_info = f'{movie["nome"]}\n{"-"*64}\n'
                    movie_info += f'Censura: {movie["censura"]}\n'
                    movie_info += f'Gênero: {movie["categoria"]}\n'
                    movie_info += 'Horários da sessão:\n\t'
                    movie_info += '\n\t'.join([f"{session['dia_da_semana']}, dia {datetime.datetime.strptime(session['data_sessao'], '%Y-%m-%d'):%d/%m/%Y} às {session['tempo_inicio']}" for session in movie['sessoes']])
                    movie_info += f'\nPreço inteira: R${movie["sessoes"][0]["valor_inteira"]:.2f}'
                    col1.code(movie_info)

                    if col1.button('Comprar', key=f'c_{index}'):
                        # print(movies.json()['data']['app_filmes'][index])
                        # print('oi')
                        col1.number_input('Quantidade', key=f'q_{index}', format="%d", step=1, min_value=0, max_value=5)
                        col1.selectbox('Sessão', [f"{session['dia_da_semana']}, dia {datetime.datetime.strptime(session['data_sessao'], '%Y-%m-%d'):%d/%m/%Y} às {session['tempo_inicio']}" for session in movie['sessoes']], key=f's_{index}')
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
                            addToCart(item, st.session_state.carrinho)

            col2.subheader('Carrinho')
            col2.code(getCart(st.session_state.carrinho))

            if col2.button('Fazer checkout'):
                st.session_state.page = "checkout"
            if col2.button('Desfazer'):
                undoCart(st.session_state.carrinho)
            if col2.button('Limpar Carrinho'):
                clearCart()
                

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
                col2.code(getCart(st.session_state.carrinho))

                submitted = col2.form_submit_button("Finalizar compra")
                if submitted:
                    print(nome, CPF, telefone)
                    st.session_state.customer_data = {"nome": nome, "CPF": CPF, "telefone": telefone}
                    st.session_state.page = "thank_you"

        elif st.session_state.page == "thank_you":
            st.subheader(f"Obrigado por comprar conosco, {st.session_state.customer_data['nome']}!")
            if st.button('Fazer nova compra'):
                st.session_state.page = "compras"

    case "Gerenciamento":
        select_mode = st.selectbox('Que modo de gerenciamento deseja utilizar?', ['Filmes', 'Sessões'])

        match select_mode:
            case 'Filmes':
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
                    if col1.button('Remover', key=f's_{index}'):
                        print(f"Removendo {movie['id_filme']} - {movie['nome']}")
                        table = 'delete_app_filmes_by_pk'
                        delete_query = 'mutation unnamedMutation3 {'
                        delete_query += f'{table}('
                        delete_query += f'id_filme: {movie["id_filme"]}'
                        delete_query += ')'
                        delete_query += '{'
                        delete_query += 'id_filme'
                        delete_query += '}'
                        delete_query += '}'
                        movies = requests.post(ENDPOINT, json=delete_query, headers=headers)
                        print(delete_query)
                        

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

            case 'Sessões':
                col1, col2 = st.columns(2)
                col1.subheader('Sessões Cadastradas')

                body = {'query': 'query MyQuery { app_sessoes { id_sessao data_sessao  dia_da_semana  tempo_final  tempo_inicio  total_vendido  valor_inteira  filme {   nome   atores_principais   categoria   censura   descricao  } sala { capacidade   id_sala  } }}'}
                sessions = requests.post(ENDPOINT, json=body, headers=headers)

                for index, sessao in enumerate(sessions.json()['data']['app_sessoes']):
                    col1.code(f'''{sessao['id_sessao']} - {sessao['filme']['nome']}
            Censura: {sessao['filme']['censura']} 
            Gênero: {sessao['filme']['categoria']}
            Horário da sessão: {sessao['dia_da_semana']} | {datetime.datetime.strptime(sessao['data_sessao'], '%Y-%m-%d'):%d/%m/%Y} | {sessao['tempo_inicio']}
            Preço inteira: {sessao['valor_inteira']}
                    ''')
                    if col1.button('Remover', key=f's_{index}'):
                        #TODO Query to delete this session
                        print(f"Removendo {sessao['id_sessao']} - {sessao['filme']['nome']}")
                        table = 'delete_app_sessoes_by_pk'
                        delete_query = 'mutation unnamedMutation3 {'
                        delete_query += f'{table}('
                        delete_query += f'id_sessao: {sessao["id_sessao"]}'
                        delete_query += ')'
                        delete_query += '{'
                        delete_query += 'id_sessao'
                        delete_query += '}'
                        delete_query += '}'
                        movies = requests.post(ENDPOINT, json=delete_query, headers=headers)
                        print(delete_query)

                col2.subheader('Cadastro de Sessão')
                form = col2.form("form_cadastro_sessao", True)     
                id_sala = form.number_input('ID da Sala', key=f'q_sala', format="%d", step=1, min_value=0)
                id_filme = form.number_input('ID do Filme', key=f'q_filme', format="%d", step=1, min_value=0)
                total_vendido = form.number_input(label='Total Vendido', key=f'q_vendido', format="%d", step=1, min_value=0)
                data_sessao = form.date_input(label='Data da Sessão (Dia/Mês/Ano)')
                dia_da_semana = form.text_input(label='Dia da Semana (e.g. Segunda-feira)')
                tempo_inicio = form.time_input(label='Horário de início da sessão')
                tempo_final = form.time_input(label='Horário de fim da sessão')
                valor_inteira = form.number_input(label='Valor da Inteira', key=f'q_valor', format="%f", step=1.0, min_value=0.0)

                submitted = form.form_submit_button("Finalizar Cadastro")
                if submitted:
                    new_session = {
                        'id_sala': id_sala,
                        'id_filme': id_filme,
                        'total_vendido': total_vendido,
                        'data_sessao': data_sessao,
                        'dia_da_semana': dia_da_semana,
                        'tempo_inicio': tempo_inicio,
                        'tempo_final': tempo_final,
                        'valor_inteira': valor_inteira
                    }
                    print('Nova Sessão: ', new_session)