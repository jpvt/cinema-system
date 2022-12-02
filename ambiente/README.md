# Cinema System - Ambiente de Desenvolvimento

Este repositório contém o Ambiente de Desenvolvimento para o projeto Cinema System, realizado durante a disciplina de Banco de Dados da UFPB, ministrada pelo Prof. Marcelo Iury Oliveira

## Pré-Requisitos

1) Linux ou macOS.

:warning: Atenção: esta instalação foi testada somente no `Linux` e no `macOS`.

2) `docker` - instalação em https://docs.docker.com/get-docker/

3) `docker-compose` - instalação em https://docs.docker.com/compose/install/

4) `git`, `git lfs`, `wget`, `curl` e `unzip` instalados pela sua distribuição Linux ou macOS (por exemplo, utilizando o `HomeBrew`)

5) Porta `5432` disponível no host onde será executado o ambiente

## Instalação do Ambiente

1) Instale o `docker` (ver https://docs.docker.com/get-docker/) e verifique a instalação. Deve ser possível executar a imagem `hello-world` e ver a saída abaixo:

```console
foor@bar# docker run hello-world

Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    (amd64)
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.

To try something more ambitious, you can run an Ubuntu container with:
 $ docker run -it ubuntu bash

Share images, automate workflows, and more with a free Docker ID:
 https://hub.docker.com/

For more examples and ideas, visit:
 https://docs.docker.com/get-started/
```

2) Clone o repositório por SSH:

```console
foo@bar# git clone git@github.com:jpvt/cinema-system.git
```

4) Prepare o script `setup.sh` para execução.

```console
foo@bar# cd cinema-system
foo@bar# chmod a+x setup.sh
```

5) Execute o script de instalação chamado `setup.sh`. Ex.:
```console
foo@bar# ./setup.sh
```

Aguarde a preparação do ambiente e leia as instruções apresentadas ao final da execução do script `setup.sh` para utilizar o ambiente. Em caso de dúvida na execução do `setup.sh`, veja o vídeo no final deste documento.

## Operando o ambiente

O ambiente é criado utilizando o `docker-compose`, podendo ser parado e reiniciado várias vezes, além de outras verificações, como os logs do banco de dados. Em algumas situações também será necessário destruir o ambiente e reinicia-lo pelo `setup.sh`.

Execute os comandos abaixo sempre dentro do diretório `cinema-system`.

### Verificando o ambiente em execução

```console
foo@bar# docker compose ps
--------------------------------------------------------------------------------------------------
cinema-system-datalake-1   "docker-entrypoint.s…"   datalake            running             0.0.0.0:5432->5432/tcp
```

Obs.: O PostgreSQL executa na porta 5432 e pode ser acessado pelo PgAdmin, DBeaver, entre outros administrador de BDs.

### Parando o ambiente

```console
foo@bar# docker compose down                                                                                         ─╯
[+] Running 2/2
 ⠿ Container cinema-system-datalake-1  Removed                                                               0.4s
 ⠿ Network cinema-system_default       Removed   
```

### Iniciando o ambiente

```console
foo@bar# docker compose up -d                                                                                        ─╯
[+] Running 2/2
 ⠿ Network cinema-system_default       Created                                                               0.1s
 ⠿ Container cinema-system-datalake-1  Started                                                               0.6s
```

### Logs dos containers do ambiente

#### PostgreSQL

```console
foo@bar# docker compose logs datalake                                                                                ─╯
cinema-system-datalake-1  | 
cinema-system-datalake-1  | PostgreSQL Database directory appears to contain a database; Skipping initialization
cinema-system-datalake-1  | 
cinema-system-datalake-1  | 2022-11-30 13:17:44.887 -03 [1] LOG:  starting PostgreSQL 15.1 (Debian 15.1-1.pgdg110+1) on x86_64-pc-linux-gnu, compiled by gcc (Debian 10.2.1-6) 10.2.1 20210110, 64-bit
cinema-system-datalake-1  | 2022-11-30 13:17:44.887 -03 [1] LOG:  listening on IPv4 address "0.0.0.0", port 5432
cinema-system-datalake-1  | 2022-11-30 13:17:44.887 -03 [1] LOG:  listening on IPv6 address "::", port 5432
cinema-system-datalake-1  | 2022-11-30 13:17:44.900 -03 [1] LOG:  listening on Unix socket "/var/run/postgresql/.s.PGSQL.5432"
cinema-system-datalake-1  | 2022-11-30 13:17:44.912 -03 [28] LOG:  database system was shut down at 2022-11-30 13:17:01 -03
cinema-system-datalake-1  | 2022-11-30 13:17:44.921 -03 [1] LOG:  database system is ready to accept connections

```

### Destruindo o ambiente

:warning: A partir da destruição do ambiente, nenhum dos comandos acima irá funcionar, sendo necessário recriar o ambiente a partir do `setup.sh`.

O conceito de `destruição do ambiente` está relacionado a remover as imagens e arquivos de configuração relacionados ao `cinema-system`.

Para realizar alguma das etapas abaixo é necessário que o ambiente esteja parado. Para parar o ambiente, faça:

```console
foo@bar# docker compose down
```

#### Removendo os volumes

Apenas um volume para armazenar os dados do PostgreSQL é criado pelo `cinema-system`. Para apagá-lo, faça:

```console
foo@bar# docker volume rm cinema-system_pgdata  
```

Uma vez que o volume `cinema-system_pgdata` é apagado, é necessário rodar novamente o script `setup.sh` (ver Item 4 da seção de Instalação do Ambiente).

#### Removendo imagens

Para remover todas as imagens docker utilizadas pelo `cinema-system`, faça:

```console
foo@bar# docker image rm postgres:15.1
```

:warning: a) Essas são as versões atuais das imagens, porém o `cinema-system` está em constante evolução e as versões ou números podem variar ligeiramente. Sempre verifique quais as imagens instaladas pelo ambiente utilizando o comando `docker images list`.

:warning: b) Apagar as imagens implica que ao rodar o `setup.sh` novamente. Considere esta informação antes de realizar esta etapa.
