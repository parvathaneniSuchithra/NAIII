import sqlite3
DATABASE_FILE = "quiz_app.db"

def add_timestamp_column():
    """Adds the missing timestamp column to the user_progress table."""
    print("Connecting to the database...")
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    try:
        print("Attempting to add 'timestamp' column to 'user_progress' table...")
        cursor.execute("ALTER TABLE user_progress ADD COLUMN timestamp INTEGER")
        print("✅ Column 'timestamp' added successfully!")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("✅ Column 'timestamp' already exists. No action needed.")
        else:
            print(f"❌ An error occurred: {e}")
    finally:
        conn.commit()
        conn.close()
        print("Database connection closed.")

if __name__ == "__main__":
    add_timestamp_column()