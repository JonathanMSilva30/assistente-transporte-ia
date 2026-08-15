PRAGMA foreign_keys = ON;

CREATE TABLE motoristas (
    id_motorista INTEGER PRIMARY KEY,
    nome TEXT NOT NULL,
    categoria_cnh TEXT NOT NULL,
    status TEXT NOT NULL CHECK(status IN ('Ativo','Férias','Afastado','Inativo')),
    data_admissao DATE NOT NULL
);

CREATE TABLE veiculos (
    id_veiculo INTEGER PRIMARY KEY,
    placa TEXT NOT NULL UNIQUE,
    tipo TEXT NOT NULL,
    marca TEXT NOT NULL,
    modelo TEXT NOT NULL,
    ano INTEGER NOT NULL,
    capacidade_kg REAL NOT NULL CHECK(capacidade_kg >= 0),
    status TEXT NOT NULL CHECK(status IN ('Disponível','Em viagem','Manutenção','Inativo'))
);

CREATE TABLE clientes (
    id_cliente INTEGER PRIMARY KEY,
    nome TEXT NOT NULL,
    cidade TEXT NOT NULL,
    estado TEXT NOT NULL,
    segmento TEXT NOT NULL,
    status TEXT NOT NULL
);

CREATE TABLE viagens (
    id_viagem INTEGER PRIMARY KEY,
    id_motorista INTEGER NOT NULL,
    id_veiculo INTEGER NOT NULL,
    data_saida DATE NOT NULL,
    hora_saida TIME NOT NULL,
    data_prevista_chegada DATE NOT NULL,
    hora_prevista_chegada TIME NOT NULL,
    data_real_chegada DATE,
    hora_real_chegada TIME,
    origem TEXT NOT NULL,
    destino TEXT NOT NULL,
    km_planejado REAL NOT NULL CHECK(km_planejado >= 0),
    km_realizado REAL CHECK(km_realizado IS NULL OR km_realizado >= 0),
    status TEXT NOT NULL,
    FOREIGN KEY(id_motorista) REFERENCES motoristas(id_motorista),
    FOREIGN KEY(id_veiculo) REFERENCES veiculos(id_veiculo)
);

CREATE TABLE atendimentos (
    id_atendimento INTEGER PRIMARY KEY,
    id_viagem INTEGER NOT NULL,
    id_cliente INTEGER NOT NULL,
    data_programada DATE NOT NULL,
    hora_programada TIME NOT NULL,
    data_chegada DATE,
    hora_chegada TIME,
    data_inicio_atendimento DATE,
    hora_inicio_atendimento TIME,
    data_fim_atendimento DATE,
    hora_fim_atendimento TIME,
    status TEXT NOT NULL,
    quantidade_volumes INTEGER NOT NULL CHECK(quantidade_volumes >= 0),
    peso_kg REAL NOT NULL CHECK(peso_kg >= 0),
    FOREIGN KEY(id_viagem) REFERENCES viagens(id_viagem),
    FOREIGN KEY(id_cliente) REFERENCES clientes(id_cliente)
);

CREATE TABLE ocorrencias (
    id_ocorrencia INTEGER PRIMARY KEY,
    id_viagem INTEGER NOT NULL,
    id_motorista INTEGER NOT NULL,
    id_veiculo INTEGER NOT NULL,
    data_ocorrencia DATE NOT NULL,
    hora_ocorrencia TIME NOT NULL,
    tipo TEXT NOT NULL,
    descricao TEXT NOT NULL,
    gravidade TEXT NOT NULL,
    status TEXT NOT NULL,
    FOREIGN KEY(id_viagem) REFERENCES viagens(id_viagem),
    FOREIGN KEY(id_motorista) REFERENCES motoristas(id_motorista),
    FOREIGN KEY(id_veiculo) REFERENCES veiculos(id_veiculo)
);

CREATE TABLE abastecimentos (
    id_abastecimento INTEGER PRIMARY KEY,
    id_veiculo INTEGER NOT NULL,
    id_viagem INTEGER,
    data_abastecimento DATE NOT NULL,
    hora_abastecimento TIME NOT NULL,
    tipo_combustivel TEXT NOT NULL,
    quantidade_litros REAL NOT NULL CHECK(quantidade_litros > 0),
    valor_litro REAL NOT NULL CHECK(valor_litro >= 0),
    valor_total REAL NOT NULL CHECK(valor_total >= 0),
    odometro REAL NOT NULL CHECK(odometro >= 0),
    FOREIGN KEY(id_veiculo) REFERENCES veiculos(id_veiculo),
    FOREIGN KEY(id_viagem) REFERENCES viagens(id_viagem)
);
