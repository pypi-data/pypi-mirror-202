"""
  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

     https://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
"""
from typing import Tuple, Optional, Any
from contextlib import contextmanager
from dataclasses import dataclass
import dmPython
import dbt.exceptions
from dbt.adapters.base import Credentials
from dbt.adapters.sql import SQLConnectionManager
from dbt.contracts.connection import AdapterResponse
from dbt.events import AdapterLogger
import time

logger = AdapterLogger("dameng")


@dataclass
class DamengAdapterCredentials(Credentials):
    """Collect Dameng credentials

    An DamengConnectionMethod is inferred from the combination
    of parameters profiled in the profile.
    """
    # Mandatory required arguments.
    host: str
    port: int
    user: str
    password: str
    database: str

    _ALIASES = {
        'server': 'host',
        'dbname': 'database',
        'pass': 'password',
    }

    @property
    def type(self):
        """Return name of adapter."""
        return 'dameng'

    @property
    def unique_field(self):
        """
        Hashed and included in anonymous telemetry to track adapter adoption.
        Pick a field that can uniquely identify one team/organization building with this adapter
        """
        return self.host

    def _connection_keys(self) -> Tuple[str]:
        """
        List of keys to display in the `dbt debug` output. Omit password.
        """
        return ('host',
                'port',
                'user',
                'database',
                'schema'
                )


class DamengAdapterConnectionManager(SQLConnectionManager):
    TYPE = 'dameng'

    @classmethod
    def open(cls, connection):
        if connection.state == 'open':
            logger.debug('Connection is already open, skipping open.')
            return connection
        credentials = cls.get_credentials(connection.credentials)

        conn_config = {
            'user': credentials.user,
            'password': credentials.password,
            'host': credentials.host,
            'port': credentials.port,
            'schema': credentials.database
        }

        try:
            handle = dmPython.connect(**conn_config)
            connection.handle = handle
            connection.state = 'open'
        except dmPython.Error as e:
            logger.info(f"Got an error when attempting to open an dameng "
                        f"connection: '{e}'")
            connection.handle = None
            connection.state = 'fail'

            raise dbt.exceptions.FailedToConnectError(str(e))

        return connection

    @classmethod
    def cancel(cls, connection):
        """
        cancel is an instance method that gets a connection object and attempts to cancel any ongoing queries,
        which is database dependent. Some databases don't support the concept of cancellation,
        they can simply implement it via 'pass' and their adapter classes should
        implement an is_cancelable that returns False - On ctrl+c connections may remain running.
        This method must be implemented carefully,
        as the affected connection will likely be in use in a different thread.
        """
        connection = connection.handle

        try:
            dmPython.Connection.close(connection)
            logger.info("Canceled dameng connection !")
        except Exception as e:
            logger.error('Error closing connection for cancel request')
            raise Exception(str(e))

    @classmethod
    def get_status(cls, cursor):
        """
        返回最近一次执行的 sql 语句，
        :param cursor:
        :return:
        """
        # return cursor.statement
        return 'ok'

    @classmethod
    def get_response(cls, cursor) -> AdapterResponse:
        # number of rows fetched for a SELECT statement or
        # have been affected by INSERT, UPDATE, DELETE and MERGE statements
        code = cursor.statement
        rows = cursor.rowcount
        status_message = f"{code} {rows}"
        return AdapterResponse(_message=status_message, code=code, rows_affected=rows)

    @contextmanager
    def exception_handler(self, sql: str):
        try:
            yield
        except dmPython.DatabaseError as e:
            logger.debug('Dameng error: {}'.format(str(e)))
            try:
                # attempt to release the connection
                self.release()
            except dmPython.DatabaseError:
                logger.debug("Failed to release connection!")
                pass
            raise dbt.exceptions.DbtDatabaseError(str(e).strip()) from e

        except Exception as e:
            logger.debug("Error running SQL: {}", sql)
            logger.debug("Rolling back transaction.")
            self.release()
            if isinstance(e, dbt.exceptions.DbtRuntimeError):
                # during a sql query, an internal to dbt exception was raised.
                # this sounds a lot like a signal handler and probably has
                # useful information, so raise it without modification.
                raise e

            raise dbt.exceptions.DbtRuntimeError(str(e)) from e

    @classmethod
    def get_credentials(cls, credentials):
        return credentials

    def add_query(
            self,
            sql: str,
            # auto_begin: bool = True,
            auto_begin: bool = False,
            bindings: Optional[Any] = {},
            abridge_sql_log: bool = False
    ) -> Tuple[dmPython.Connection, Any]:
        connection = self.get_thread_connection()
        if auto_begin and connection.transaction_open is False:
            self.begin()
        # logger.debug('Using {} connection "{}".'.format(self.TYPE, connection.name))
        # logger.debug('add_query sql ->{}'.format(sql))

        with self.exception_handler(sql):
            # if abridge_sql_log:
            #     log_sql = '{}...'.format(sql[:512])
            # else:
            #     log_sql = sql

            # logger.debug('log_sql: {}'.format(log_sql))

            # pre = time.time()
            cursor = connection.handle.cursor()
            try:
                logger.debug('add_query sql-->[{0}],bindings-->[{1}]'.format(sql, bindings))
                if 'BEGIN' not in sql:
                    cursor.execute(sql, bindings)
            except Exception as ex:
                logger.error(ex)
            # logger.debug(f"execute {self.get_status(cursor)} SQL cost {(time.time() - pre)} seconds")
            return connection, cursor

    # def add_begin_query(self):
    #     connection = self.get_thread_connection()
    #     cursor = connection.handle.cursor
    #     return connection, cursor
