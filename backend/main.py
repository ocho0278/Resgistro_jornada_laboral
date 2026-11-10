from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .jornadas import iniciar_jornada, finalizar_jornada

app = FastAPI(
    title="Sistema de Registro de Jornada Laboral",
    description="API para gestionar las jornadas laborales de los trabajadores",
    version="1.0.0"
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