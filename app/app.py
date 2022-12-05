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
        carrinho_str += f"{key} - {carrinho[key]['valor_item']:.2f} - {carrinho[key]['quantidade']}\n"
        total += carrinho[key]['valor_item'] * carrinho[key]['quantidade']
    carrinho_str += f"Total - {total:.2f}"

    return carrinho_str

def addToCarrinho(item, carrinho):
    if item["descricao"] not in carrinho.keys():
        carrinho[item["descricao"]] = {"quantidade": 1, "valor_item": item["valor_item"]}
    else:
        carrinho[item["descricao"]]["quantidade"] += 1

if 'carrinho' not in st.session_state:
    st.session_state.carrinho = {}

st.title("Cinema Sauro")

st.sidebar.title("Telas")
select = st.sidebar.selectbox('Escolha a tela que deseja visualizar:', ["Loja","Gerenciamento"])

if select == "Loja":
        body = {'query': 'query MyQuery { app_sessoes {  data_sessao  dia_da_semana  tempo_final  tempo_inicio  total_vendido  valor_inteira  filme {   nome   atores_principais   categoria   censura   descricao  }  ingressos {   assento  } }}'}
        session = requests.post(ENDPOINT, json=body, headers=headers)

        body = {'query': 'query MyQuery { app_itens {  descricao  valor_item }}'}
        items = requests.post(ENDPOINT, json=body, headers=headers)

        col1, col2, col3 = st.columns(3)

        col1.subheader('Ingressos')
        col1.code(json.dumps(session.json()['data']['app_sessoes'], indent=2))

        col2.subheader('Lanchonete')
        col2.code(itemsStr(items.json()['data']['app_itens']))
        selected_item = col2.selectbox('Escolha um lanche', [item['descricao'] for item in items.json()['data']['app_itens']])
        if col2.button('Adicionar ao Carrinho'):
            for index, item in enumerate(items.json()['data']['app_itens']):
                if selected_item == item["descricao"]:
                    addToCarrinho(item, st.session_state.carrinho)

        col3.subheader('Carrinho')
        col3.code(getCarrinho(st.session_state.carrinho))

elif select == "Gerenciamento":
    print('abc')