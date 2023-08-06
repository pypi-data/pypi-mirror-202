import psycopg2
from re import findall
from logging import info, warning
from sqlalchemy import create_engine
from typing import Type
from os import environ
from .Helper import psql_insert_copy,timing

@timing
def load_cloud(df:Type,bot:str) -> None:
    """
    Ira fazer o processo de carregamento para o RDS depois de processado.
    """
    engine_alchemy = create_engine(f"postgresql://tracking:{environ['SQL_PET_PASSWORD']}@pet-avi-chatbot-tracking-db.clarobrasil.mobi:5432/clean_data")
    tries = 10
    for _ in range(tries):
        try:
            df.to_sql(f'{bot}_tracking_treated',engine_alchemy,if_exists = 'append',method = psql_insert_copy,index = False,chunksize = 10000)
            break
        except (Exception,psycopg2.Error) as error:
            warning("Fazendo novo conexao com a clean data para adicionar coluna!")
            engine = psycopg2.connect(
                database = 'clean_data',
                user = 'tracking',
                password = environ['SQL_PET_PASSWORD'],
                host = 'pet-avi-chatbot-tracking-db.clarobrasil.mobi',
                port = '5432',
            )
            cursor = engine.cursor()
            column = findall('"(.*?)"',str(error))[0]
            warning(f"Tive que acrescentar mais uma coluna ao seu dataframe ja existente a coluna foi {column}")
            query = f"""
            ALTER TABLE {bot}_tracking_treated
            ADD COLUMN {column} VARCHAR NULL;
            """
            info(query)
            cursor.execute(query)
            engine.commit()
            # Sempre fazer esse commit pelo amor
            tries -= 1
        if tries == 0:
            warning("E não deu eu puis maximo de colunas que podia")