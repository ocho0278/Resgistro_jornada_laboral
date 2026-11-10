import sqlite3
from pathlib import Path

db_path = Path(__file__).parent / "jornadas.db"

def conectar_db():
    conexion = sqlite3.connect(db_path)
    conexion.row_factory = sqlite3.Row
    conexion.execute("PRAGMA foreign_keys = ON")
    return conexion

def crear_tablas():
    conexion = conectar_db()

    conexion.execute("""
        CREATE TABLE IF NOT EXISTS trabajadores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT NOT NULL UNIQUE,
            nombre TEXT NOT NULL
        )
    """)

    conexion.execute("""
        CREATE TABLE IF NOT EXISTS jornadas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            trabajador_id INTEGER NOT NULL,
            hora_entrada TEXT NOT NULL,
            hora_salida TEXT,
            duracion_segundos INTEGER,

            FOREIGN KEY (trabajador_id)
                REFERENCES trabajadores(id)
        )
    """)

    conexion.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS idx_jornada_activa
        ON jornadas(trabajador_id)
        WHERE hora_salida IS NULL
    """)

    #guardar y cerrar
    conexion.commit()
    conexion.close()

if __name__ == "__main__":
    crear_tablas()
    print("Base de datos y tablas creadas correctamente.")