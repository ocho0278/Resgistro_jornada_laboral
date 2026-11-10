from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from pathlib import Path
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from database.data import crear_tablas

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

from .jornadas import (
    iniciar_jornada,
    finalizar_jornada,
    consultar_jornada_activa
)
@asynccontextmanager
async def lifespan(app: FastAPI):
    crear_tablas()
    yield

app = FastAPI(
    title="Sistema de Registro de Jornada Laboral",
    description="API para gestionar las jornadas laborales de los trabajadores",
    version="1.0.0",
    lifespan=lifespan
)
app.mount(
    "/static",
    StaticFiles(directory=FRONTEND_DIR),
    name="static"
)

#datos recibidos
class TrabajadorCodigo(BaseModel):
    codigo: str

#iniciar jornada
@app.post("/api/jornadas/iniciar")
def iniciar(datos: TrabajadorCodigo):

    resultado = iniciar_jornada(datos.codigo)

    if "error" in resultado:
        if resultado["error"] == "El trabajador no existe.":
            raise HTTPException(
                status_code=404,
                detail=resultado["error"]
            )

        raise HTTPException(
            status_code=409,
            detail=resultado["error"]
        )

    return resultado

#finalizar jornada
@app.post("/api/jornadas/finalizar")
def finalizar(datos: TrabajadorCodigo):

    resultado = finalizar_jornada(datos.codigo)

    if "error" in resultado:
        if resultado["error"] == "El trabajador no existe.":
            raise HTTPException(
                status_code=404,
                detail=resultado["error"]
            )

        raise HTTPException(
            status_code=409,
            detail=resultado["error"]
        )

    return resultado

@app.get("/api/jornadas/estado/{codigo}")
def consultar_estado(codigo: str):

    resultado = consultar_jornada_activa(codigo)

    if "error" in resultado:
        raise HTTPException(
            status_code=404,
            detail=resultado["error"]
        )

    return resultado
@app.get("/")
def mostrar_inicio():
    return FileResponse(FRONTEND_DIR / "index.html")