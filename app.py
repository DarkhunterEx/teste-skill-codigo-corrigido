import sqlite3


def fazer_login(usuario, senha):
    conexao = None
    try:
        conexao = sqlite3.connect("banco_de_dados.db")
        cursor = conexao.cursor()

        # Consulta parametrizada: os valores são passados separadamente,
        # impedindo que o usuário altere a estrutura da query (SQL Injection).
        query = "SELECT * FROM usuarios WHERE username = ? AND password = ?"
        cursor.execute(query, (usuario, senha))

        resultado = cursor.fetchone()
        return "Acesso Permitido!" if resultado else "Acesso Negado."
    finally:
        if conexao is not None:
            conexao.close()
