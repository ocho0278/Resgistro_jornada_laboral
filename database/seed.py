import sqlite3

from database.data import conectar_db, crear_tablas


def crear_trabajadores_demo():

    crear_tablas()

    trabajadores = [
        ("0180004", "Gabriel D."),
        ("0180005", "Lina E."),
        ("0180006", "Roberto F.")
    ]

    conexion = conectar_db()

    try:
        for codigo, nombre in trabajadores:

            conexion.execute(
                """
                INSERT OR IGNORE INTO trabajadores (codigo, nombre)
                VALUES (?, ?)
                """,
                (codigo, nombre)
            )

        conexion.commit()

        print("Trabajadores de demostración disponibles.")

    except sqlite3.Error as error:
        conexion.rollback()
        print("Error al crear trabajadores:", error)

    finally:
        conexion.close()


if __name__ == "__main__":
    crear_trabajadores_demo()