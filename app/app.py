import streamlit as st
import datetime
import requests
import math

ENDPOINT = 'http://localhost:8080/v1/graphql'
headers = {'x-hasura-admin-secret': 'marceloVaiDar10'}

st.set_page_config(
     page_title='Cinema Sauro',
     layout="wide",
     initial_sidebar_state="collapsed",
)

def itemsStr(obj):
    r = ''
    for item in obj:
        r += f'{item["descricao"]}: R${item["valor_item"]:.2f}\n'
        # r += f'**{item["descricao"]}**: R\${item["valor_item"]:.2f}\\\n'
    return r

# TODO: checar double click dos botões
# TODO: filtrar por dia ou fazer um sort de dia e horário
def getCart(carrinho):
    carrinho_str = ""
    total = 0.0

    for key in carrinho.keys():
        carrinho_str += f"{key:<85}R${carrinho[key]['valor_item']:.2f} (x{carrinho[key]['quantidade']})\n"
        total += carrinho[key]['valor_item'] * carrinho[key]['quantidade']

    if not carrinho.keys():
        carrinho_str += 'Seu carrinho está vazio!\n'

    carrinho_str += f'{"-"*96}\n'
    carrinho_str += f"Total{'':<80}R${total:.2f}"

    return carrinho_str, total

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

def showSeats(occupied, seats, columns = 16):
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
    r += '\n\t\tTELA\n\n'
    r += 'O = Assento livre\n* = Assento ocupado'
    
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
        st.session_state.movie_id = -1

initialize_data()

st.title("Cinema Sauro")

st.sidebar.title("Telas")
select_tela = st.sidebar.selectbox('Escolha a tela que deseja visualizar:', ["Loja","Gerenciamento"])

page = "compras"

