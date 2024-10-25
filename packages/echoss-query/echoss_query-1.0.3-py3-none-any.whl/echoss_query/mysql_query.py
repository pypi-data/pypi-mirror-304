import pandas as pd
import pymysql
import pymysql.cursors
from pymysql import MySQLError

from echoss_fileformat import FileUtil, get_logger

logger = get_logger("echoss_query")


class MysqlQuery:
    conn = None
    empty_dataframe = pd.DataFrame()
    use_query_debug = True

    def __init__(self, conn_info: str or dict):
        """
        Args:
            conn_info : configration dictionary
                (ex) conn_info = {
                                'mysql':
                                    {
                                        'user'  : str(user),
                                        'passwd': str(pw),
                                        'host'  : int(ip),
                                        'db'    : str(db_name),
                                        'charset': str(utf8)
                                    }
                            }
        """
        if isinstance(conn_info, str):
            conn_info = FileUtil.dict_load(conn_info)
        elif not isinstance(conn_info, dict):
            raise TypeError("MysqlQuery support type 'str' and 'dict'")
        required_keys = ['user', 'passwd', 'host', 'db', 'charset']
        if (len(conn_info) > 0) and ('mysql' in conn_info) and all(key in conn_info['mysql'] for key in required_keys):
            self.user = conn_info['mysql']['user']
            self.passwd = conn_info['mysql']['passwd']
            self.host = conn_info['mysql']['host']
            self.db = conn_info['mysql']['db']
            self.charset = conn_info['mysql']['charset']
        else:
            logger.debug(f'[MySQL] config info not exist or any required keys are missing {required_keys}')
        try:
            self.conn = self._connect_db()
        except MySQLError as e:
            logger.error(f"mysql connection failed. {self.__str__()} : {e}")

    def __str__(self):
        return f"Mysql(host={self.conn.host}, db={self.conn.db}, charset={self.conn.charset})"

    def query_debug(self, use_debug_query=None):
        """
        :param use_debug_query:  None, True, False
        :return: self.use_debug_query
        """
        if use_debug_query is None:
            logger.debug(f"{self.use_query_debug=}")
        elif use_debug_query is True or use_debug_query is False:
            self.use_query_debug = use_debug_query
        return self.use_query_debug

    def conn_info(self):
        """
        Args:
        Returns:
            tuple : connection information(host_info, db_info, charset_info)
        """
        return self.conn.host, self.conn.db, self.conn.charset

    def _parsing(self, query: str, params=None) -> str:
        if ';' not in query:
            query = query + ';'
        if params:
            cur = self.conn_cursor()
            result_query = cur.mogrify(query, params)
        else:
            result_query = query
        if self.use_query_debug:
            logger.debug(result_query)
        return result_query

    def _connect_db(self):
        try:
            self.conn = pymysql.connect(
                user=self.user,
                passwd=self.passwd,
                host=self.host,
                db=self.db,
                charset=self.charset,
                cursorclass=pymysql.cursors.DictCursor,
                autocommit=False
            )
            logger.info(f"[MySQL] DB Connection established.")
            return self.conn
        except MySQLError as e:
            logger.error(f"[MySQL] DB Connection Exception : {e}")
            raise

    def conn_cursor(self, cursorclass=None):
        try:
            if not self.conn.open:
                self.conn.ping(reconnect=True)
        except MySQLError as e:
            logger.error(f"Error ping mysql: {e}. Reconnecting...")
            self.conn = self._connect_db()

        try:
            if self.conn.open:
                return self.conn.cursor(cursor=cursorclass)
        except pymysql.MySQLError as e:
            logger.error(f"Error get connection cursor: {e}")
        raise ConnectionError('Connection MySql Cursor Error')

    def ping(self):
        """
        Args:

        Returns:
            str : DB Status
        """
        if self.conn.open:
            logger.debug(f'[MySQL] database {self.__str__()} connection success')
        else:
            raise ConnectionError(f'database {self.__str__()} connection fail')

    def databases(self) -> pd.DataFrame:
        """
        Args:
        Returns:
            pd.DataFrame() : database dataframe
        """
        cur = self.conn_cursor()
        cur.execute('SHOW DATABASES;')
        result = cur.fetchall()

        if result:
            return pd.DataFrame(result, columns=[desc[0] for desc in cur.description])
        else:
            logger.debug("[MySQL] can't find database")
            return self.empty_dataframe

    def tables(self) -> pd.DataFrame:
        """
        Returns:
            pd.DataFrame() : table dataframe
        """
        cur = self.conn_cursor()
        cur.execute('SHOW TABLES;')
        result = cur.fetchall()

        if result != ():
            return pd.DataFrame(result, columns=[desc[0] for desc in cur.description])
        else:
            logger.debug("[MySQL] can't find tables")
            return self.empty_dataframe

    # ##################################3###
    #  Table method
    # ######################################
    def create(self, query_str: str) -> None:
        """
        Args:
            query_str(str) : MySQL create query string
        """
        query = self._parsing(query_str)
        keyword = 'CREATE'
        if keyword in query or keyword.lower() in query:
            try:
                cur = self.conn_cursor()
                cur.execute(query)
                self.conn.commit()
            except MySQLError as e:
                logger.debug(f"[MySQL] Create Exception : {e}")
        else:
            raise ValueError('input is not include "create"')

    def drop(self, query_str: str) -> None:
        """
        Args:
            query_str(str) : MySQL drop query string
        """
        query = self._parsing(query_str)
        keyword = 'DROP'
        if keyword in query or keyword.lower() in query:
            try:
                cur = self.conn_cursor()
                cur.execute(query)
                self.conn.commit()
            except MySQLError as e:
                logger.debug(f"[MySQL] Drop Exception : {e}")
        else:
            raise ValueError('input is not include "drop"')

    def truncate(self, query_str: str) -> None:
        """
        Args:
            query_str(str) : MySQL truncate query string
        """
        query = self._parsing(query_str)
        keyword = 'TRUNCATE'
        if keyword in query or keyword.lower() in query:
            try:
                cur = self.conn_cursor()
                cur.execute(query)
                self.conn.commit()
            except MySQLError as e:
                logger.debug(f"[MySQL] Truncate Exception : {e}")
        else:
            raise ValueError('input is not include "truncate"')

    def alter(self, query_str: str) -> None:
        """
        Args:
            query_str(str) : MySQL alter query string
        """
        query = self._parsing(query_str)
        keyword = 'ALTER'
        if keyword in query or keyword.lower() in query:
            try:
                cur = self.conn_cursor()
                cur.execute(query)
                self.conn.commit()
            except MySQLError as e:
                logger.debug(f"[MySQL] Alter Exception : {e}")
        else:
            raise ValueError('input is not include "alter"')

    # ##################################3###
    #  Quqery method
    # ######################################

    def select_one(self, query_str: str, params=None):
        """
        Args:
            query_str(str): MySQL select query string that returns a single row
            params: query string format parameters like % style
        Returns:
            dict: A single dictionary result from the query
        """
        query = self._parsing(query_str, params)
        keyword = 'SELECT'

        if keyword in query or keyword.lower() in query:
            try:
                cur = self.conn_cursor()
                cur.execute(query)
                result = cur.fetchone()
                if result:
                    return result
                else:
                    logger.debug("[MySQL] No data found")
                    return {}
            except MySQLError as e:
                logger.debug(f"[MySQL] SELECT Exception: {e}")
                return {}
        else:
            raise ValueError('Input does not include "SELECT"')

    def select_list(self, query_str: str, params=None) -> list:
        """
        Args:
            query_str(str) : MySQL select query string
            params: query string format parameters like % style
        Returns:
            list() : List of query result
        """
        query = self._parsing(query_str, params)
        keyword = 'SELECT'

        if keyword in query or keyword.lower() in query:
            try:
                cur = self.conn_cursor()
                cur.execute(query)
                result = cur.fetchall()

                if result is None:
                    logger.debug("[MySQL] data not exist")
                    result_list = None
                elif isinstance(result, list):
                    result_list = result
                else:
                    result_list = [result]
                return result_list
            except MySQLError as e:
                logger.debug(f"[MySQL] SELECT_LIST Exception : {e}")
                return []
        else:
            raise ValueError('input is not include "select"')

    def select(self, query_str: str, params=None) -> pd.DataFrame:
        """
        Args:
            query_str(str) : MySQL select query string
            params: query string format parameters like % style
        Returns:
            pd.DataFrame() : DataFrame of query result
        """
        query = self._parsing(query_str, params)
        keyword = 'SELECT'

        if keyword in query or keyword.lower() in query:
            try:
                cur = self.conn_cursor()
                cur.execute(query)
                result = cur.fetchall()

                if result:
                    return pd.DataFrame(result)
                else:
                    logger.debug(f"[MySQL] data not exist")
            except MySQLError as e:
                logger.debug(f"[MySQL] SELECT Exception : {e}")
                return self.empty_dataframe
        else:
            raise ValueError('input is not include "select"')

    def faster_select(self, query_str: str, params=None, fetch_size=1000) -> pd.DataFrame:
        """
        Args:
            query_str(str) : MySQL select query string better than normal select
            params: query string format parameters like % style
        Returns:
            pd.DataFrame() : DataFrame of query result
        """
        query = self._parsing(query_str, params)
        keyword = 'SELECT'
        if keyword in query or keyword.lower() in query:
            results = []
            try:
                cur = self.conn_cursor(pymysql.cursors.SSCursor)
                cur.execute(query)
                while True:
                    rows = cur.fetchmany(fetch_size)
                    if not rows:
                        break
                    results.extend(rows)

                if len(results) > 0:
                    return pd.DataFrame(results, columns=[desc[0] for desc in cur.description])
                else:
                    logger.debug(f"[MySQL] data not exist")
                    return self.empty_dataframe
            except MySQLError as e:
                logger.debug(f"[MySQL] FASTER_SELECT Exception : {e}")
            self.close()
        else:
            raise ValueError('input is not include "select"')

    def insert(self, query_str: str, params=None) -> int:
        """
        Args:
            query_str(str) : MySQL insert query string
            params : query string format parameters like % style, tuple or  list of tuple
        Returns:
            pd.DataFrame() : DataFrame of query result
        """
        query = self._parsing(query_str, params)
        keyword = 'INSERT'
        if keyword in query or keyword.lower() in query:
            try:
                cur = self.conn_cursor()
                if isinstance(params, list):
                    cur.executemany(query)
                else:
                    cur.execute(query)
                logger.debug(f"[MySQL] INSERT {cur.rowcount} rows")
                self.conn.commit()
                return cur.rowcount
            except MySQLError as e:
                self.conn.rollback()
                logger.debug(f"[MySQL] INSERT Exception : {e}")
                return 0
        else:
            raise ValueError('input is not include "insert"')

    def update(self, query_str: str, params=None) -> int:
        """
        Args:
            query_str(str) : MySQL update query string
            params: query string format parameters like % style
        Returns:
            pd.DataFrame() : DataFrame of query result
        """
        query = self._parsing(query_str, params)
        keyword = 'UPDATE'
        if keyword in query or keyword.lower() in query:
            try:
                cur = self.conn_cursor()
                if isinstance(params, list):
                    cur.executemany(query)
                else:
                    cur.execute(query)
                logger.debug(f"[MySQL] UPDATE {cur.rowcount} rows")
                self.conn.commit()
                return cur.rowcount
            except MySQLError as e:
                self.conn.rollback()
                logger.debug(f"[MySQL] UPDATE Exception : {e}")
                return 0
        else:
            raise ValueError('input is not include "update"')

    def delete(self, query_str: str, params=None) -> int:
        """
        Args:
            query_str(str) : MySQL delete query string

        Returns:
            pd.DataFrame() : DataFrame of query result
        """
        query = self._parsing(query_str, params)
        keyword = 'DELETE'
        if keyword in query or keyword.lower() in query:
            try:
                cur = self.conn_cursor()
                if isinstance(params, list):
                    cur.executemany(query)
                else:
                    cur.execute(query)
                logger.debug(f"[MySQL] DELETE {cur.rowcount} rows")
                self.conn.commit()
                return cur.rowcount
            except MySQLError as e:
                self.conn.rollback()
                logger.debug(f"[MySQL] DELETE Exception : {e}")
                return 0
        else:
            raise ValueError('input is not include "delete"')

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None
            logger.debug(f"[MySQL] DB Connection closed.")
