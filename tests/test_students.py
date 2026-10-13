"""Tests de l'API Étudiants (21 tests)."""

VALID_STUDENT = {
    "firstName": "Lina",
    "lastName": "Moreau",
    "email": "lina.moreau@example.com",
    "grade": 15,
    "field": "physique",
}


def make_student(**overrides):
    """Retourne un étudiant valide, avec des champs éventuellement modifiés."""
    return {**VALID_STUDENT, **overrides}


# ---------- GET : lecture (5 tests) ----------

def test_get_students_returns_200_and_list(client):
    response = client.get("/students")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_students_returns_all_initial_students(client):
    response = client.get("/students")
    assert len(response.json()) == 5


def test_get_student_by_id_returns_student(client):
    response = client.get("/students/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_get_student_unknown_id_returns_404(client):
    response = client.get("/students/999")
    assert response.status_code == 404


def test_get_student_invalid_id_returns_400(client):
    response = client.get("/students/abc")
    assert response.status_code == 400


# ---------- POST : création (4 tests) ----------

def test_post_valid_student_returns_201_with_id(client):
    response = client.post("/students", json=VALID_STUDENT)
    body = response.json()
    assert response.status_code == 201
    assert "id" in body
    assert body["email"] == VALID_STUDENT["email"]


def test_post_missing_field_returns_400(client):
    payload = make_student()
    del payload["email"]
    response = client.post("/students", json=payload)
    assert response.status_code == 400


def test_post_invalid_grade_returns_400(client):
    response = client.post("/students", json=make_student(grade=25))
    assert response.status_code == 400


def test_post_duplicate_email_returns_409(client):
    client.post("/students", json=VALID_STUDENT)
    response = client.post("/students", json=VALID_STUDENT)
    assert response.status_code == 409


# ---------- PUT : modification (2 tests) ----------

def test_put_valid_data_returns_200_and_updated_student(client):
    response = client.put("/students/1", json=make_student(firstName="Nouveau"))
    assert response.status_code == 200
    assert response.json()["firstName"] == "Nouveau"


def test_put_unknown_id_returns_404(client):
    response = client.put("/students/999", json=VALID_STUDENT)
    assert response.status_code == 404


# ---------- DELETE : suppression (2 tests) ----------

def test_delete_valid_id_returns_200(client):
    response = client.delete("/students/1")
    assert response.status_code == 200


def test_delete_unknown_id_returns_404(client):
    response = client.delete("/students/999")
    assert response.status_code == 404


# ---------- Stats & search (2 tests) ----------

def test_stats_returns_expected_keys_and_values(client):
    students = client.get("/students").json()
    response = client.get("/students/stats")
    data = response.json()

    assert response.status_code == 200
    for key in ("totalStudents", "averageGrade", "studentsByField", "bestStudent"):
        assert key in data

    expected_avg = round(sum(s["grade"] for s in students) / len(students), 2)
    assert data["totalStudents"] == len(students)
    assert data["averageGrade"] == expected_avg
    assert data["bestStudent"]["grade"] == max(s["grade"] for s in students)
    assert sum(data["studentsByField"].values()) == len(students)


def test_search_returns_matching_students(client):
    response = client.get("/students/search", params={"q": "ahmed"})
    results = response.json()
    assert response.status_code == 200
    assert len(results) >= 1
    for student in results:
        full_name = f"{student['firstName']} {student['lastName']}".lower()
        assert "ahmed" in full_name


# ---------- Tests supplémentaires (cas limites / bonus 20+) ----------

def test_search_is_case_insensitive(client):
    lower = client.get("/students/search", params={"q": "ahmed"}).json()
    upper = client.get("/students/search", params={"q": "AHMED"}).json()
    assert lower == upper


def test_search_without_q_returns_400(client):
    assert client.get("/students/search").status_code == 400
    assert client.get("/students/search", params={"q": ""}).status_code == 400


def test_post_invalid_field_returns_400(client):
    response = client.post("/students", json=make_student(field="histoire"))
    assert response.status_code == 400


def test_post_short_name_returns_400(client):
    response = client.post("/students", json=make_student(firstName="A"))
    assert response.status_code == 400


def test_post_invalid_email_format_returns_400(client):
    response = client.post("/students", json=make_student(email="pas-un-email"))
    assert response.status_code == 400


def test_put_email_taken_by_other_student_returns_409(client):
    other = client.get("/students/2").json()
    response = client.put("/students/1", json=make_student(email=other["email"]))
    assert response.status_code == 409


def test_deleted_student_is_no_longer_found(client):
    client.delete("/students/1")
    assert client.get("/students/1").status_code == 404
