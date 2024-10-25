# sql_profiler/query_profiler.py
import time
import logging

class QueryProfiler:
    def __init__(self, connection):
        """
        Initializes the query profiler.

        :param connection: The database connection object
        """
        self.connection = connection

    def execute_query(self, query):
        """
        Executes a given SQL query and measures its execution time.

        :param query: The SQL query to execute
        :return: The result of the executed query
        """
        start_time = time.time()
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
        execution_time = time.time() - start_time
        logging.info(f'Query: {query}, Execution time: {execution_time:.2f} seconds')
        print(f'Query executed in {execution_time:.2f} seconds')
        return result, execution_time
