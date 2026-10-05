"""Repository layer: all SQL lives here. Returns model objects."""
from features.student.model import Student


class Repository:
    def __init__(self, conn):
        self.conn = conn

    # students
    def find_student(self, name):
        r = self.conn.execute("SELECT * FROM students WHERE lower(name)=lower(?)", (name,)).fetchone()
        return Student(**dict(r)) if r else None

    def create_student(self, name, avatar):
        with self.conn:
            cur = self.conn.execute("INSERT INTO students(name,avatar) VALUES(?,?)", (name, avatar))
        return Student(cur.lastrowid, name, avatar)