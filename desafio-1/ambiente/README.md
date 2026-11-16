# Ambiente de laboratório

Composição e configuração do ambiente virtual para o desafio.

## Máquinas virtuais

| VM | Papel | Rede |
|----|-------|------|
| **Kali Linux** | Executa os scripts de auditoria | Host-only |
| **Metasploitable 2** | Alvo com serviços expostos | Host-only |
| Outro alvo (SMBNT) | Serviço SMB/NetBIOS para spraying | Host-only |

## VirtualBox

- Rede: **host-only** (RT) — as VMs ficam isoladas na rede interna do host;
- Adaptador 1: `nat` (para acesso à internet no Kali);
- Adaptador 2: `host-only` (para comunicação com as VMs alvo).

## IPs

- Metasploitable 2: `192.168.56.101`
  - FTP `21`, SSH `22`, HTTP `80`, SMB `445`, NetBIOS `139`
- Outro alvo: `192.168.56.191` (serviço SMBNT utilizado no spraying)

## Verificar conectividade

```bash
ping -c 3 192.168.56.101
```

### O que significa `-c`?

`-c` é o **count** (contador): número de pacotes ICMP (`echo-request`) a enviar.
Com `-c 3`, o ping envia 3 pacotes e para sozinho. Sem `-c`, o ping roda
infinitamente (comportamento padrão no Linux). No Windows, o padrão é 4 pacotes.

## Verificar serviços

```bash
nmap -sV -p 21,22,80,445,139 192.168.56.101
```

- `-sV`: tenta identificar a versão dos serviços;
- `-p 21,22,80,445,139`: escaneia as portas FTP, SSH, HTTP, SMB e NetBIOS.

## Comandos úteis

```bash
# Lista VMs do VirtualBox
VBoxManage list vms

# Inicia uma VM em segundo plano
VBoxManage startvm "Metasploitable 2" --type headless

# Verifica se a VM está Respondendo
ping -c 3 192.168.56.101
```
