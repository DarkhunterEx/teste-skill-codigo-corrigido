# 01 — Reconhecimento

Verificar se a VM alvo está acessível e enumerar portas e versões dos serviços.

## Comandos

### Conectividade
```bash
ping -c 3 192.168.56.101
```

### Enumeração de portas e versões
```bash
nmap -sV -p 21,22,80,445,139 192.168.56.101
```

## Explicação dos parâmetros

| Flag | Significado |
|------|-------------|
| `-c 3` | `count`: envia 3 pacotes ICMP e para |
| `-sV` | Detecta a versão dos serviços |
| `-p 21,22,80,445,139` | Portas: FTP, SSH, HTTP, SMB, NetBIOS |

## O que observar

- Serviços abertos na VM alvo;
- Versões dos serviços (vsftpd, OpenSSH, Apache, Samba, Samba smbd);
- Quais módulos do Medusa serão necessários nas etapas seguintes.

## Resultado esperado

Variação de serviços expostos; a lista serve como "mapa" do ataque a ser executado.
