from database import query_one, query_rows
from prompts import NO_DATA_MESSAGE, AMBIGUOUS_DELAY_MESSAGE
import unicodedata


def normalize(text):
    text = text.lower().strip()
    text = "".join(
        char for char in unicodedata.normalize("NFD", text)
        if unicodedata.category(char) != "Mn"
    )
    return " ".join(text.split())


def money(value):
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def _has_any(text, terms):
    return any(term in text for term in terms)


def _fuel_average():
    return query_one("""
        WITH litros_viagem AS (
            SELECT id_viagem, SUM(quantidade_litros) AS litros
            FROM abastecimentos
            WHERE id_viagem IS NOT NULL
            GROUP BY id_viagem
        )
        SELECT ROUND(SUM(v.km_realizado) / SUM(l.litros), 2)
        FROM viagens v
        JOIN litros_viagem l ON l.id_viagem = v.id_viagem
        WHERE v.km_realizado IS NOT NULL
          AND l.litros > 0
    """)


def _fuel_cost_per_km():
    return query_one("""
        WITH custo_viagem AS (
            SELECT id_viagem, SUM(valor_total) AS custo
            FROM abastecimentos
            WHERE id_viagem IS NOT NULL
            GROUP BY id_viagem
        )
        SELECT ROUND(SUM(c.custo) / SUM(v.km_realizado), 2)
        FROM viagens v
        JOIN custo_viagem c ON c.id_viagem = v.id_viagem
        WHERE v.km_realizado IS NOT NULL
          AND v.km_realizado > 0
    """)


def _delay_minutes():
    return query_one("""
        SELECT MAX(
            CAST(
                (
                    julianday(data_chegada || ' ' || hora_chegada) -
                    julianday(data_programada || ' ' || hora_programada)
                ) * 24 * 60 AS INTEGER
            )
        )
        FROM atendimentos
        WHERE data_chegada IS NOT NULL
          AND hora_chegada IS NOT NULL
    """)


