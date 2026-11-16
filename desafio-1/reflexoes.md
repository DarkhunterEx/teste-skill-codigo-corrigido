# Reflexões — Desafio 1

Resumo das aprendizagens e observações do processo de pentest realizado no
primeiro desafio.

## 1. O que foi feito

- **Reconhecimento:** `ping -c 3` e `nmap -sV -p 21,22,80,445,139`.
- **Força bruta FTP:** Medusa com wordlists de usuário e senha.
- **Password spraying:** `enum4linux`, `echo` para gerar wordlists e Medusa SMBNT
  com `-T 50`.
- **Força bruta web (DVWA):** Medusa `web-form` e Hydra `http-get-form`.

## 2. O que ficou claro

- **O `-c` no `ping` é o contador de pacotes.** `ping -c 3` envia 3 pacotes e para.
- **A `nmap -sV -p ...` direciona a escolha dos módulos.** Saber quais serviços
  estão expostos redefine o cenario de ataque.
- **O Medusa funciona melhor com o formulário bem definido.**
  O `form-data` deve ser o body do POST com `^USER^` e `^PASS^`.
- **O Hydra precisa de aspas nos headers com `;`.**
  Sem as aspas, `security=low` é lido como parâmetro extra e a tentativa falha.
- **`-T 50` é decisivo no spraying.** Atraso entre tentativas evita bloqueio de
  conta e reduz a chance de detecção.

## 3. Erros encontrados e corrigidos

1. `less enum4output.txt` → o arquivo gerado foi `enum4_output.txt` (com sublinhado).
2. `echo -e "password\n123456\nWelcome123\nmsfadmin` → faltava o fechamento de
   aspas; corrigido para `" > senham.txt`.
3. `-m form-data:'get?username=&password=&Login=Login'` → o `form-data` deve ser o
   body do POST, não uma URL GET. Corrigido para
   `'username=^USER^&password=^PASS^&Login=Login'`.
4. `H=Cookie: PHPSESSID=...;security=low` → o `;` quebrava a opção. Corrigido com
   aspas: `H='Cookie: PHPSESSID=...;security=low'`.

## 4. O que se aprendeu

- A cadeia de ataque foi feita em camadas: reconhecimento → força bruta → spraying →
  web.
- A qualidade das wordlists é mais importante que o tamanho. A lista mistura padrões
  gerais (`123456`, `password`) com credenciais plausíveis para o cenário
  (`msfadmin`, `Welcome123`).
- Sempre registrar o comando, a saída e as correções deixa o repositório útil para
  reexecução e estudo.

## 5. Próximos passos

- Reproduzir o desafio em um ambiente isolado;
- Testar outros módulos do Medusa (SSH, HTTP POST);
- Gerar relatório de evidências com screenshots e comandos logados.
