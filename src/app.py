"""Configuration de l'application FastAPI (sans démarrage du serveur)."""
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from src.routes import router

app = FastAPI(title="API Étudiants")
app.include_router(router)


@app.exception_handler(RequestValidationError)
async def validation_handler(_request, _exc):
    """FastAPI renvoie 422 par défaut, le TP exige 400."""
    return JSONResponse(status_code=400, content={"detail": "Données invalides"})
