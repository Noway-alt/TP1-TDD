"""Point d'entrée : uvicorn src.main:app --reload"""
from src.app import app

__all__ = ["app"]
