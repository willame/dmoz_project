from mysql import connector
import logging


class Connection(object):
    def __init__(self, db_config=None):
        if not db_config:
            raise Exception('Database config not None!')
        # user，password，database，(host, port
        print(db_config)
        self._conn = connector.connect(**db_config)
        self._cursor = self._conn.cursor()

    def __enter__(self):
        return self._cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val:
            self._conn.rollback()
            logging.error('Exception:', exc_val)
        else:
            self._conn.commit()
        self._cursor.close()
        self._conn.close()
        return True


class DB_Utils(object):
    def __init__(self, db_config):
        self._db_config = db_config

    def execute(self, sql, params):
        with Connection(self._db_config) as cursor:
            return cursor.execute(sql, params)

    def execute_many(self, sql, params):
        with Connection(self._db_config) as cursor:
            return cursor.executemany(sql, params)

    def query(self, sql, params=()):
        with Connection(self._db_config) as cursor:
            cursor.execute(sql, params)
            return cursor.fetchall()

