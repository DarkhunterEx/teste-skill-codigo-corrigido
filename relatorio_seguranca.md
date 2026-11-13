# Relatório de Segurança — app.py

**Arquivo analisado:** `app.py`
**Data:** 13/11/2026
**Teste realizado:** `teste-skill-codigo-corrigido`

---

## 1. Resumo

O arquivo `app.py` possui uma **falha crítica de segurança** que permite que um
atacante contorne a autenticação e acesse o sistema sem senha válida.

**Classificação: CRÍTICO**

---

## 2. Falhas encontradas

### 2.1 SQL Injection — crítico

**Local:** linha 7

```python
query = f"SELECT * FROM usuarios where username = '{usuario}' AND password = '{senha}'"
```

**O que está errado:** os valores de `usuario` e `senha` são inseridos
**diretamente** na query SQL por meio de f-string. Um atacante pode enviar:

```text
usuario  = ' OR '1'='1
senha    = ' OR '1'='1
```

A query resultante vira:

```sql
SELECT * FROM usuarios WHERE username = '' OR '1'='1' AND password = '' OR '1'='1'
```

O que sempre retorna pelo menos um registro → **acesso autorizado sem senha
válida.**

**Correção:** usar consulta parametrizada.

**Correção aplicada:**

```python
query = "SELECT * FROM usuarios WHERE username = ? AND password = ?"
cursor.execute(query, (usuario, senha))
```

---

### 2.2 Conexão e cursor não fechados em caso de erro

**Local:** linhas 4–11

Se `cursor.execute()` ou qualquer outra operação lançar uma exceção, a conexão
`sqlite3` não é fechada — isso causa **vazamento de conexão / resource leak** e
pode enfraquecer o banco.

**Correção:** garantir o fechamento com `try/finally`.

**Correção aplicada:**

```python
try:
    conexao = sqlite3.connect("banco_de_dados.db")
    cursor = conexao.cursor()
    ...
finally:
    if conexao is not None:
        conexao.close()
```

---

## 3. Recomendações (melhorias adicionais)

1. **Armazenar senhas com hash** (`bcrypt` ou `argon2`) em vez de texto puro.
   A senha deve ser hasheada **antes** da comparação.
2. **Validar/limitar as entradas** do usuário (comprimento, tipo, caracteres
   permitidos).
3. **Usar um ORM** (ex.: SQLAlchemy) para evitar a construção manual de queries.
4. **Isolar credenciais** — colocar caminhos do banco em variáveis de ambiente,
   não no código-fonte.

---

## 4. Versão corrigida

Veja o arquivo `app.py` disponível nesta pasta. Ele contém apenas a correção
necessária: consulta parametrizada + fechamento seguro da conexão.

---

*Relatório gerado pela análise de segurança.*
