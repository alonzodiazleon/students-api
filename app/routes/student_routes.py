import sqlite3
from flask import Blueprint, jsonify, request, render_template

from app.models.student_model import (
    create_student,
    get_all_students,
    get_student_by_id,
    update_student,
    delete_student,
    get_average_grade
)


student_bp = Blueprint("students", __name__)


def validate_student_data(data, required=True):
    required_fields = ["dni", "name", "age", "grade", "is_approved"]

    if required:
        for field in required_fields:
            if field not in data:
                return f"The field '{field}' is required."

    if "dni" in data and not isinstance(data["dni"], str):
        return "The field 'dni' must be a string."

    if "name" in data and not isinstance(data["name"], str):
        return "The field 'name' must be a string."

    if "age" in data and not isinstance(data["age"], int):
        return "The field 'age' must be an integer."

    if "grade" in data and not isinstance(data["grade"], (int, float)):
        return "The field 'grade' must be a number."

    if "is_approved" in data and not isinstance(data["is_approved"], bool):
        return "The field 'is_approved' must be a boolean."

    return None


@student_bp.route("/students", methods=["POST"])
def add_student():
    data = request.get_json()

    if not data:
        return jsonify({"message": "JSON body is required"}), 400

    error = validate_student_data(data)

    if error:
        return jsonify({"message": error}), 400

    try:
        student = create_student(data)
        return jsonify(student), 201
    except sqlite3.IntegrityError:
        return jsonify({"message": "The dni already exists"}), 400


@student_bp.route("/students", methods=["GET"])
def list_students():
    students = get_all_students()
    return jsonify(students), 200


@student_bp.route("/students/<int:student_id>", methods=["GET"])
def get_student(student_id):
    student = get_student_by_id(student_id)

    if student is None:
        return jsonify({"message": "Student not found"}), 404

    return jsonify(student), 200


@student_bp.route("/students/<int:student_id>", methods=["PUT", "PATCH"])
def edit_student(student_id):
    data = request.get_json()

    if not data:
        return jsonify({"message": "JSON body is required"}), 400

    error = validate_student_data(data, required=False)

    if error:
        return jsonify({"message": error}), 400

    try:
        student = update_student(student_id, data)
    except sqlite3.IntegrityError:
        return jsonify({"message": "The dni already exists"}), 400

    if student is None:
        return jsonify({"message": "Student not found"}), 404

    return jsonify(student), 200


@student_bp.route("/students/<int:student_id>", methods=["DELETE"])
def remove_student(student_id):
    student = delete_student(student_id)

    if student is None:
        return jsonify({"message": "Student not found"}), 404

    return jsonify({
        "message": "Student deleted successfully",
        "student": student
    }), 200


@student_bp.route("/students/bulk", methods=["POST"])
def bulk_insert_students():
    data = request.get_json()

    if not data or not isinstance(data, list):
        return jsonify({"message": "A JSON list is required"}), 400

    created_students = []

    for item in data:
        error = validate_student_data(item)

        if error:
            return jsonify({
                "message": "Invalid student data",
                "error": error,
                "student": item
            }), 400

    try:
        for item in data:
            student = create_student(item)
            created_students.append(student)
    except sqlite3.IntegrityError:
        return jsonify({"message": "One or more dni values already exist"}), 400

    return jsonify(created_students), 201


@student_bp.route("/students/average", methods=["GET"])
def average_grade():
    average = get_average_grade()

    return jsonify({
        "average_grade": round(average, 2)
    }), 200


@student_bp.route("/students/table", methods=["GET"])
def students_table():
    students = get_all_students()
    return render_template("partials/students_table.html", students=students), 200