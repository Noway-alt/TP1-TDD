"""Fixtures partagées par les tests."""
import pytest
from fastapi.testclient import TestClient

from src.app import app
from src.data import reset_students


@pytest.fixture(autouse=True)
def reset_data():
    """Remet les données à l'état initial avant chaque test."""
    reset_students()
    yield


@pytest.fixture
def client():
    """Client HTTP de test (aucun serveur lancé)."""
    return TestClient(app)
