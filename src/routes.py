"""Endpoints de l'API Étudiants."""
from typing import Literal

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr, Field

from src.data import get_next_id, students

router = APIRouter(prefix="/students", tags=["students"])


class StudentIn(BaseModel):
    """Corps des requêtes POST et PUT."""

    firstName: str = Field(min_length=2)
    lastName: str = Field(min_length=2)
    email: EmailStr
    grade: float = Field(ge=0, le=20)
    field: Literal["informatique", "mathématiques", "physique", "chimie"]


def _find_student(student_id):
    """Retourne l'étudiant correspondant à l'ID ou lève une 404."""
    for student in students:
        if student["id"] == student_id:
            return student
    raise HTTPException(status_code=404, detail="Étudiant introuvable")


def _email_taken(email, exclude_id=None):
    """Indique si l'email est déjà utilisé par un autre étudiant."""
    return any(
        s["email"].lower() == email.lower() and s["id"] != exclude_id
        for s in students
    )


# ---------- GET /students ----------

@router.get("")
def list_students():
    """Liste tous les étudiants."""
    return students


# /stats et /search DOIVENT être déclarées avant /{student_id}

@router.get("/stats")
def get_stats():
    """Statistiques globales sur les étudiants."""
    if not students:
        return {
            "totalStudents": 0,
            "averageGrade": 0,
            "studentsByField": {},
            "bestStudent": None,
        }

    by_field = {}
    for student in students:
        by_field[student["field"]] = by_field.get(student["field"], 0) + 1

    average = sum(s["grade"] for s in students) / len(students)
    return {
        "totalStudents": len(students),
        "averageGrade": round(average, 2),
        "studentsByField": by_field,
        "bestStudent": max(students, key=lambda s: s["grade"]),
    }


@router.get("/search")
def search_students(q: str | None = None):
    """Recherche par nom ou prénom (insensible à la casse)."""
    if q is None or not q.strip():
        raise HTTPException(status_code=400, detail="Paramètre q requis")

    term = q.strip().lower()
    return [
        s
        for s in students
        if term in s["firstName"].lower() or term in s["lastName"].lower()
    ]


# ---------- GET /students/{id} ----------

@router.get("/{student_id}")
def get_student(student_id: int):
    """Récupère un étudiant par son ID (400 si l'ID n'est pas un entier)."""
    return _find_student(student_id)


# ---------- POST /students ----------

@router.post("", status_code=201)
def create_student(student_in: StudentIn):
    """Crée un étudiant (409 si l'email existe déjà)."""
    if _email_taken(student_in.email):
        raise HTTPException(status_code=409, detail="Email déjà utilisé")

    new_student = {"id": get_next_id(), **student_in.model_dump()}
    students.append(new_student)
    return new_student


# ---------- PUT /students/{id} ----------

@router.put("/{student_id}")
def update_student(student_id: int, student_in: StudentIn):
    """Modifie un étudiant existant."""
    student = _find_student(student_id)

    if _email_taken(student_in.email, exclude_id=student_id):
        raise HTTPException(status_code=409, detail="Email déjà utilisé")

    student.update(student_in.model_dump())
    return student


# ---------- DELETE /students/{id} ----------

@router.delete("/{student_id}")
def delete_student(student_id: int):
    """Supprime un étudiant."""
    student = _find_student(student_id)
    students.remove(student)
    return {"message": f"Étudiant {student_id} supprimé"}