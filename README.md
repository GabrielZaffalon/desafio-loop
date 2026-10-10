# desafio-loop

Atividade da disciplina **Automação e Programabilidade em Redes**. O script faz login em uma API REST, obtém o token JWT e resolve o **Loop Challenge**: uma sequência de requisições que precisam ser enviadas no intervalo de tempo informado pelo servidor.

As credenciais ficam em um arquivo `.env`, carregado em tempo de execução, e não aparecem no código.

## Como o desafio funciona

1. O script faz `POST /challenges/loop` informando o número máximo de iterações.
2. A API sorteia quantas requisições serão necessárias (entre 2 e o máximo) e responde com o tempo de espera até a próxima, entre 5 e 60 segundos.
3. O script espera esse tempo e envia a próxima requisição, repetindo até receber `SUCCESS`.
4. Se a requisição chegar antes ou depois da hora, a API reseta o desafio.

| Status | Significado | O que o script faz |
|---|---|---|
| `START` | Desafio iniciado | Espera o tempo informado e continua |
| `CONTINUE` | Requisição no tempo certo | Espera o tempo informado e continua |
| `SUCCESS` | Desafio concluído | Mostra a mensagem e encerra |
| `TOO_EARLY` | Requisição adiantada, desafio resetado | Mostra a mensagem e encerra |
| `TOO_LATE` | Requisição atrasada, desafio resetado | Mostra a mensagem e encerra |

Base da API: `https://api.wagnerloch.com.br`

| Etapa | Método | Endpoint |
|---|---|---|
| Login | `POST` | `/auth/login` |
| Desafio | `POST` | `/challenges/loop` |

A conta precisa existir antes de rodar o script (criada na atividade de autenticação, via `POST /auth/register`).

## Estrutura

```
desafio-loop/
├── main.py        # opções de linha de comando, logging e o loop do desafio
├── get_token.py   # login na API e obtenção do token
├── get_loop.py    # requisição do desafio, com retry e medição de latência
├── .env           # credenciais e configurações (não versionado)
├── .gitignore     # ignora .env, .venv e __pycache__
└── README.md
```

## Melhorias implementadas

- **Retry para falhas de rede:** se a conexão cair ou a requisição estourar o tempo limite, o script espera 1 segundo e tenta de novo, 3 vezes por padrão, antes de encerrar.
- **Compensação de latência:** o tempo de cada requisição é medido e descontado da espera seguinte, para que a próxima requisição chegue ao servidor no momento certo. Uma margem de 0,2 s por padrão evita chegar cedo demais.
- **Logging:** as mensagens do desafio aparecem no terminal com horário e nível (`INFO`, `WARNING`, `ERROR`). Com `-v`, aparece também a resposta completa da API.
- **Linha de comando:** o número de iterações, a margem e as tentativas podem ser informados por opções.

## Requisitos

- Python 3.10 ou superior
- Bibliotecas `requests` e `python-dotenv`

## Como executar

**1. Criar e ativar o ambiente virtual**

Windows (PowerShell):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**2. Instalar as dependências**

```bash
python -m pip install requests python-dotenv
```

**3. Criar o arquivo `.env`**

Na pasta do projeto, crie um arquivo `.env` com as quatro variáveis:

```
BASE=https://api.wagnerloch.com.br
LIMIT_TIME=10

API_EMAIL=seu@email.com
API_SENHA=sua-senha
```

| Variável | Descrição |
|---|---|
| `BASE` | Endereço base da API |
| `LIMIT_TIME` | Tempo limite de cada requisição, em segundos |
| `API_EMAIL` | E-mail da conta |
| `API_SENHA` | Senha da conta |

**4. Rodar o script**

Perguntando o número de iterações:

```bash
python main.py
```

Informando pela linha de comando:

```bash
python main.py -m 5
```

## Opções

| Opção | Padrão | Descrição |
|---|---|---|
| `-m`, `--max-iteracoes` | pergunta ao usuário | Número máximo de iterações |
| `--margem` | `0.2` | Segundos somados à espera para não chegar cedo demais |
| `--tentativas` | `3` | Novas tentativas quando a rede falha |
| `-v`, `--verbose` | desligado | Mostra as mensagens de debug, com a resposta completa da API |
| `-h`, `--help` | | Mostra a ajuda |

Quando o `-m` não é informado, o script pergunta o número de iterações e repete a pergunta enquanto a entrada não for um número inteiro maior que um.

## Saída esperada

```
Fazendo login do usuário.

Login feito com sucesso!

==============================
Início do desafio de Loop!
==============================

18:02:27 [INFO] [START] Desafio iniciado! Você precisa fazer 2 requisições. A próxima deve ser em 19 segundos. (progresso: 1 / 2)
18:02:27 [INFO] Latência: 0.688s | espera pedida: 19s | espera real: 18.512s
18:02:46 [INFO] [CONTINUE] Correto! Próxima requisição em 12 segundos. (progresso: 2 / 2)
18:02:46 [INFO] Latência: 0.703s | espera pedida: 12s | espera real: 11.497s
18:02:58 [INFO] [SUCCESS] Parabéns! Você completou o desafio de loop com sucesso!
```

## Tratamento de erros

| Situação | Comportamento |
|---|---|
| Variável ausente no `.env` | `Erro: defina ... no .env antes de executar.` e encerra |
| `LIMIT_TIME` não numérico | Informa o valor recebido e encerra |
| Erro HTTP no login (como credenciais erradas) | Exceção do `raise_for_status()` com o código de status |
| Falha de rede ou tempo limite no desafio | Avisa e tenta de novo até o limite de `--tentativas` |
| `TOO_EARLY` ou `TOO_LATE` | Mostra a mensagem da API e encerra; basta rodar de novo |

## Segurança

- O `.env` está no `.gitignore` e **não deve ser versionado**. Antes de cada commit, confira com `git status` que ele não aparece na lista.
- O token não é exibido no terminal.
- O token JWT emitido pela API expira em **1 hora**. Basta rodar o script de novo para obter um token novo.

## Autor

Gabriel Zaffalon
