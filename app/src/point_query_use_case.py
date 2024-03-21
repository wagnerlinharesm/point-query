import os
from app.src.fetch_user_name_password import fetch_username_password
import psycopg2
import json


def execute(id_funcionario):
    try:
        username, password = fetch_username_password(os.getenv("DB_SECRET"))
        database = {
            'dbname': 'pointdb',
            'user': username,
            'password': password,
            'host': os.getenv('DB_HOST')
        }
        conn = psycopg2.connect(**database)
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