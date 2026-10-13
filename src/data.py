"""Données en mémoire (pas de base de données)."""
from copy import deepcopy

# État initial : ne jamais le modifier directement
INITIAL_STUDENTS = [
    {
        "id": 1,
        "firstName": "Ahmed",
        "lastName": "Benali",
        "email": "ahmed.benali@example.com",
        "grade": 16.5,
        "field": "informatique",
    },
    {
        "id": 2,
        "firstName": "Sophie",
        "lastName": "Martin",
        "email": "sophie.martin@example.com",
        "grade": 18,
        "field": "mathématiques",
    },
    {
        "id": 3,
        "firstName": "Lucas",
        "lastName": "Dubois",
        "email": "lucas.dubois@example.com",
        "grade": 12,
        "field": "physique",
    },
    {
        "id": 4,
        "firstName": "Inès",
        "lastName": "Khelifi",
        "email": "ines.khelifi@example.com",
        "grade": 14.75,
        "field": "chimie",
    },
    {
        "id": 5,
        "firstName": "Thomas",
        "lastName": "Leroy",
        "email": "thomas.leroy@example.com",
        "grade": 9.5,
        "field": "informatique",
    },
]

# Liste de travail utilisée par l'API
students = deepcopy(INITIAL_STUDENTS)

# Compteur d'ID auto-incrémenté (dict pour éviter le "global" que pylint signale)
_state = {"next_id": len(INITIAL_STUDENTS) + 1}


def get_next_id():
    """Retourne un nouvel ID unique et incrémente le compteur."""
    new_id = _state["next_id"]
    _state["next_id"] += 1
    return new_id


def reset_students():
    """Remet les étudiants et le compteur d'ID à l'état initial."""
    students.clear()
    students.extend(deepcopy(INITIAL_STUDENTS))
    _state["next_id"] = len(INITIAL_STUDENTS) + 1
