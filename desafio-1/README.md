# Desafio 1 — Força Bruta e Password Spraying com Medusa

Mentoria prática de segurança da informação. O objetivo: usar **Kali Linux** e a
ferramenta **Medusa** em ambientes vulneráveis (**Metasploitable 2** + **DVWA**) para
simular cenários de **força bruta** e **password spraying**, e documentar o processo
para comprovar o entendimento e compor o portfólio técnico.

## Como o desafio funciona

1. **Configurar o ambiente** — duas VMs (Kali Linux e Metasploitable 2) no VirtualBox,
   com rede interna **host-only**.
2. **Executar ataques simulados** — força bruta em FTP, automação de tentativas em
   formulário web (DVWA) e password spraying em SMB com enumeração de usuários.
3. **Documentar os testes** — wordlists simples, comandos utilizados, validação de
   acessos e recomendações de mitigação.

> ⚠️ **Flexibilidade:** o desafio é aberto. Você pode seguir os cenários propostos
> (FTP, DVWA, SMB) ou adaptar — outras ferramentas, novas wordlists, módulos
> diferentes, ou apenas documentar em detalhes o que aprendeu.

## Objetivos de aprendizagem

Ao concluir, você será capaz de:

- Compreender ataques de **força bruta** em diferentes serviços (FTP, Web, SMB);
- Utilizar o **Kali Linux** e o **Medusa** para auditoria de segurança em ambiente
  controlado;
- Documentar processos técnicos de forma clara e estruturada;
- Reconhecer vulnerabilidades comuns e propor medidas de **mitigação**;
- Usar o **GitHub** como portfólio técnico para compartilhar documentação e evidências.

## Estrutura do repositório

```
desafio-1/
├── README.md                # Documentação principal
├── ambiente/                # Como montar o laboratório
├── 01-recon/                # Reconhecimento
├── 02-forca-bruta-ftp/      # Força bruta em FTP
├── 03-password-spraying/    # Password spraying em SMB
├── 04-forca-bruta-web/      # Força bruta em formulário web (DVWA)
├── wordlists/               # Wordlists utilizadas
└── reflexoes.md             # Reflexões e aprendizados
```

## Pré-requisitos

- VirtualBox rodando com **Kali Linux** e **Metasploitable 2** em rede host-only;
- O Linux Kali com as ferramentas `medusa`, `hydra`, `nmap`, `enum4linux`;
- Ambientes alvo acessíveis na rede interna.

## Como rodar

1. Siga `ambiente/` para montar o laboratório;
2. Execute os cenários em cada pasta (`01-recon/`, `02-forca-bruta-ftp/`, etc.);
3. Revise a documentação de cada etapa — os comandos estão comentados;
4. Consulte `reflexoes.md` para os aprendizados e `README.md` final do repositório.

## Entrega

- Repositório **público** no GitHub;
- `README.md` detalhado;
- Wordlists e (opcionalmente) capturas de tela em `/images`;
- Link do repositório + breve descrição enviados no "Entregar Projeto".

## Licença

Documento didático. Use apenas em ambientes próprios ou autorizados.
