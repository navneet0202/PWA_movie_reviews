import sqlite3


# intially connect to a database to start working
# command -> sqlite3.connect(db_name) -> if the database exists it will connect to
# that db otherwise it create a new db
# initializing the db -> creating tables


# Database file
DB_FILE = "mydatabase.db"


def get_connection():
    """
    Establishes and returns a connection to the SQLite database.
    """
    conn = sqlite3.connect(DB_FILE)
    print(conn, "conn")

    # Enable dictionary-style row access
    # dictionary (type of data structure) -> {key: value} -> {row1: ["name", "password"]}, {row2: ["name", "password"]}
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """
    Initializes the database and creates tables if they don't exist.
    """
    conn = get_connection()
    cursor = conn.cursor()
    # cursor is acting as an interface to execute the sql queries/commands like execute, update, insert, delete etc

    # Create a 'users' table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users2 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            name TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """
    )

    # Create a 'reviews' table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            review_date TEXT NOT NULL,
            user_name TEXT NOT NULL,
            rating INTEGER CHECK(rating >= 1 AND rating <= 5),
            review_text TEXT NOT NULL
        )
    """
    )

    conn.commit()
    # saving
    conn.close()


def execute_query(query, params=()):
    """
    Executes a query (INSERT, UPDATE, DELETE).
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    conn.close()


def fetch_all(query, params=()):
    """
    Fetches all rows from a SELECT query.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.commit()
    conn.close()
    return rows
