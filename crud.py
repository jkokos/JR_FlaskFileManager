import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv


load_dotenv()

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME", "documents_db"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "DB_PASSWORD"),
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5433")
}


def get_files_count():
    with psycopg2.connect(**DB_CONFIG) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM dokuments")
            return cursor.fetchone()[0]

def add_file(stored_name, original_name, size_bytes, extension):
    with psycopg2.connect(**DB_CONFIG) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO dokuments
                (stored_name, original_name, size_bytes, extension)
                VALUES (%s, %s, %s, %s)
                RETURNING id
                """,
                (stored_name, original_name, size_bytes, extension)
            )
            return cursor.fetchone()[0]

def get_documents_page(limit, offset):
    with psycopg2.connect(**DB_CONFIG) as connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""
                SELECT
                    id,
                    stored_name,
                    original_name,
                    extension,
                    uploaded_at AT TIME ZONE 'UTC' AS uploaded_at,
                    ROUND(size_bytes / 1024.0, 1) AS size_kb
                FROM dokuments
                ORDER BY uploaded_at DESC, id DESC
                LIMIT %s OFFSET %s
            """, (limit, offset))

            return cursor.fetchall()


def count_documents():
    with psycopg2.connect(**DB_CONFIG) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM dokuments")
            return cursor.fetchone()[0]


def get_file_by_stored_name(stored_name):
    with psycopg2.connect(**DB_CONFIG) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT original_name
                FROM dokuments
                WHERE stored_name = %s
                """,
                (stored_name,)
            )
            return cursor.fetchone()

def get_file_by_id(file_id):
    with psycopg2.connect(**DB_CONFIG) as connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "SELECT stored_name FROM dokuments WHERE id = %s",
                (file_id,)
            )
            return cursor.fetchone()


def remove_file(file_id):
    with psycopg2.connect(**DB_CONFIG) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM dokuments WHERE id = %s",
                (file_id,)
            )


def get_by_query(query):
    with psycopg2.connect(**DB_CONFIG) as connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""
                SELECT
                    id,
                    stored_name,
                    original_name,
                    extension,
                    uploaded_at AT TIME ZONE 'UTC' AS uploaded_at,
                    ROUND(size_bytes / 1024.0, 1) AS size_kb
                FROM dokuments
                WHERE original_name ILIKE %s
                ORDER BY uploaded_at DESC
            """, (f"%{query}%",))

            return cursor.fetchall()