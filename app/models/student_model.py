from datetime import datetime
from app.database import get_connection


def row_to_dict(row):
    return {
        "id": row["id"],
        "dni": row["dni"],
        "name": row["name"],
        "age": row["age"],
        "grade": row["grade"],
        "is_approved": bool(row["is_approved"]),
        "created_at": row["created_at"],
        "updated_at": row["updated_at"]
    }


def create_student(data):
    now = datetime.now().isoformat()

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO students (dni, name, age, grade, is_approved, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        data["dni"],
        data["name"],
        data["age"],
        data["grade"],
        data["is_approved"],
        now,
        now
    ))

    connection.commit()
    student_id = cursor.lastrowid
    connection.close()

    return get_student_by_id(student_id)


def get_all_students():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()

    connection.close()

    return [row_to_dict(row) for row in rows]


def get_student_by_id(student_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
    row = cursor.fetchone()

    connection.close()

    if row is None:
        return None

    return row_to_dict(row)


def update_student(student_id, data):
    existing_student = get_student_by_id(student_id)

    if existing_student is None:
        return None

    updated_data = {
        "dni": data.get("dni", existing_student["dni"]),
        "name": data.get("name", existing_student["name"]),
        "age": data.get("age", existing_student["age"]),
        "grade": data.get("grade", existing_student["grade"]),
        "is_approved": data.get("is_approved", existing_student["is_approved"]),
        "updated_at": datetime.now().isoformat()
    }

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE students
        SET dni = ?, name = ?, age = ?, grade = ?, is_approved = ?, updated_at = ?
        WHERE id = ?
    """, (
        updated_data["dni"],
        updated_data["name"],
        updated_data["age"],
        updated_data["grade"],
        updated_data["is_approved"],
        updated_data["updated_at"],
        student_id
    ))

    connection.commit()
    connection.close()

    return get_student_by_id(student_id)


def delete_student(student_id):
    existing_student = get_student_by_id(student_id)

    if existing_student is None:
        return None

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))

    connection.commit()
    connection.close()

    return existing_student


def get_average_grade():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT AVG(grade) AS average_grade FROM students")
    row = cursor.fetchone()

    connection.close()

    average = row["average_grade"]

    if average is None:
        return 0

    return average