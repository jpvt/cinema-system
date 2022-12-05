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

st.title("Cinema Sauro")

st.sidebar.title("Telas")
select = st.sidebar.selectbox('Escolha a tela que deseja visualizar:', ["Loja","Gerenciamento"])

match select:
    case "Loja":
        body = {'query': 'query MyQuery { app_sessoes {  data_sessao  dia_da_semana  tempo_final  tempo_inicio  total_vendido  valor_inteira  filme {   nome   atores_principais   categoria   censura   descricao  }  ingressos {   assento  } }}'}
        session = requests.post(ENDPOINT, json=body, headers=headers)

        body = {'query': 'query MyQuery { app_itens {  descricao  valor_item }}'}
        items = requests.post(ENDPOINT, json=body, headers=headers)

        col1, col2, col3 = st.columns(3)

        col1.subheader('Ingressos')
        col1.code(json.dumps(session.json()['data']['app_sessoes'], indent=2))
        col1.code('''# Magic commands implicitly `st.write()`
    \'\'\' _This_ is some __Markdown__ \'\'\'
    a=3
    'dataframe:', data
        ''')

        col2.subheader('Lanchonete')
        col2.code(itemsStr(items.json()['data']['app_itens']))
        col2.selectbox('Escolha um lanche', [item['descricao'] for item in items.json()['data']['app_itens']])
        col2.button('Adicionar ao Carrinho')

        col3.subheader('Carrinho')
        col3.code('''# Magic commands implicitly `st.write()`
    \'\'\' _This_ is some __Markdown__ \'\'\'
    a=3
    'dataframe:', data
        ''')
    case "Gerenciamento":
        print('abc')