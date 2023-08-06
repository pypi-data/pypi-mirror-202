# Copyright (c) 2023 Macrometa Corp All rights reserved.
import json
import time

import psycopg2
from psycopg2 import OperationalError
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2.pool import SimpleConnectionPool


class DB:
    def __init__(
            self, user: str, password: str, host: str, port: str, database: str = 'c8cws'
    ) -> None:
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database
        self.try_create_tables(database, host, password, port, user, 20)
        self.pool = SimpleConnectionPool(
            1, 25, user=user,
            password=password,
            host=host,
            port=port,
            database=database)

    @staticmethod
    def try_create_tables(database, host, password, port, user, max_tries):
        cursor, con = None, None
        backoff = 2
        done = False
        for i in range(max_tries):
            backoff = (i + 1) * backoff
            try:
                con = psycopg2.connect(user=user, password=password, host=host, port=port, database=database)
                con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
                cursor = con.cursor()
                cursor.execute("CREATE TABLE workflow (uuid TEXT PRIMARY KEY, federation TEXT,"
                               " tenant TEXT, fabric TEXT, bin_workflow BYTEA, state JSONB);")
                done = True
            except OperationalError as e:
                print(f"Unable to connect to the central cloud RDS. {str(e).capitalize().strip()}."
                      f" Retrying in {backoff} seconds ...")
                time.sleep(backoff)
                continue
            except Exception as e:
                print(f"Skipping tables creation. {str(e).capitalize().strip()}.")
                done = True
                break
            finally:
                if cursor is not None:
                    cursor.close()
                if con is not None:
                    con.close()
        if not done:
            raise RuntimeError(f"Unable to connect to the central cloud RDS. "
                               f"Please check RDS connectivity and configurations.")

    def close(
            self
    ) -> None:
        self.pool.closeall()

    def update_state(self, uuid: str, state: object):
        state_json = json.dumps(state)
        conn = self.pool.getconn()
        cursor = conn.cursor()
        query = """
            UPDATE workflow
            SET state = %s
            WHERE uuid = %s;
        """
        cursor.execute(query, (state_json, uuid))
        conn.commit()
        cursor.close()
        self.pool.putconn(conn)

    def get_state(self, uuid: str):
        conn = self.pool.getconn()
        cursor = conn.cursor()
        query = """
            SELECT state
            FROM workflow
            WHERE uuid = %s;
        """
        cursor.execute(query, (uuid,))
        result = cursor.fetchone()
        cursor.close()
        self.pool.putconn(conn)
        if result is not None and result[0] is not None:
            return json.loads(result[0])
        else:
            return None
