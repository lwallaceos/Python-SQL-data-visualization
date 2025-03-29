from database import create_connection


def get_top_titles(limit=10):
    conn = create_connection()
    query = f"SELECT job_title, COUNT(*) as count FROM jobs GROUP BY job_title ORDER BY count DESC LIMIT {limit}"
    result = conn.execute(query).fetchall()
    conn.close()
    return result


def get_location_distribution():
    conn = create_connection()
    query = "SELECT location, COUNT(*) as count FROM jobs GROUP BY location ORDER BY count DESC"
    result = conn.execute(query).fetchall()
    conn.close()
    return result
