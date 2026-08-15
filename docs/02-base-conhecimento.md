# Etapa 2 — Base de Conhecimento

## 1. Objetivo

A Base de Conhecimento do ATIA será a fonte de dados utilizada para responder perguntas relacionadas à operação de transporte.

O princípio central é:

> **O ATIA somente deverá apresentar informações factuais fundamentadas nos dados disponíveis. Quando os dados forem inexistentes ou insuficientes, não deverá inventar, estimar ou completar a resposta.**

## 2. Tecnologia

Será utilizado **SQLite**.

Banco:

```text
data/transporte.db
```

A escolha permite utilizar um banco relacional real sem necessidade de servidor, facilitando a execução local e a integração posterior com Python.

## 3. Entidades

A primeira versão será composta por:

1. `motoristas`
2. `veiculos`
3. `clientes`
4. `viagens`
5. `atendimentos`
6. `ocorrencias`
7. `abastecimentos`

---

# 4. Dicionário de Dados

## 4.1 `motoristas`

| Campo | Tipo | Chave | Descrição |
|---|---|---|---|
| id_motorista | INTEGER | PK | Identificador único |
| nome | TEXT | - | Nome |
| categoria_cnh | TEXT | - | Categoria da CNH |
| status | TEXT | - | Situação |
| data_admissao | DATE | - | Data de admissão |

Status: `Ativo`, `Férias`, `Afastado`, `Inativo`.

## 4.2 `veiculos`

| Campo | Tipo | Chave | Descrição |
|---|---|---|---|
| id_veiculo | INTEGER | PK | Identificador |
| placa | TEXT | UNIQUE | Placa |
| tipo | TEXT | - | Tipo do veículo |
| marca | TEXT | - | Marca |
| modelo | TEXT | - | Modelo |
| ano | INTEGER | - | Ano |
| capacidade_kg | REAL | - | Capacidade de carga |
| status | TEXT | - | Situação |

Status: `Disponível`, `Em viagem`, `Manutenção`, `Inativo`.

## 4.3 `clientes`

| Campo | Tipo | Chave | Descrição |
|---|---|---|---|
| id_cliente | INTEGER | PK | Identificador |
| nome | TEXT | - | Nome |
| cidade | TEXT | - | Cidade |
| estado | TEXT | - | Estado |
| segmento | TEXT | - | Segmento |
| status | TEXT | - | Situação |

## 4.4 `viagens`

| Campo | Tipo | Chave | Descrição |
|---|---|---|---|
| id_viagem | INTEGER | PK | Identificador |
| id_motorista | INTEGER | FK | Motorista |
| id_veiculo | INTEGER | FK | Veículo |
| data_saida | DATE | - | Data de saída |
| hora_saida | TIME | - | Hora de saída |
| data_prevista_chegada | DATE | - | Data prevista |
| hora_prevista_chegada | TIME | - | Hora prevista |
| data_real_chegada | DATE | - | Data real |
| hora_real_chegada | TIME | - | Hora real |
| origem | TEXT | - | Origem |
| destino | TEXT | - | Destino |
| km_planejado | REAL | - | KM planejado |
| km_realizado | REAL | - | KM realizado |
| status | TEXT | - | Situação |

Atraso da viagem:

```text
data/hora real de chegada - data/hora prevista = tempo de atraso
```

## 4.5 `atendimentos`

Representa o atendimento realizado no local do cliente.

| Campo | Tipo | Chave | Descrição |
|---|---|---|---|
| id_atendimento | INTEGER | PK | Identificador |
| id_viagem | INTEGER | FK | Viagem |
| id_cliente | INTEGER | FK | Cliente |
| data_programada | DATE | - | Data programada |
| hora_programada | TIME | - | Hora programada |
| data_chegada | DATE | - | Data efetiva da chegada |
| hora_chegada | TIME | - | Hora efetiva da chegada |
| data_inicio_atendimento | DATE | - | Data de início |
| hora_inicio_atendimento | TIME | - | Hora de início |
| data_fim_atendimento | DATE | - | Data de término |
| hora_fim_atendimento | TIME | - | Hora de término |
| status | TEXT | - | Situação |
| quantidade_volumes | INTEGER | - | Volumes |
| peso_kg | REAL | - | Peso |

Status: `Programado`, `Realizado`, `Atrasado`, `Cancelado`, `Não realizado`.

Atraso do atendimento:

```text
data/hora de chegada - data/hora programada = tempo de atraso
```

Tempo de atendimento:

```text
data/hora de fim - data/hora de início = duração
```

## 4.6 `ocorrencias`