def answer_question(question):

    q = normalize(question)

    if not q:
        return "Digite uma pergunta para o ATIA."

    # =========================================================
    # COMBUSTÍVEL
    # =========================================================

    fuel = _has_any(q, [
        "combust",
        "abastec",
        "gasolina",
        "diesel",
        "litro",
        "litros"
    ])

    asks_cost = _has_any(q, [
        "gasto",
        "gastou",
        "gastar",
        "gasta",
        "gastei",
        "custo",
        "custou",
        "custa",
        "valor",
        "preco",
        "preço"
    ])

    asks_km = _has_any(q, [
        "quilometro",
        "quilometros",
        "km",
        "distancia",
        "distância"
    ])

    asks_average = _has_any(q, [
        "media",
        "média",
        "medio",
        "médio",
        "por km",
        "cada km"
    ])

    asks_consumption = _has_any(q, [
        "consumo",
        "km/l",
        "km por litro",
        "quilometros por litro",
        "quilômetros por litro"
    ])

    # =========================================================
    # CUSTO MÉDIO DE COMBUSTÍVEL POR KM
    # =========================================================

    if fuel and asks_cost and (asks_km or asks_average):

        value = _fuel_cost_per_km()

        if value is None:
            return NO_DATA_MESSAGE

        return (
            "O custo médio de combustível por quilômetro "
            f"registrado na base é de {money(value)} por km."
        )

    # =========================================================
    # CONSUMO MÉDIO KM/L
    # =========================================================

    if fuel and asks_consumption:

        value = _fuel_average()

        if value is None:
            return NO_DATA_MESSAGE

        return (
            f"O consumo médio registrado na base é de "
            f"{value:.2f} km/l."
        )

    # =========================================================
    # GASTO TOTAL COM COMBUSTÍVEL
    # =========================================================

    if fuel and asks_cost:

        value = query_one("""
            SELECT ROUND(SUM(valor_total), 2)
            FROM abastecimentos
        """)

        if value is None:
            return NO_DATA_MESSAGE

        return (
            "O gasto total com combustível registrado na base "
            f"é de {money(value)}."
        )

    # =========================================================
    # QUANTIDADE DE COMBUSTÍVEL
    # =========================================================

    if fuel and _has_any(q, [
        "litro",
        "litros",
        "quantidade"
    ]):

        value = query_one("""
            SELECT ROUND(SUM(quantidade_litros), 2)
            FROM abastecimentos
        """)

        if value is None:
            return NO_DATA_MESSAGE

        return (
            f"Foram registrados {value:.2f} litros "
            "de combustível na base."
        )

    # =========================================================
    # QUILOMETRAGEM TOTAL
    # =========================================================

    asks_km_total = _has_any(q, [
        "quantos quilômetros",
        "quantos quilometros",
        "quilometragem",
        "quilometragem total",
        "distância total",
        "distancia total",
        "km total",
        "quantos km",
        "total de km",
        "total percorrido",
        "quanto foi percorrido",
        "quanto percorreu"
    ])

    if asks_km_total:

        value = query_one("""
            SELECT ROUND(SUM(km_realizado), 2)
            FROM viagens
            WHERE km_realizado IS NOT NULL
        """)

        if value is None:
            return NO_DATA_MESSAGE

        return (
            f"A quilometragem total registrada na base foi de "
            f"{value:.2f} km."
        )

    # =========================================================
    # ATENDIMENTOS / ATRASOS
    # =========================================================

    if _has_any(q, [
        "atraso",
        "atrasou",
        "chegou atrasado",
        "fora do prazo"
    ]):

        if not _has_any(q, [
            "atendimento",
            "cliente",
            "local"
        ]):
            return AMBIGUOUS_DELAY_MESSAGE

        value = _delay_minutes()

        if value is None:
            return NO_DATA_MESSAGE

        return (
            f"O maior atraso de atendimento registrado "
            f"foi de {value} minutos."
        )

    # =========================================================
    # VIAGENS
    # =========================================================

    if _has_any(q, [
        "viagem",
        "viagens",
        "rota",
        "rotas"
    ]):

        if _has_any(q, [
            "quantas",
            "quantidade",
            "total",
            "numero",
            "número"
        ]):

            value = query_one("""
                SELECT COUNT(*)
                FROM viagens
            """)

            if value is None:
                return NO_DATA_MESSAGE

            return (
                f"Existem {value} viagens registradas "
                "na Base de Conhecimento."
            )

    # =========================================================
    # VEÍCULOS
    # =========================================================

    if _has_any(q, [
        "veiculo",
        "veículos",
        "placa",
        "frota"
    ]):

        if _has_any(q, [
            "mais km",
            "maior distancia",
            "maior distância",
            "rodou mais",
            "percorreu mais"
        ]):

            rows = query_rows("""
                SELECT
                    ve.placa,
                    SUM(v.km_realizado) AS km_total
                FROM viagens v
                JOIN veiculos ve
                    ON ve.id_veiculo = v.id_veiculo
                GROUP BY
                    ve.id_veiculo,
                    ve.placa
                ORDER BY km_total DESC
                LIMIT 1
            """)

            if not rows:
                return NO_DATA_MESSAGE

            return (
                f"O veículo {rows[0][0]} foi o que percorreu "
                f"mais quilômetros, com "
                f"{rows[0][1]:.0f} km registrados."
            )

    # =========================================================
    # INFORMAÇÕES FORA DA BASE
    # =========================================================

    if _has_any(q, [
        "faturamento",
        "salario",
        "salário",
        "lucro"
    ]):

        return NO_DATA_MESSAGE

    # =========================================================
    # FALLBACK SEGURO
    # =========================================================

    return (
        "Não encontrei dados suficientes na Base de Conhecimento "
        "para responder a essa pergunta com segurança. "
        "Tente reformular a pergunta relacionando-a aos dados "
        "de transporte disponíveis."
    )