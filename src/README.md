# src — Aplicação Funcional

- `app.py` — interface web.
- `agent.py` — lógica do ATIA.
- `database.py` — conexão somente leitura com SQLite.
- `prompts.py` — regras fundamentais do agente.

## Execução local

Na raiz do projeto:

```bash
pip install streamlit
streamlit run src/app.py
```

O banco utilizado é `data/transporte.db`.

A primeira versão usa regras determinísticas para validar a integração entre aplicação e banco antes da inclusão de um modelo de linguagem.
