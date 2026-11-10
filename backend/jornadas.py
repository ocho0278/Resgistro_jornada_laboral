import sqlite3
from datetime import datetime, timezone

from database.data import conectar_db


def iniciar_jornada(codigo):
    conexion = conectar_db()

    try:
        trabajador = conexion.execute(
            "SELECT id, nombre FROM trabajadores WHERE codigo = ?",
            (codigo,)
        ).fetchone()

        if trabajador is None:
            return {"error": "El trabajador no existe."}

        activa = conexion.execute(
            """
            SELECT id FROM jornadas
            WHERE trabajador_id = ? AND hora_salida IS NULL
            """,
            (trabajador["id"],)
        ).fetchone()

        if activa:
            return {"error": "El trabajador ya tiene una jornada activa."}

        entrada = datetime.now(timezone.utc).isoformat()

        cursor = conexion.execute(
            """
            INSERT INTO jornadas (trabajador_id, hora_entrada)
            VALUES (?, ?)
            """,
            (trabajador["id"], entrada)
        )

        conexion.commit()

        return {
            "mensaje": "Jornada iniciada correctamente.",
            "jornada_id": cursor.lastrowid,
            "trabajador": trabajador["nombre"],
            "hora_entrada": entrada
        }

    except sqlite3.IntegrityError:
        conexion.rollback()
        return {"error": "El trabajador ya tiene una jornada activa."}

    finally:
        conexion.close()


def finalizar_jornada(codigo):
    conexion = conectar_db()

    try:
        trabajador = conexion.execute(
            "SELECT id, nombre FROM trabajadores WHERE codigo = ?",
            (codigo,)
        ).fetchone()

        if trabajador is None:
            return {"error": "El trabajador no existe."}

        jornada = conexion.execute(
            """
            SELECT id, hora_entrada
            FROM jornadas
            WHERE trabajador_id = ? AND hora_salida IS NULL
            """,
            (trabajador["id"],)
        ).fetchone()

        if jornada is None:
            return {"error": "El trabajador no tiene una jornada activa."}

        salida = datetime.now(timezone.utc)
        entrada = datetime.fromisoformat(jornada["hora_entrada"])

        duracion = max(0, int((salida - entrada).total_seconds()))

        conexion.execute(
            """
            UPDATE jornadas
            SET hora_salida = ?, duracion_segundos = ?
            WHERE id = ? AND hora_salida IS NULL
            """,
            (salida.isoformat(), duracion, jornada["id"])
        )

        conexion.commit()

        return {
            "mensaje": "Jornada finalizada correctamente.",
            "trabajador": trabajador["nombre"],
            "hora_entrada": jornada["hora_entrada"],
            "hora_salida": salida.isoformat(),
            "duracion_segundos": duracion
        }

    finally:
        conexion.close()

if __name__ == "__main__":

    codigo = input("Ingrese el código del trabajador: ").strip()

    print("\n1. Iniciar jornada")
    print("2. Finalizar jornada")

    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        print(iniciar_jornada(codigo))

    elif opcion == "2":
        print(finalizar_jornada(codigo))

    else:
        print("Opción inválida.")