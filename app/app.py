import streamlit as st
import requests
import json

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
    if item["descricao"] not in carrinho.keys():
        carrinho[item["descricao"]] = {"quantidade": 1, "valor_item": item["valor_item"]}
    else:
        carrinho[item["descricao"]]["quantidade"] += 1

def initialize_data():
    if 'carrinho' not in st.session_state:
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
        body = {'query': 'query MyQuery { app_sessoes {  data_sessao  dia_da_semana  tempo_final  tempo_inicio  total_vendido  valor_inteira  filme {   nome   atores_principais   categoria   censura   descricao  }  ingressos {   assento  } }}'}
        session = requests.post(ENDPOINT, json=body, headers=headers)

        body = {'query': 'query MyQuery { app_itens {  descricao  valor_item }}'}
        items = requests.post(ENDPOINT, json=body, headers=headers)

        col1, col2 = st.columns(2)

        col1.subheader('Ingressos')
        col1.code(json.dumps(session.json()['data']['app_sessoes'], indent=2))

        col2.subheader('Lanchonete')
        col2.code(itemsStr(items.json()['data']['app_itens']))
        selected_item = col2.selectbox('Escolha um lanche', [item['descricao'] for item in items.json()['data']['app_itens']])
        if col2.button('Adicionar ao Carrinho'):
            for index, item in enumerate(items.json()['data']['app_itens']):
                if selected_item == item["descricao"]:
                    addToCarrinho(item, st.session_state.carrinho)

        col2.subheader('Carrinho')
        col2.code(getCarrinho(st.session_state.carrinho))

        if col2.button('Fazer checkout'):
            st.session_state.page = "checkout"

    elif st.session_state.page == "checkout":

        st.subheader('Preencher informações de compra')

        if st.button('Voltar para compras'):
            st.session_state.page = "compras"
        
        with st.form("my_form"):
            col1, col2 = st.columns(2)
            
            nome = col1.text_input(label='nome')
            CPF = col1.text_input(label='CPF')
            telefone = col1.text_input(label='telefone')
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
    print('abc')