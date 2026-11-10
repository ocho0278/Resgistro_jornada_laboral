# Resgistro_jornada_laboral
Sistema para registrar el inicio y la finalización de la jornada laboral de un trabajador.

Funcionalidades: 
El sistema permite
- Identificar trabajadores mediante un código único.
- Registrar el inicio de una jornada laboral.
- Visualizar el tiempo transcurrido mediante un cronómetro.
- Registrar la finalización de la jornada.
- Calcular y almacenar la duración total en segundos.
- Recuperar jornadas activas después de recargar la página.
- Impedir el registro de jornadas simultáneas para un mismo trabajador.
- Mostrar mensajes de confirmación y error.
El tiempo trabajado se calcula utilizando la diferencia entre la hora actual y la hora de entrada registrada.
La base de datos no se actualiza cada segundo; únicamente se registran los eventos necesarios.

Arquitectura:
La aplicación utiliza una arquitectura organizada en tres componentes:
1. Frontend: Desarrollado en HTML, CSS y JavaScript. Permite la interacción del trabajador con el sistema y realiza solicitudes HTTP al backend.
2. Backend: Desarrollado en Python con FastAPI. Gestiona las solicitudes, valida las operaciones y calcula la duración de las jornadas.
3. Base de datos:Implementada mediante SQLite. Almacena la información de los trabajadores y sus registros de jornada laboral. 

La base de datos contiene dos tablas relacionadas.

Tabla: trabajadores

id---Identificador interno autoincremental
codigo---Codigo único del trabajador
nombre---Nombre del trabajador

Tabla: jornadas

id---Identificador de la jornada
trabajador_id---Referencia al trabajado
hora_entrada---Fecha y hora de inicio
hora_salida---Fecha y hora de finalización
duracion_segundos---Duración total de la jornada

Manejo de errores

Se implementaron tres escenarios principales.

Error 1. Trabajador inexistente
Situación: el usuario introduce un código que no existe en la base de datos.
Gestión: el backend verifica la existencia del trabajador antes de permitir la operación.
Respuesta: HTTP 404, con un mensaje indicando que el trabajador no existe.

Erro 2. Jornada activa duplicada
Situación: un trabajador intenta iniciar una nueva jornada sin finalizar la anterior.
Gestión: el backend consulta si existe una jornada activa y rechaza la operación.
Adicionalmente, SQLite incorpora un índice único parcial que impide almacenar dos jornadas abiertas para el mismo trabajador.
Respuesta: HTTP 409, indicando que el trabajador ya tiene una jornada activa.

Error 3. Finalización sin jornada activa
Situación: un trabajador intenta finalizar una jornada que no ha iniciado.
Gestión: el backend comprueba que exista una jornada abierta.
Respuesta: HTTP 409, indicando que no existe una jornada activa.
Estas validaciones permiten mantener la consistencia de los registros y evitar operaciones incorrectas.

Instalación y ejecución:
1. Requisitos
2. Python 3.10 o superior.
3. Git.
Navegador web.

Ejecucion:
    1. Clonar el repositorio
    git clone https://github.com/ocho0278/Resgistro_jornada_laboral.git
    cd Resgistro_jornada_laboral

    2. Instalar dependencias
    python -m pip install -r requirements.txt

    3. Crear trabajadores de demostración
    python -m database.seed
    Este comando crea las tablas necesarias y registra trabajadores de prueba.

    4. Iniciar el servidor
    python -m uvicorn backend.main:app --reload

    5. Abrir la aplicación

En el navegador, ingresar a:
http://127.0.0.1:8000/

La documentación interactiva de la API está disponible en:
http://127.0.0.1:8000/docs

7. Trabajadores de demostración
id - codigo Trabajador - nombretrabajador
1 0180001 Sergio A.
2 0180002 Johana B.
3 0180003 Andres C.
4 0180004 Gabriel D.
5 0180005 Lina E.
6 0180006 Roberto F.

Estos códigos se generan al ejecutar database.seed.

8. Uso del sistema

Iniciar jornada:
Introducir el código del trabajador.
Seleccionar «Iniciar jornada».
El sistema registra la fecha y hora de entrada.
El cronómetro comienza a mostrar el tiempo transcurrido.

Terminar jornada:
Seleccionar «Terminar jornada».
El sistema registra la fecha y hora de salida.
Se calcula y almacena la duración total.
Se muestra un mensaje de confirmación.

Recuperar jornada activa:
Si el trabajador recarga la página, puede ingresar nuevamente su código para recuperar la jornada en curso.
El cronómetro se reconstruye a partir de la hora de entrada almacenada.



Autor: Sebastian Ochoa C.
contacto: ochoac0278@gmail.com