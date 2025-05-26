from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
from datetime import datetime

app = Flask(__name__)
CORS(app)

DB_NAME = "bibliotecatech.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # permite acessar colunas por nome
    return conn

# Inicializa o banco de dados
def init_db():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS livros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                autor TEXT,
                ano INTEGER,
                copias INTEGER DEFAULT 1
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS emprestimos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_usuario INTEGER,
                id_livro INTEGER,
                data TEXT,
                FOREIGN KEY (id_usuario) REFERENCES usuarios(id),
                FOREIGN KEY (id_livro) REFERENCES livros(id)
            )
        """)

init_db()

@app.route("/api/livros", methods=["GET", "POST"])
def livros():
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == "POST":
        data = request.json
        if not data.get("titulo"):
            return jsonify({"erro": "Título é obrigatório"}), 400

        cursor.execute("""
            INSERT INTO livros (titulo, autor, ano, copias) 
            VALUES (?, ?, ?, ?)
        """, (data["titulo"], data.get("autor"), data.get("ano"), data.get("copias", 1)))

        conn.commit()
        return jsonify({"id": cursor.lastrowid, **data}), 201

    cursor.execute("SELECT * FROM livros")
    livros = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(livros)

@app.route("/api/usuarios", methods=["GET", "POST"])
def usuarios():
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == "POST":
        data = request.json
        if not data.get("nome"):
            return jsonify({"erro": "Nome é obrigatório"}), 400

        cursor.execute("""
            INSERT INTO usuarios (nome, email) VALUES (?, ?)
        """, (data["nome"], data.get("email")))

        conn.commit()
        return jsonify({"id": cursor.lastrowid, **data}), 201

    cursor.execute("SELECT * FROM usuarios")
    usuarios = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(usuarios)

@app.route("/api/emprestimos", methods=["GET", "POST"])
def emprestimos():
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == "POST":
        data = request.json
        id_usuario = data.get("id_usuario")
        id_livro = data.get("id_livro")

        if not id_usuario or not id_livro:
            return jsonify({"erro": "id_usuario e id_livro são obrigatórios"}), 400

        cursor.execute("SELECT * FROM livros WHERE id = ?", (id_livro,))
        livro = cursor.fetchone()
        if not livro or livro["copias"] <= 0:
            return jsonify({"erro": "Livro indisponível"}), 400

        data_atual = datetime.now().strftime("%Y-%m-%d")
        cursor.execute("""
            INSERT INTO emprestimos (id_usuario, id_livro, data) 
            VALUES (?, ?, ?)
        """, (id_usuario, id_livro, data_atual))

        cursor.execute("UPDATE livros SET copias = copias - 1 WHERE id = ?", (id_livro,))
        conn.commit()
        return jsonify({"mensagem": "Empréstimo registrado"}), 201

    cursor.execute("""
        SELECT e.id, u.nome AS usuario, l.titulo AS livro, e.data
        FROM emprestimos e
        JOIN usuarios u ON e.id_usuario = u.id
        JOIN livros l ON e.id_livro = l.id
    """)
    emprestimos = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(emprestimos)

@app.route("/api/devolucoes/<int:id_emprestimo>", methods=["POST"])
def devolucao(id_emprestimo):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id_livro FROM emprestimos WHERE id = ?", (id_emprestimo,))
    row = cursor.fetchone()

    if not row:
        conn.close()
        return jsonify({"erro": "Empréstimo não encontrado"}), 404

    id_livro = row["id_livro"]
    cursor.execute("DELETE FROM emprestimos WHERE id = ?", (id_emprestimo,))
    cursor.execute("UPDATE livros SET copias = copias + 1 WHERE id = ?", (id_livro,))
    conn.commit()
    conn.close()
    return jsonify({"mensagem": "Devolução registrada"}), 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)
