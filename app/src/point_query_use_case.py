import os
import psycopg2
import json


def execute(id_funcionario):
    try:
        database = {
            'dbname': 'pointdb',
            'user': os.getenv('POINT_DB_USERNAME'),
            'password': os.getenv('POINT_DB_PASSWORD'),
            'host': os.getenv('DB_HOST')
        }
        conn = psycopg2.connect(**database)
        print(conn)
        cursor = conn.cursor()

        query = """SELECT p.data, pp.hora_entrada, pp.hora_saida, pp.horas_periodo,
                   p.horas_trabalhadas, sp.situacao FROM funcionario f
                   INNER JOIN ponto p ON f.id_funcionario = p.id_funcionario
                   INNER JOIN periodo_ponto pp ON p.id_ponto = pp.id_ponto
                   INNER JOIN situacao_ponto sp ON p.id_situacao_ponto = sp.id_situacao_ponto
                   WHERE f.id_funcionario = %s and p.data = current_date
                   ORDER BY pp.hora_entrada
                   ;"""

        cursor.execute(query, (id_funcionario,))
        result = cursor.fetchall()

        if not result:
            return json.dumps([])  # Retorna um array vazio caso não haja resultados

            # Assumindo que todos os registros de um dia compartilham a mesma data, horas_trabalhadas, e situação
        primeiro_registro = result[0]
        data, horas_trabalhadas, situacao = primeiro_registro[0], primeiro_registro[4], primeiro_registro[5]

        periodos = [
            {
                "entrada": registro[1],
                "saida": registro[2],
                "horas_periodo": registro[3]
            } for registro in result
        ]

        json_result = {
            "data": data,
            "horas_trabalhadas": horas_trabalhadas,
            "status": situacao,
            "periodos": periodos
        }

        cursor.close()
        conn.close()

        return json.dumps(json_result, default=str)

        return json.dumps(json_result, default=str)

    except Exception as e:
        print(f"Erro: {e}")
        return []