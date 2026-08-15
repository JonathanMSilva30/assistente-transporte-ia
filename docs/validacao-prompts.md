# Validação dos Prompts — Etapa 3

## Objetivo
Verificar se as regras do prompt conduzem o ATIA ao comportamento esperado antes da integração com a aplicação.

## Critérios
- Responder quando houver dados.
- Calcular quando houver dados suficientes.
- Pedir esclarecimento quando a pergunta for ambígua.
- Informar ausência de dados quando a informação não existir.
- Nunca inventar valores.

## Casos de teste

### T01 — Quantas viagens existem na base?
- **Comportamento esperado:** RESPONDER
- **Justificativa:** Há dados suficientes na tabela viagens.
- **Validação da base:** 30

### T02 — Quanto foi gasto com combustível?
- **Comportamento esperado:** CALCULAR
- **Justificativa:** Usar SUM(valor_total) em abastecimentos.
- **Validação da base:** R$ 12482.37

### T03 — Qual foi o maior atraso de atendimento?
- **Comportamento esperado:** CALCULAR
- **Justificativa:** Comparar chegada com data/hora programada.
- **Validação da base:** 60 minutos

### T04 — Qual foi o faturamento da empresa?
- **Comportamento esperado:** NÃO RESPONDER
- **Justificativa:** Faturamento não existe na Base de Conhecimento.
- **Validação da base:** Não existe

### T05 — Qual foi o atraso?
- **Comportamento esperado:** PEDIR ESCLARECIMENTO
- **Justificativa:** Pode significar atraso da viagem ou do atendimento.
- **Validação da base:** Não aplicável

### T06 — Qual veículo percorreu mais quilômetros?
- **Comportamento esperado:** RESPONDER
- **Justificativa:** Usar viagens relacionadas a veículos.
- **Validação da base:** PQR6I78 — 876.0 km

### T07 — Qual foi o consumo médio em km/l?
- **Comportamento esperado:** CALCULAR
- **Justificativa:** Derivar a métrica somente dos dados disponíveis.
- **Validação da base:** 3.16 km/l

### T08 — Qual foi o salário dos motoristas?
- **Comportamento esperado:** NÃO RESPONDER
- **Justificativa:** Salário não existe na Base de Conhecimento.
- **Validação da base:** Não existe

### T09 — Qual cliente teve mais atendimentos atrasados?
- **Comportamento esperado:** RESPONDER
- **Justificativa:** Relacionar atendimentos e clientes.
- **Validação da base:** Centro Médico Leste — 4 atrasos

### T10 — Qual motorista teve mais ocorrências?
- **Comportamento esperado:** RESPONDER
- **Justificativa:** Relacionar ocorrências e motoristas.
- **Validação da base:** Felipe Santos — 3 ocorrências

## Conclusão
Os casos foram classificados de acordo com as regras definidas em `03-prompts-agente.md`. Os testes T01, T02, T03, T06, T07, T09 e T10 possuem dados verificáveis na base; T04 e T08 devem ser tratados como ausência de informação; T05 deve solicitar esclarecimento.

Esta etapa valida o comportamento esperado dos prompts. A avaliação real das respostas do modelo será realizada novamente na Etapa 6, com métricas e critérios formais.