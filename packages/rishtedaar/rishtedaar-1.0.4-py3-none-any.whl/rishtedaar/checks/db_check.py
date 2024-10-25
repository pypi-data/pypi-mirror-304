from django.db import connection

def check_db():
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchall()  # Fetch results to ensure the query executes
        return True, "Database connection is healthy"
    except Exception as e:
        return False, f"Database error: {str(e)}"
