from data import conectar_db

def registrar_trabajador(codigo, nombre):
    conexion = conectar_db()
    try:
        conexion.execute(
            """
            INSERT INTO trabajadores (codigo, nombre)
            VALUES (?, ?)
            """,
            (codigo, nombre)
        )
        conexion.commit()
        print("Trabajador registrado correctamente.")

    except Exception as error:
        print("Error al registrar trabajador:", error)

    finally:
        conexion.close()
def consultar_trabajadores():
    conexion = conectar_db()

    try:
        cursor = conexion.execute("""
            SELECT id, codigo, nombre
            FROM trabajadores
        """)

        trabajadores = cursor.fetchall()

        for trabajador in trabajadores:
            print(
                trabajador["id"],
                trabajador["codigo"],
                trabajador["nombre"]
            )

    finally:
        conexion.close()
def eliminar_trabajador(codigo):
    conexion = conectar_db()

    try:
        cursor = conexion.execute(
            "DELETE FROM trabajadores WHERE codigo = ?",
            (codigo,)
        )

        conexion.commit()

        if cursor.rowcount > 0:
            print("Trabajador eliminado correctamente.")
        else:
            print("No se encontró un trabajador con ese código.")

    except Exception as error:
        print("Error al eliminar trabajador:", error)

    finally:
        conexion.close()


if __name__ == "__main__":
    # registrar_trabajador("0180001", "Sergio A.")
    # registrar_trabajador("0180002", "Johana B.")
    # registrar_trabajador("0180003", "Andres C.")
    #eliminar_trabajador("")
    consultar_trabajadores()