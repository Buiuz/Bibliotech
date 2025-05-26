📚 BiblioTech

Sistema completo de gerenciamento de biblioteca com **Flask (Back-end)** e **Streamlit (Front-end)**.  
Permite cadastrar livros e usuários, registrar empréstimos e devoluções, além de gerar relatórios interativos.

---

## 🔧 Tecnologias Utilizadas

- Python 3.8+
- Flask (API REST)
- Flask-CORS
- SQLite (Banco de dados)
- Streamlit (Interface gráfica)
- Requests
- Plotly
- Pandas

---

## 📦 Instalação de Dependências

Crie um ambiente virtual (opcional, mas recomendado):

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

Instale as dependências com:

```bash
pip install -r requirements.txt
```

Se preferir, instale manualmente:

```bash
pip install flask flask-cors streamlit requests pandas plotly
```

---

## ▶️ Como Rodar o Projeto

### 1. **Iniciar o Back-end (API Flask)**

Execute o arquivo `api.py`:

```bash
python api.py
```

O servidor Flask estará disponível em:  
📍 `http://localhost:5000/api`

---

### 2. **Iniciar o Front-end (Streamlit)**

Execute o Streamlit:

```bash
streamlit run bibliotech.py
```

A interface será aberta automaticamente no navegador:  
📍 `http://localhost:8501`

---

## 🗂 Estrutura do Projeto

```
📁 projeto/
│
├── api.py              # Backend Flask
├── bibliotech.py       # Frontend Streamlit
├── bibliotecatech.db   # Banco de dados SQLite (gerado automaticamente)
├── requirements.txt    # Lista de dependências
└── README.md           # Documentação do projeto
```

---

## 📸 Funcionalidades

- ✅ Cadastro de livros e usuários
- 📤 Registro de empréstimos
- 📥 Devolução de livros
- 📊 Painel com métricas
- 📈 Gráficos interativos por usuário e ano

---

## 🧪 Requisitos

- Python 3.8 ou superior
- Navegador web (Chrome, Firefox, etc.)

---

## 👨‍💻 Autor

Desenvolvido por buiuz 🚀  
Colabore, dê sugestões ou envie melhorias! 😊
