import re

def is_select_query(query):
    """
    Check if the given query is a valid SELECT statement.

    This function checks if the provided query is a SELECT statement by matching
    against regular expressions for SELECT and forbidden SQL commands such as
    DROP, DELETE, INSERT, UPDATE, ALTER, CREATE, and TRUNCATE. It simplifies the
    query text by removing extra whitespace before performing the match.

    Args:
        query (str): The SQL query to be checked.

    Returns:
        bool: True if the query is a valid SELECT statement, False otherwise.
    """
    forbidden_pattern = r'\b(DROP|DELETE|INSERT|UPDATE|ALTER|CREATE|TRUNCATE)\b'
    select_pattern = r'\bSELECT\b'
    query_simplified = re.sub(r'\s+', ' ', query.strip())
    
    if re.search(forbidden_pattern, query_simplified, re.IGNORECASE):
        return False
    return bool(re.search(select_pattern, query_simplified, re.IGNORECASE))