import streamlit as st
import plotly.express as px
import requests
import pandas as pd

# Configuração da página
st.set_page_config(page_title="BiblioTech", page_icon="📓", layout="wide")
st.markdown("""
    <style>
        .main {
            background-color: #1e1e2f;
            color: white;
        }
        .css-1d391kg, .css-1v3fvcr {
            background-color: #2c2f48;
            border-radius: 15px;
            padding: 1.5rem;
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
            color: white;
        }
        .stButton>button {
            border-radius: 10px;
            background-color: #6c63ff;
            color: white;
            font-weight: bold;
        }
        .css-1v3fvcr .stTextInput>div>input,
        .css-1v3fvcr .stNumberInput>div>input,
        .css-1v3fvcr .stSelectbox>div>div>div>input {
            background-color: #3b3e5e;
            color: white;
        }
        .stRadio>div>label {
            color: white;
        }
        .css-1aumxhk, .css-1v3fvcr h1, .css-1v3fvcr h2, .css-1v3fvcr h3 {
            color: #f0f0f0;
        }
    </style>
""", unsafe_allow_html=True)

st.title("📚 BiblioTech - Sistema de Gerenciamento de Biblioteca")

# URL base da API
API_URL = "http://localhost:5000/api"

# Funções auxiliares para consumir a API
def get_livros():
    try:
        resp = requests.get(f"{API_URL}/livros")
        return resp.json() if resp.status_code == 200 else []
    except:
        return []

def get_usuarios():
    try:
        resp = requests.get(f"{API_URL}/usuarios")
        return resp.json() if resp.status_code == 200 else []
    except:
        return []

def get_emprestimos():
    try:
        resp = requests.get(f"{API_URL}/emprestimos")
        return resp.json() if resp.status_code == 200 else []
    except:
        return []

def cadastrar_livro(titulo, autor, ano, copias):
    try:
        payload = {"titulo": titulo, "autor": autor, "ano": ano, "copias": copias}
        r = requests.post(f"{API_URL}/livros", json=payload)
        return r.status_code == 201
    except:
        return False

def cadastrar_usuario(nome, identificacao, contato):
    try:
        payload = {"nome": nome, "identificacao": identificacao, "contato": contato}
        r = requests.post(f"{API_URL}/usuarios", json=payload)
        return r.status_code == 201
    except:
        return False

def emprestar_livro(id_usuario, id_livro):
    try:
        payload = {"id_usuario": id_usuario, "id_livro": id_livro}
        r = requests.post(f"{API_URL}/emprestimos", json=payload)
        return r.status_code == 201
    except:
        return False

def devolver_livro(id_emprestimo):
    try:
        r = requests.post(f"{API_URL}/devolucoes/{id_emprestimo}")
        return r.status_code == 200
    except:
        return False

# Navegação
st.sidebar.image("https://img.icons8.com/external-flatart-icons-outline-flatarticons/64/library.png", width=50)
pagina = st.sidebar.radio("📌 Menu", [
    "Dashboard", 
    "Cadastrar Livro", 
    "Cadastrar Usuário",
    "Consultar Livros",
    "Empréstimo de Livro", 
    "Devolução de Livro",
    "Relatórios"])

# Dashboard
if pagina == "Dashboard":
    st.subheader("📊 Visão Geral")
    livros = get_livros()
    usuarios = get_usuarios()
    emprestimos = get_emprestimos()

    col1, col2, col3 = st.columns(3)
    col1.metric("📘 Total de Livros", len(livros))
    col2.metric("👥 Usuários Cadastrados", len(usuarios))
    col3.metric("📤 Empréstimos Ativos", len(emprestimos))

# Cadastro de Livro
elif pagina == "Cadastrar Livro":
    st.subheader("➕ Cadastrar Livro")
    with st.form("form_livro"):
        titulo = st.text_input("Título")
        autor = st.text_input("Autor")
        ano = st.number_input("Ano de Publicação", step=1)
        copias = st.number_input("Número de Cópias", step=1)
        submitted = st.form_submit_button("Cadastrar")
        if submitted:
            if cadastrar_livro(titulo, autor, ano, copias):
                st.success("✅ Livro cadastrado com sucesso!")
            else:
                st.error("❌ Erro ao cadastrar livro.")

# Cadastro de Usuário
elif pagina == "Cadastrar Usuário":
    st.subheader("👤 Cadastrar Usuário")
    with st.form("form_usuario"):
        nome = st.text_input("Nome")
        identificacao = st.text_input("Identificação")
        contato = st.text_input("Contato")
        submitted = st.form_submit_button("Cadastrar")
        if submitted:
            if cadastrar_usuario(nome, identificacao, contato):
                st.success("✅ Usuário cadastrado com sucesso!")
            else:
                st.error("❌ Erro ao cadastrar usuário.")

# Consulta de Livros
elif pagina == "Consultar Livros":
    st.subheader("🔎 Consultar Livros")
    livros = get_livros()
    busca = st.text_input("Buscar por título, autor ou ano")
    if busca:
        livros = [livro for livro in livros if busca.lower() in str(livro).lower()]
    st.dataframe(livros, use_container_width=True)

# Empréstimo de Livro
elif pagina == "Empréstimo de Livro":
    st.subheader("📤 Empréstimo de Livro")
    usuarios = get_usuarios()
    livros = get_livros()
    usuarios_op = {u['nome']: u['id'] for u in usuarios}
    livros_disponiveis = {f"{l['titulo']} ({l['copias']} disp)": l['id'] for l in livros if l['copias'] > 0}

    if usuarios_op and livros_disponiveis:
        with st.form("form_emprestimo"):
            usuario = st.selectbox("Usuário", list(usuarios_op.keys()))
            livro = st.selectbox("Livro", list(livros_disponiveis.keys()))
            submitted = st.form_submit_button("Emprestar")
            if submitted:
                if emprestar_livro(usuarios_op[usuario], livros_disponiveis[livro]):
                    st.success("📚 Livro emprestado com sucesso!")
                else:
                    st.error("❌ Falha ao emprestar livro.")
    else:
        st.warning("⚠️ É necessário ao menos um usuário e um livro disponível para realizar empréstimos.")

# Devolução de Livro
elif pagina == "Devolução de Livro":
    st.subheader("📥 Devolução de Livro")
    emprestimos = get_emprestimos()
    opcoes = {f"{e['usuario']} - {e['livro']}": e['id'] for e in emprestimos}

    if opcoes:
        devolucao = st.selectbox("Selecione um empréstimo para devolução", list(opcoes.keys()))
        if st.button("Devolver"):
            if devolver_livro(opcoes[devolucao]):
                st.success("✅ Livro devolvido com sucesso!")
            else:
                st.error("❌ Erro ao registrar devolução.")
    else:
        st.info("ℹ️ Nenhum empréstimo ativo encontrado.")

# Relatórios
elif pagina == "Relatórios":
    st.subheader("📈 Relatórios Visuais")
    col1, col2 = st.columns(2)
    with col1:
        livros = get_livros()
        if livros:
            df = pd.DataFrame(livros)
            st.subheader("📅 Livros por Ano")
            st.plotly_chart(px.histogram(df, x="ano", title="Publicações por Ano"), use_container_width=True)
    with col2:
        emprestimos = get_emprestimos()
        if emprestimos:
            df = pd.DataFrame(emprestimos)
            st.subheader("👤 Empréstimos por Usuário")
            st.plotly_chart(px.histogram(df, x="usuario", title="Empréstimos por Usuário"), use_container_width=True)
