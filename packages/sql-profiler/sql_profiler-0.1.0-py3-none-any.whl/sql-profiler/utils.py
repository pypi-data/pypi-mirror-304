import logging
import json

def setup_logging(log_file='sql_profiler.log'):
    """
    Sets up logging configuration for the package.

    :param log_file: The file where logs should be written.
    """
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logging.info("Logging is set up.")


def parse_query_results(results):
    """
    Parses and formats the results from a database query.

    :param results: The raw results from the database cursor.
    :return: A list of dictionaries representing the query results.
    """
    formatted_results = []
    for row in results:
        formatted_results.append(dict(row))
    return formatted_results


def format_alert_message(query, execution_time, threshold):
    """
    Formats an alert message for long-running queries.

    :param query: The SQL query string that was executed.
    :param execution_time: The execution time of the query.
    :param threshold: The threshold time for alerts.
    :return: A formatted alert message string.
    """
    return (
        f"Alert: The query '{query}' took {execution_time:.2f} seconds to execute, "
        f"which exceeds the threshold of {threshold} seconds."
    )


def save_results_to_file(results, file_path='query_results.json'):
    """
    Saves the query results to a JSON file.

    :param results: The results of the SQL query to save.
    :param file_path: The file path where the results should be saved.
    """
    with open(file_path, 'w') as file:
        json.dump(results, file, indent=4)
    logging.info(f"Query results saved to {file_path}.")
