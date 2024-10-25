# sql_profiler/suggestions.py
class SuggestionGenerator:
    def suggest_index(self, query):
        """
        Suggests index creation based on the query structure.

        :param query: The SQL query to analyze
        :return: A suggestion string
        """
        if "WHERE" in query.upper():
            print("Consider adding an index to the columns used in the WHERE clause.")
            return "Add index to columns used in the WHERE clause"
        return "No suggestions available."
