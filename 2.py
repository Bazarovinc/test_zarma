import sqlite3
from typing import Final

DB: Final[str] = "test.sqlite"


def main():
    connection = sqlite3.connect(DB)
    cursor = connection.cursor()
    cursor.execute("""SELECT name, age FROM users WHERE age > 30;""")
    users = cursor.fetchall()
    for user in users:
        print(user)


if __name__ == "__main__":
    main()
