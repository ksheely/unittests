from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from db import get_connection

app = FastAPI(title="FastAPI + psycopg2 Example")


class StudentCreate(BaseModel):
    first_name: str
    last_name: str
    email: str


@app.get("/")
def read_root():
    return {"message": "FastAPI with PostgreSQL and psycopg2 is running"}


@app.get("/students")
def get_students():
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("SELECT id, first_name, last_name, email FROM students ORDER BY id;")
        students = cur.fetchall()
        return students
    finally:
        cur.close()
        conn.close()


@app.get("/students/{student_id}")
def get_student(student_id: int):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            "SELECT id, first_name, last_name, email FROM students WHERE id = %s;",
            (student_id,)
        )
        student = cur.fetchone()

        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        return student
    finally:
        cur.close()
        conn.close()


@app.post("/students")
def create_student(student: StudentCreate):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            """
            INSERT INTO students (first_name, last_name, email)
            VALUES (%s, %s, %s)
            RETURNING id, first_name, last_name, email;
            """,
            (student.first_name, student.last_name, student.email)
        )
        new_student = cur.fetchone()
        conn.commit()
        return new_student
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close()
        conn.close()


@app.put("/students/{student_id}")
def update_student(student_id: int, student: StudentCreate):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            """
            UPDATE students
            SET first_name = %s, last_name = %s, email = %s
            WHERE id = %s
            RETURNING id, first_name, last_name, email;
            """,
            (student.first_name, student.last_name, student.email, student_id)
        )
        updated_student = cur.fetchone()

        if not updated_student:
            raise HTTPException(status_code=404, detail="Student not found")

        conn.commit()
        return updated_student
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close()
        conn.close()


@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            "DELETE FROM students WHERE id = %s RETURNING id;",
            (student_id,)
        )
        deleted = cur.fetchone()

        if not deleted:
            raise HTTPException(status_code=404, detail="Student not found")

        conn.commit()
        return {"message": f"Student {student_id} deleted"}
    finally:
        cur.close()
        conn.close()