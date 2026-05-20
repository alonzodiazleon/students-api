# Students API

API REST básica para la gestión de estudiantes desarrollada con Python, Flask y SQLite.

## Objetivo

Este proyecto permite gestionar estudiantes mediante una API REST. Incluye operaciones CRUD, inserción masiva, cálculo del promedio de notas y renderizado de una tabla HTML parcial.

## Tecnologías utilizadas

- Python
- Flask
- SQLite
- JSON
- HTML parcial para HTMX

## Estructura del proyecto

```text
students-api/
│── app/
│   │── models/
│   │   └── student_model.py
│   │── routes/
│   │   └── student_routes.py
│   │── templates/
│   │   └── partials/
│   │       └── students_table.html
│   │── __init__.py
│   └── database.py
│── main.py
│── requirements.txt
│── README.md
```

## Instalación

Crear el entorno virtual:

```bash
python -m venv .venv
```

Instalar dependencias:

```bash
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Ejecución

Ejecutar el proyecto:

```bash
.venv\Scripts\python.exe main.py
```

El servidor se ejecutará en:

```text
http://127.0.0.1:5000
```

## Modelo de datos

```json
{
  "id": 1,
  "dni": "12345678",
  "name": "Juan Perez",
  "age": 20,
  "grade": 15.5,
  "is_approved": true,
  "created_at": "timestamp",
  "updated_at": "timestamp"
}
```

## Endpoints

| Método | Ruta | Descripción |
|---|---|---|
| POST | `/students` | Crear un estudiante |
| GET | `/students` | Obtener todos los estudiantes |
| GET | `/students/<id>` | Obtener un estudiante por ID |
| PUT/PATCH | `/students/<id>` | Actualizar un estudiante |
| DELETE | `/students/<id>` | Eliminar un estudiante |
| POST | `/students/bulk` | Crear estudiantes de forma masiva |
| GET | `/students/average` | Obtener promedio de notas |
| GET | `/students/table` | Renderizar tabla HTML parcial |

## Ejemplo para crear estudiante

```json
{
  "dni": "12345678",
  "name": "Juan Perez",
  "age": 20,
  "grade": 15.5,
  "is_approved": true
}
```

## Ejemplo para bulk insert

```json
[
  {
    "dni": "11111111",
    "name": "Ana Torres",
    "age": 21,
    "grade": 18.5,
    "is_approved": true
  },
  {
    "dni": "22222222",
    "name": "Carlos Ruiz",
    "age": 19,
    "grade": 10.5,
    "is_approved": false
  }
]
```

## Consideraciones

- El campo `dni` es obligatorio y único.
- El campo `is_approved` se ingresa manualmente.
- El campo `created_at` se genera automáticamente.
- El campo `updated_at` se actualiza en cada modificación.
- La API maneja respuestas JSON y códigos HTTP adecuados.