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

        query = """SELECT f.id_funcionario, f.email, p.data, pp.hora_entrada, pp.hora_saida, pp.horas_periodo,
                   p.horas_trabalhadas, sp.situacao FROM funcionario f
                   INNER JOIN ponto p ON f.id_funcionario = p.id_funcionario
                   INNER JOIN periodo_ponto pp ON p.id_ponto = pp.id_ponto
                   INNER JOIN situacao_ponto sp ON p.id_situacao_ponto = sp.id_situacao_ponto
                   WHERE f.id_funcionario = %s;"""

        cursor.execute(query, (id_funcionario,))
        result = cursor.fetchall()

        column_names = ["id_funcionario", "email", "data", "hora_entrada", "hora_saida",
                        "horas_periodo", "horas_trabalhadas", "situacao"]

        json_result = [
            dict(zip(column_names, row))
            for row in result
        ]

        cursor.close()
        conn.close()

        return json.dumps(json_result, default=str)

    except Exception as e:
        print(f"Erro: {e}")
        return []