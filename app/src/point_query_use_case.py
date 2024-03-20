# from app.psycopg2 import connect
import os
from fetch_user_name_password import fetch_username_password


def execute(matricula):
    try:
        # username, password = fetch_username_password(os.getenv("DB_SECRET"))
        # database = {
        #     'dbname': 'pointdb',
        #     'user': username,
        #     'password': password,
        #     'host': os.getenv('DB_HOST')
        # }
        # conn = connect(**database)
        # cursor = conn.cursor()
        #
        # query = """SELECT f.matricula, f.email, p.data, pp.hora_entrada, pp.hora_saida, pp.horas_periodo,
        # p.horas_trabalhadas, sp.descricao FROM funcionario f
        # INNER JOIN ponto p ON f.id_funcionario = p.id_funcionario
        # INNER JOIN periodo_ponto pp ON p.id_ponto = pp.id_ponto
        # INNER JOIN situacao_ponto sp ON p.id_situacao_ponto =
        # sp.id_situacao_ponto WHERE f.matricula = %s;"""
        #
        # cursor.execute(query, (matricula,))
        # result = cursor.fetchall()
        #
        # cursor.close()
        # conn.close()
        #
        # print(result)

        return "result"
    except Exception as e:
        print(f"Erro ao acessar banco de dados: {e}")
        return []
