import streamlit as st
import json
import time
from search import ask

html = '''
<style>
.appview-container .main .block-container{
    padding-top: 0px;
    padding-left: 20px;
    padding-right: 20px;
    padding-bottom: 0px
}
.st-emotion-cache-1y4p8pa{
    max-width: 1200px;
}
</style>
'''
with open('catecismo.json','r',encoding = 'utf-8') as f:
    cat = json.load(f)
    cat = {int(key):cat[key] for key in cat}
last_key = max(cat.keys())

st.set_page_config(page_title='Pergunte ao Catecismo', page_icon='📖')
st.markdown(html,unsafe_allow_html = True)

st.markdown('''<h1 style='text-align: center; font-family: "times-new-roman"'>Pergunte ao Catecismo</h1>''', unsafe_allow_html=True)
tabquest,tabbook,tabsearch = st.tabs(['Pergunte','Texto Completo','Buscar Parágrafos'])
contquest = tabquest.container(height = 430)
prompt = tabquest.chat_input("Faça uma pergunta.")
def word_generator(string):
    def gen():
        for word in string.split():
            yield word + " "
            time.sleep(0.02)
    return gen
if prompt:
    contquest.write(prompt)
    respostas = ask(prompt)
    for resp in respostas:
        contquest.write_stream(word_generator(resp))
tabsearch.number_input('Parágrafo',min_value = 1,max_value = last_key,key = 'paragrafo',step = 5)
contsearch = tabsearch.container(height = 430)
for key in range(st.session_state.paragrafo,min(last_key + 1,st.session_state.paragrafo + 5)):
    contsearch.write(cat[key])
contbook = tabbook.container(height = 500)
for key in cat:
    contbook.write(cat[key])