# todo_cli

Ferramenta de linha de comando mínima que lê um arquivo `todo.txt`,
atribui pontuações a cada tarefa via LLM (placeholder mockável) e
reescreve o arquivo ordenado por prioridade, anexando metadados.

## Instalação

```bash
python -m venv .venv
.venv/bin/pip install -e '.[dev]'
```

Requisitos: Python ≥ 3.11.

## Uso

```bash
python -m todo_cli.main <arquivo> [--strategy <nome>] [--dry-run]
```

Ou, via script instalado:

```bash
todo-cli <arquivo> [--strategy <nome>] [--dry-run]
```

### Opções

- `--strategy <nome>` — nome da estratégia de pontuação. Padrão:
  `wsjf_simplified`. Nomes desconhecidos recaem no padrão.
- `--dry-run` — imprime o resultado na saída padrão sem modificar o
  arquivo e sem criar backup.

### Estratégias disponíveis

- `wsjf_simplified` — `(value + urgency) * (1 + ease)` (padrão).
- `linear_combo` — `2 * value + urgency + ease`.

Cada tarefa é avaliada em três dimensões, todas inteiros no intervalo
`[0, 5]`: `value`, `urgency`, `ease`.

## Formato do arquivo

Entrada:

```
(A) Refactor auth module +backend @dev
Fix login bug +backend @urgent
Write documentation +docs
```

Saída (após execução):

```
(A) Refactor auth module +backend @dev value:4 urgency:3 ease:2 score:21
Fix login bug +backend @urgent value:5 urgency:5 ease:1 score:20
Write documentation +docs value:1 urgency:1 ease:1 score:4
```

As tarefas são ordenadas por `score` em ordem decrescente. Metadados
`value:`/`urgency:`/`ease:`/`score:` já existentes são removidos antes
da reavaliação, tornando a execução idempotente.

## Segurança

Antes de sobrescrever o arquivo, a ferramenta cria um backup em
`<arquivo>.bak`. A opção `--dry-run` não cria backup.

## Arquitetura

```
todo_cli/
├── main.py     # Entrypoint Typer — orquestração
├── parser.py   # Leitura e limpeza de metadados
├── llm.py      # Prompt, chamada (placeholder) e validação
├── scorer.py   # Estratégias puras de pontuação
└── writer.py   # Anotação, backup e escrita
```

A função `llm.call_llm` é um placeholder determinístico pensado para
ser facilmente mockado em testes. A integração real com uma API de
LLM está fora do escopo atual.

## Testes

```bash
.venv/bin/pytest
```

Linting e formatação:

```bash
.venv/bin/ruff check todo_cli tests
.venv/bin/ruff format --check todo_cli tests
```
