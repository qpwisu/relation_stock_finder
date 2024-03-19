import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.sql import text

class MySQLDataConnector:
    def __init__(self, user, password, host, database, port=3306):
        """ MySQL 데이터베이스 엔진을 초기화합니다. """
        self.engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}')

    def upload_dataframe(self, df, table_name, if_exists='append', index=False):
        """ DataFrame 데이터를 MySQL 테이블에 업로드합니다. """
        try:
            df.to_sql(name=table_name, con=self.engine, if_exists=if_exists, index=index)
            print(f"Data uploaded successfully to {table_name}.")
        except Exception as e:
            print(f"Error uploading data: {e}")

    # 데이터베이스에 데이터 업로드
    def update_politician_dataframe(self, df, table_name):
        for _, row in df.iterrows():
            name = row['name']
            party = row['party']
            # 쿼리 작성
            sql = text("""
                INSERT INTO {} (name, party)
                VALUES (:name, :party)
                ON DUPLICATE KEY UPDATE party=VALUES(party);
            """.format(table_name))  # table_name은 직접 포매팅

            # 쿼리 실행
            with self.engine.connect() as conn:
                conn.execute(sql, {"name": name, "party": party})  # 딕셔너리로 파라미터 전달
                conn.commit()  # 커밋 추가

        print(f"Data uploaded successfully to {table_name}.")

    def select_columns(self,table_name,column_names = "*"):
        if column_names != "*":
            column_names = ",".join(column_names)

        query = f"SELECT {column_names} FROM {table_name}"
        try:
            df = pd.read_sql_query(query, self.engine)
            return df
        except Exception as e:
            print(f"Error downloading data: {e}")
            return None

    def default_query(self,query):
        try:
            df = pd.read_sql_query(query, self.engine)
            return df
        except Exception as e:
            print(f"Error downloading data: {e}")
            return None


    def search_last_date(self,table_name):
        query = f"SELECT max(date) FROM {table_name};"
        try:
            df = pd.read_sql_query(query, self.engine)
            return df.values[0][0]
        except Exception as e:
            print(f"Error downloading data: {e}")
            return None
    def close(self):
        """ 데이터베이스 연결을 종료합니다. """
        self.engine.dispose()