| Campo | Tipo | Chave | Descrição |
|---|---|---|---|
| id_ocorrencia | INTEGER | PK | Identificador |
| id_viagem | INTEGER | FK | Viagem |
| id_motorista | INTEGER | FK | Motorista |
| id_veiculo | INTEGER | FK | Veículo |
| data_ocorrencia | DATE | - | Data |
| hora_ocorrencia | TIME | - | Hora |
| tipo | TEXT | - | Tipo |
| descricao | TEXT | - | Descrição |
| gravidade | TEXT | - | Gravidade |
| status | TEXT | - | Situação |

Tipos: `Avaria`, `Acidente`, `Trânsito`, `Falha mecânica`, `Problema documental`, `Problema operacional`, `Outros`.

Gravidade: `Baixa`, `Média`, `Alta`, `Crítica`.

## 4.7 `abastecimentos`

| Campo | Tipo | Chave | Descrição |
|---|---|---|---|
| id_abastecimento | INTEGER | PK | Identificador |
| id_veiculo | INTEGER | FK | Veículo |
| id_viagem | INTEGER | FK | Viagem relacionada, quando aplicável |
| data_abastecimento | DATE | - | Data |
| hora_abastecimento | TIME | - | Hora |
| tipo_combustivel | TEXT | - | Combustível |
| quantidade_litros | REAL | - | Litros |
| valor_litro | REAL | - | Preço por litro |
| valor_total | REAL | - | Valor total |
| odometro | REAL | - | Odômetro |

Tipos previstos: `Diesel`, `Diesel S10`, `Diesel S500`, `Gasolina`, `Etanol`.

---

# 5. Relacionamentos

```text
MOTORISTAS
    |
    | 1:N
    v
VIAGENS
    |
    +----> ATENDIMENTOS ----> CLIENTES
    |
    +----> OCORRENCIAS
    |
    +----> ABASTECIMENTOS <---- VEICULOS

VIAGENS ----> VEICULOS
```

Principais relações:

- Um motorista pode realizar várias viagens.
- Um veículo pode participar de várias viagens.
- Uma viagem pode possuir vários atendimentos.
- Um cliente pode possuir vários atendimentos.
- Uma viagem pode possuir várias ocorrências.
- Um veículo pode possuir vários abastecimentos.
- Uma viagem pode estar relacionada a vários abastecimentos.

---

# 6. Perguntas que a base deverá permitir

A base deverá permitir perguntas não previamente programadas, desde que os dados necessários existam.

### Viagens

- Quantas viagens foram realizadas?
- Qual motorista realizou mais viagens?
- Qual foi a distância total percorrida?
- Quais viagens chegaram atrasadas?

### Atendimentos

- Quais atendimentos chegaram atrasados?
- Qual foi o maior atraso?
- Qual foi o atraso médio?
- Qual cliente teve mais atrasos?
- Qual motorista teve mais atrasos?
- Qual percentual de atendimentos ocorreu dentro do horário?
- Qual foi o tempo médio de atendimento?

### Combustível

- Quanto combustível foi consumido?
- Qual veículo consumiu mais?
- Qual foi o consumo médio em km/l?
- Qual veículo apresentou melhor consumo?
- Quanto foi gasto com combustível?
- Qual foi o custo médio por quilômetro?

### Ocorrências

- Quantas ocorrências foram registradas?
- Qual motorista teve mais ocorrências?
- Qual veículo teve mais ocorrências?
- Quais foram as ocorrências críticas?

### Cruzamentos

Também será possível fazer perguntas que envolvam várias entidades, por exemplo:

> Qual motorista realizou mais viagens atrasadas?

> Qual motorista teve mais atrasos de atendimento?

> Qual veículo teve maior consumo médio?

> Qual motorista realizou mais viagens e qual foi o consumo médio dos veículos utilizados por ele?

---

# 7. Regra de ausência de informação

Uma pergunta relacionada a transporte não significa que a resposta necessariamente exista.

Exemplo:

> Qual foi o faturamento da empresa?

Se não houver dados de faturamento, o ATIA deverá informar que a informação não está disponível.

Não deverá:

- estimar;
- usar conhecimento externo;
- inventar;
- completar com suposições.

---

# 8. Integridade dos Dados

Os registros deverão manter relacionamentos válidos.

Exemplos:

- uma viagem deve possuir motorista válido;
- uma viagem deve possuir veículo válido;
- um atendimento deve possuir viagem e cliente válidos;
- uma ocorrência relacionada a uma viagem deve apontar para uma viagem existente;
- um abastecimento deve apontar para um veículo existente;
- litros, quilômetros e valores não deverão ser negativos.

---

# 9. Dados Fictícios

Os dados serão fictícios e destinados exclusivamente a fins educacionais, demonstração, desenvolvimento e testes.

Os registros serão construídos de forma coerente entre si para permitir consultas, cálculos e cruzamentos.

---

# 10. Próximo passo

Após a validação desta estrutura, será criado:

```text
data/
└── transporte.db
```

Também será criado um arquivo SQL para permitir reproduzir a estrutura do banco.