match select_tela:
    case 'Loja':
        if st.session_state.page == "compras":
            nl = '\n'
            body = {'query': 'query MyQuery { app_filmes {  sessoes {   id_sessao   data_sessao   dia_da_semana   tempo_inicio   valor_inteira   sala {    capacidade    id_sala   } ingressos { assento } }  nome  id_filme  censura  categoria }}'}
            movies = requests.post(ENDPOINT, json=body, headers=headers)

            body = {'query': 'query MyQuery { app_itens {  descricao  valor_item }}'}
            items = requests.post(ENDPOINT, json=body, headers=headers)

            col1, col2 = st.columns(2)

            col1.subheader('Loja')
            select_mode = col1.selectbox('Para onde deseja ir?', ['Bilheteria', 'Lanchonete'])

            if select_mode == 'Bilheteria':
                col1.subheader("Filmes em cartaz")
                for index, movie in enumerate(movies.json()['data']['app_filmes']):
                    if movie['sessoes'] and (st.session_state.movie_id == -1 or st.session_state.movie_id == movie['id_filme']):
                        # and (st.session_state.movie_id == -1 or st.session_state.movie_id == movie['id_filme'])
                        sessions = [f"{session['dia_da_semana']}, dia {datetime.datetime.strptime(session['data_sessao'], '%Y-%m-%d'):%d/%m/%Y} às {session['tempo_inicio']}" for session in movie['sessoes']]

                        movie_info = f'{movie["nome"]}\n{"-"*64}\n'
                        movie_info += f'Censura: {movie["censura"]}\n'
                        movie_info += f'Gênero: {movie["categoria"]}\n'
                        movie_info += 'Horários da sessão:\n\t'
                        movie_info += '\n\t'.join(sessions)
                        movie_info += f'\nPreço inteira: R${movie["sessoes"][0]["valor_inteira"]:.2f}'
                        col1.code(movie_info)

                        if st.session_state.movie_id != movie['id_filme'] and col1.button('Detalhes', key=f'c_{index}'):
                            st.session_state.movie_id = movie['id_filme']

                        if movie['id_filme'] == st.session_state.movie_id:
                            if col1.button('Voltar', key=f'v_{index}'):
                                st.session_state.movie_id = -1

                            session = col1.selectbox('Sessão', sessions, key=f's_{index}')
                            session_idx = sessions.index(session)
                            qnt = col1.number_input('Quantidade', key=f'q_{index}', format="%d", step=1, min_value=0, max_value=5)

                            if qnt:
                                selected_tickets = []
                                for i in range(qnt):
                                    selected_tickets.append(col1.selectbox(f'Tipo de ingresso - Ingresso {i+1}', key=f't_{i}_{index}', options=["Adulto", "Estudante", "Infantil", "Idoso", "Flamenguista"]))
                                    
                                occupied = [ticket['assento'] for ticket in movie['sessoes'][session_idx]['ingressos']]
                                capacity = movie['sessoes'][session_idx]['sala']['capacidade']

                                col1.code(showSeats(occupied, capacity))
                                # for i in range(qnt):


                                if st.button("Adicionar ao carrinho"):
                                    # checa se satisfaz a capacidade
                                    for category in selected_tickets:
                                        descricao = f"{movie['nome']} - {datetime.datetime.strptime(movie['sessoes'][session_idx]['data_sessao'], '%Y-%m-%d'):%d/%m/%Y} às {movie['sessoes'][session_idx]['tempo_inicio'][0:2]}h - {category}"
                                        valor = movie["sessoes"][session_idx]["valor_inteira"]
                                        match category: 
                                            case "Flamenguista":
                                                valor = 0.0
                                            case "Adulto":
                                                pass
                                            case "Infantil":
                                                valor *= 0.25
                                            case _:
                                                valor *= 0.5

                                        addToCart({"descricao": f"{descricao}", "valor_item": valor}, st.session_state.carrinho)
                                        st.session_state.movie_id = -1

            elif select_mode == "Lanchonete":
                col1.subheader('Lanchonete')
                col1.code(itemsStr(items.json()['data']['app_itens']))
                selected_item = col1.selectbox('Não perca a oportunidade, adicione um lanche ao seu pedido!', [item['descricao'] for item in items.json()['data']['app_itens']])
                if col1.button('Adicionar ao Carrinho'):
                    for index, item in enumerate(items.json()['data']['app_itens']):
                        if selected_item == item["descricao"]:
                            addToCart(item, st.session_state.carrinho)

            col2.subheader('Carrinho')
            col2.code(getCart(st.session_state.carrinho)[0])

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
            
            with st.form("form_checkout"):
                col1, col2 = st.columns(2)
                
                nome = col1.text_input(label='Nome')
                cpf = col1.text_input(label='CPF')
                telefone = col1.text_input(label='Telefone')
                forma_de_pagamento = col1.selectbox(label="Forma de pagamento", options=["crédito", "débito", "dinheiro", "pix"])

                # Every form must have a submit button.

                col2.subheader('Carrinho')
                
                cart_str, cart_total = getCart(st.session_state.carrinho)
                col2.code(cart_str)

                submitted = col2.form_submit_button("Finalizar compra")
                if submitted:
                    # UPSERT CLIENTE
                    print(nome, cpf, telefone)
                    upsert_query = f'''mutation upsert_clientes {{
                    insert_app_clientes_one(object: {{id_cliente: "{cpf}", nome: "{nome}", telefone: "{telefone}"}}, on_conflict: {{constraint: clientes_pkey, update_columns: [nome, telefone]}}) {{
                        id_cliente
                        nome
                        telefone
                    }}
                    }}'''

                    print(upsert_query)
                    clientes = requests.post(ENDPOINT, json={'query': upsert_query}, headers=headers)
                    print(clientes.json())

                    # INSERT COMPRA
                    insert_query = f'''mutation unnamedMutation3 {{
                    insert_app_compras_one(object: {{id_cliente: "{cpf}", tipo_pagamento: "{forma_de_pagamento}", valor_total: {cart_total}}}) {{
                        id_compra
                        id_cliente
                        tipo_pagamento
                        valor_total
                    }}
                    }}'''

                    print(insert_query)
                    compras = requests.post(ENDPOINT, json={'query': insert_query}, headers=headers)
                    print(compras.json())
                    
                    st.session_state.customer_data = {"nome": nome, "CPF": cpf, "telefone": telefone}
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
                        print('Query: ', delete_query)
                        movies = requests.post(ENDPOINT, json={'query': delete_query}, headers=headers)
                        print('Response: ', movies.json())
                        

                col2.subheader('Cadastro de Filme')
                form = col2.form("form_cadastro_filme", True)     
                nome = form.text_input(label='Nome')
                categoria = form.text_input(label='Categoria')
                censura = form.text_input(label='Censura')
                atores_principais = form.text_input(label='Atores Principais')
                duracao = form.text_input(label='Duração')
                produtora = form.text_input(label='Produtora')
                nacional = form.selectbox(label="Nacional?", options=["true", "false"])
                descricao = form.text_input(label='Descrição')

                submitted = form.form_submit_button("Finalizar Cadastro")
                if submitted:
                    insert_query = f'''mutation unnamedMutation3 {{
                    insert_app_filmes_one(object: {{nome: "{nome}", categoria: "{categoria}", censura: "{censura}", atores_principais: "{atores_principais}", duracao: "{duracao}", produtora: "{produtora}", nacional: {nacional}, descricao: "{descricao}"}}) {{
                        nome
                        produtora
                        nacional
                        id_filme
                        duracao
                        descricao
                        censura
                        categoria
                        atores_principais
                    }}
                    }}'''

                    print(insert_query)
                    movies = requests.post(ENDPOINT, json={'query': insert_query}, headers=headers)
                    print(movies.json())

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
                        delete_query = f'mutation unnamedMutation3 {{ {table}(id_sessao: {sessao["id_sessao"]}) {{ id_sessao}} }}'
                        print(delete_query)
                        movies = requests.post(ENDPOINT, json={'query': delete_query}, headers=headers)
                        print(movies.json())

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
                    table = 'insert_app_sessoes'
                    insert_query = 'mutation unnamedMutation3 {'
                    insert_query += f'{table}('
                    insert_query += 'objects: {'
                    insert_query += f'id_sala: {id_sala},'
                    insert_query += f'id_filme: {id_filme},'
                    insert_query += f'total_vendido: {total_vendido},'
                    insert_query += f'data_sessao: "{data_sessao}",'
                    insert_query += f'dia_da_semana: "{dia_da_semana}",'
                    insert_query += f'tempo_inicio: "{tempo_inicio}",'
                    insert_query += f'tempo_final: "{tempo_final}",'
                    insert_query += f'valor_inteira: {valor_inteira},'
                    insert_query += '}'
                    insert_query += ')'
                    insert_query += '{'
                    insert_query += 'returning {'
                    insert_query += 'id_sala,'
                    insert_query += 'id_filme,'
                    insert_query += 'total_vendido,'
                    insert_query += 'dia_da_semana,'
                    insert_query += 'tempo_inicio,'
                    insert_query += 'tempo_final,'
                    insert_query += 'valor_inteira,'
                    insert_query += '}'
                    insert_query += '}'
                    insert_query += '}'
                    print(insert_query)
                    movies = requests.post(ENDPOINT, json={'query': insert_query}, headers=headers)
                    print(movies.json())
