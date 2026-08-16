import streamlit as st
from agent import answer_question

st.set_page_config(page_title="ATIA — Assistente de Transporte", page_icon="🚚")
st.title("ATIA — Assistente de Transporte")
st.caption("Protótipo funcional baseado na Base de Conhecimento do projeto.")

st.write("Faça perguntas sobre os dados de transporte. O ATIA não inventa informações que não estejam disponíveis na base.")

question = st.text_input("Digite sua pergunta:", placeholder="Ex.: Quanto foi gasto com combustível?")

if st.button("Perguntar"):
    if question.strip():
        st.subheader("Resposta do ATIA")
        st.write(answer_question(question))
    else:
        st.warning("Digite uma pergunta.")
