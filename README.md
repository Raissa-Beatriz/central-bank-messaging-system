# Central Bank Messaging System

2° Projeto prático da disciplina de Sistemas Paralelos e Distribuídos.

**Professor:** Levy de Souza Silva

## Sobre o projeto

Este projeto simula um sistema distribuído de mensageria inspirado no ecossistema PIX. A ideia é representar um cenário em que múltiplos bancos geram transações e publicam essas mensagens em um broker RabbitMQ, enquanto um serviço consumidor faz a auditoria e registra todas as transações em um arquivo de log.

O foco principal da implementação está no **Audit Logging Service**, responsável por consumir as mensagens recebidas e persistir cada transação no arquivo `audit.log`.

## Objetivo

Implementar uma solução distribuída baseada em mensageria com os seguintes componentes:

- múltiplos produtores simulando bancos;
- um broker RabbitMQ para intermediar as mensagens;
- um consumidor responsável pela auditoria das transações.

## Arquitetura

O fluxo do sistema funciona assim:

1. Um banco simulado gera uma transação PIX.
2. O produtor publica essa transação na fila do RabbitMQ.
3. O Audit Logging Service consome a mensagem.
4. O consumidor registra a transação no arquivo `logs/audit.log`.

## Tecnologias utilizadas

- Python
- RabbitMQ
- Pika

## Estrutura do projeto

```text
central-bank-messaging-system/
├── consumer/
│   └── audit_consumer.py
├── producers/
│   ├── bank_a.py
│   ├── bank_b.py
│   └── bank_c.py
├── shared/
│   ├── __init__.py
│   ├── config.py
│   └── utils.py
├── logs/
│   └── .gitkeep
├── .gitignore
├── README.md
└── requirements.txt
```

## Pré-requisitos

Antes de rodar o projeto, é necessário ter instalado:

- Python 3
- RabbitMQ
- Erlang
- Git

## Instalação do RabbitMQ

1. Instale o Erlang compatível com a versão do RabbitMQ.
2. Instale o RabbitMQ Server.
3. Inicie o serviço do RabbitMQ.
4. Habilite o painel de gerenciamento:

```powershell
rabbitmq-plugins enable rabbitmq_management
```

5. Acesse no navegador:

```text
http://localhost:15672
```

Login padrão local:

- usuário: `guest`
- senha: `guest`

## Configuração do ambiente Python

Clone o repositório e entre na pasta do projeto:

```powershell
git clone https://github.com/Raissa-Beatriz/central-bank-messaging-system.git
cd central-bank-messaging-system
```

Crie e ative o ambiente virtual:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

Instale as dependências:

```powershell
pip install -r requirements.txt
```

## Como executar o projeto

Com o RabbitMQ já ligado, abra **quatro terminais** na pasta do projeto.

### Terminal 1

Inicie o consumidor de auditoria:

```powershell
python consumer/audit_consumer.py
```

### Terminal 2

Inicie o produtor do BankA:

```powershell
python producers/bank_a.py
```

### Terminal 3

Inicie o produtor do BankB:

```powershell
python producers/bank_b.py
```

### Terminal 4

Inicie o produtor do BankC:

```powershell
python producers/bank_c.py
```

## O que deve acontecer

Os produtores devem começar a enviar mensagens continuamente para a fila do RabbitMQ.

No terminal do consumidor, devem aparecer registros como estes:

```text
[*] Audit Logging Service aguardando mensagens...
[AUDIT] Registrado: [2026-06-22 20:30:01] TX-AB12CD34EF | BankA | BankB | 532.40
[AUDIT] Registrado: [2026-06-22 20:30:03] TX-98XY76ZT54 | BankB | BankC | 1200.00
[AUDIT] Registrado: [2026-06-22 20:30:05] TX-11AA22BB33 | BankC | BankA | 89.99
```

Nos terminais dos produtores, devem aparecer mensagens semelhantes a:

```text
[BankA] Enviou: {"transactionId": "...", "timestamp": "...", ...}
```

## Arquivo de auditoria

As transações processadas são registradas em:

```text
logs/audit.log
```

Exemplo de conteúdo esperado:

```text
[2026-06-22 20:30:01] TX-AB12CD34EF | BankA | BankB | 532.40
[2026-06-22 20:30:03] TX-98XY76ZT54 | BankB | BankC | 1200.00
[2026-06-22 20:30:05] TX-11AA22BB33 | BankC | BankA | 89.99
```

Para visualizar o log no PowerShell:

```powershell
Get-Content .\logs\audit.log
```

## Formato da mensagem

Cada transação enviada para o broker segue este formato:

```json
{
  "transactionId": "TX123456",
  "timestamp": "2026-06-01T10:15:30",
  "senderBank": "BankA",
  "receiverBank": "BankB",
  "senderAccount": "12345",
  "receiverAccount": "98765",
  "amount": 1500.50
}
```

## Autores

José Ernandes Gonçalves Costa

Raissa Beatriz Marinho dos Santos
