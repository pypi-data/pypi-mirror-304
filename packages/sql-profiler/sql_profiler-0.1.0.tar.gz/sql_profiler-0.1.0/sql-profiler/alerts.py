# sql_profiler/alerts.py
class AlertManager:
    def __init__(self, threshold=2.0):
        """
        Initializes the alert manager.

        :param threshold: The execution time threshold for generating an alert
        """
        self.threshold = threshold

    def check_query_time(self, execution_time):
        """
        Checks if a query's execution time exceeds the threshold.

        :param execution_time: The execution time of a query
        :return: True if the time exceeds the threshold, otherwise False
        """
        if execution_time > self.threshold:
            print(f"Alert: Query execution time exceeded the threshold of {self.threshold} seconds.")
            return True
        return False
