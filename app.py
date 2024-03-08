import streamlit as st
import streamlit_javascript as st_js
import json
import time
from search import ask,ask_pio

html = '''
<style>
.appview-container .main .block-container{
    padding-top: 0px;
    padding-left: 20px;
    padding-right: 20px;
    padding-bottom: 30px
}
.st-emotion-cache-1y4p8pa{
    max-width: 1200px;
}
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}
.block-container {padding-top:1rem;}
.e1fqkh3o4 {padding-top:1rem;}
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
prompt = tabquest.chat_input("Faça uma pergunta.")
contquest = tabquest.container()
def word_generator(string):
    def gen():
        for word in string.split():
            yield word + " "
            time.sleep(0.02)
    return gen
if prompt:
    contquest.write(f'**{prompt}**')
    pio = ask_pio(prompt)
    if pio:
        contquest.write_stream(word_generator(' '.join([f'*{w}*' for w in pio.split()])))
        contquest.write('<sup><i>Catecismo de São Pio X</i></sup>',unsafe_allow_html = True)
    respostas = ask(prompt)
    for resp in respostas:
        contquest.write_stream(word_generator(resp))

colbar,colspace = tabsearch.columns([.2,.8])
colbar.number_input('Parágrafo',min_value = 1,max_value = last_key,key = 'paragrafo',step = 5)
contsearch = tabsearch.container()
for key in range(st.session_state.paragrafo,min(last_key + 1,st.session_state.paragrafo + 5)):
    contsearch.write(cat[key])
contbook = tabbook.container()
for key in cat:
    contbook.write(cat[key])