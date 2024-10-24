# db_utils.py
import sys
import pymysql.cursors
from .db_connection import get_db_connection

def get_operation_from_query(query):
    """
    Determine the SQL operation (e.g., 'select', 'insert', 'update', 'delete') from the query.
    """
    operation = query.strip().split()[0].lower()
    return operation

def rds_execute(query, params=None):
    """
    Execute a query on the RDS database.
    """
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            if isinstance(params, list) and (all(isinstance(i, tuple) for i in params) or all(isinstance(i, list) for i in params)):
                cursor.executemany(query, params)
            else:
                cursor.execute(query, params or {})
            operation = get_operation_from_query(query)
            if operation in ['insert', 'update', 'delete']:
                connection.commit()
            if operation == 'select':
                return cursor.fetchall()
    except pymysql.OperationalError as op_err:
        print(f'Error In DB Query query: {query}')
        raise
    except Exception as e:
        print(f'Error In DB Query query: {query}')
        raise

# Make the function available in the module
sys.modules[__name__] = rds_execute
