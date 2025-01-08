import sqlite3


class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY,
            Name TEXT NOT NULL,
            Username TEXT,
            Phone TEXT NOT NULL,
            score INTEGER, 
            passed TEXT 
        );
        """
        self.execute(sql, commit=True)

    def add_user(self, id: int, name: str, username: str, phone: str, score=0, passed=False):
        sql = """
        INSERT INTO Users (id, Name, Username, Phone, Score, Passed) VALUES (?, ?, ?, ?, ?, ?)
        """
        self.execute(sql, parameters=(id, name, username, phone, score, passed), commit=True)

    def update_user(self, id: int, score: int, passed: bool):
        sql = """
        UPDATE Users
        SET score = ?, passed = ?
        WHERE id = ?
        """
        self.execute(sql, parameters=(score, passed, id), commit=True)

    def select_all_users(self):
        sql = """
        SELECT * FROM Users
        """
        return self.execute(sql, fetchall=True)

    def select_user(self, user_id: int):
        sql = "SELECT * FROM Users WHERE id = ?"
        return self.execute(sql, parameters=(user_id,), fetchone=True)

    # def select_test_results(self, user_id: int):
    #     sql = """
    #     SELECT * FROM Tests WHERE user_id = ?
    #     """
    #     return self.execute(sql, parameters=(user_id,), fetchall=True)

    def delete_user(self, id: int):
        sql = """
        DELETE FROM Users WHERE id = ?
        """
        self.execute(sql, parameters=(id,), commit=True)

    def delete_all_users(self):
        sql = """
        DELETE FROM Users
        """
        self.execute(sql, commit=True)

    #
    # def delete_all_tests(self):
    #     sql = """
    #     DELETE FROM Tests
    #     """
    #     self.execute(sql, commit=True)

    def user_exists(self, user_id: int):
        """Check if the user exists in the database."""
        user = self.select_user(id=user_id)
        return user is not None

    def user_test_passed(self, user_id: int):
        """Check if the user has passed the test."""
        results = self.select_test_results(user_id)
        if results:
            return any(result['passed'] == 'yes' for result in results)
        return False
