// =============================================
// CONFIGURACIÓN
// =============================================

// Usaremos el mismo servidor para frontend y backend.
const API_URL = "/api/jornadas";

// Elementos de la interfaz
const codigoInput = document.getElementById("codigo");
const nombreTrabajador = document.getElementById("nombreTrabajador");
const estadoJornada = document.getElementById("estadoJornada");
const tiempoElemento = document.getElementById("tiempo");
const btnIniciar = document.getElementById("btnIniciar");
const btnFinalizar = document.getElementById("btnFinalizar");
const mensajeElemento = document.getElementById("mensaje");

// Variables para el cronómetro
let intervalo = null;
let horaEntrada = null;
let peticionEnCurso = false;
let versionConsulta = 0;


// =============================================
// FUNCIONES AUXILIARES
// =============================================

// Mostrar mensajes de éxito o error
function mostrarMensaje(texto, tipo = "") {
    mensajeElemento.textContent = texto;
    mensajeElemento.className = tipo;
}


// Convertir segundos a formato HH:MM:SS
function formatearTiempo(segundos) {
    const horas = Math.floor(segundos / 3600);
    const minutos = Math.floor((segundos % 3600) / 60);
    const segundosRestantes = segundos % 60;

    return `${String(horas).padStart(2, "0")}:${String(minutos).padStart(2, "0")}:${String(segundosRestantes).padStart(2, "0")}`;
}


// Configurar botones según el estado
function configurarBotones(jornadaActiva) {
    btnIniciar.disabled = peticionEnCurso || jornadaActiva;
    btnFinalizar.disabled = peticionEnCurso || !jornadaActiva;
}


// =============================================
// CRONÓMETRO
// =============================================

function actualizarCronometro() {
    if (!horaEntrada) return;

    // Calculamos la diferencia entre ahora y la entrada
    const ahora = Date.now();
    const inicio = new Date(horaEntrada).getTime();

    const segundos = Math.max(
        0,
        Math.floor((ahora - inicio) / 1000)
    );

    tiempoElemento.textContent = formatearTiempo(segundos);
}


function iniciarCronometro(fechaEntrada) {
    detenerCronometro();

    horaEntrada = fechaEntrada;

    // Mostrar inmediatamente el tiempo transcurrido
    actualizarCronometro();

    // Actualizar la pantalla cada segundo
    intervalo = setInterval(actualizarCronometro, 1000);
}


function detenerCronometro() {
    if (intervalo !== null) {
        clearInterval(intervalo);
        intervalo = null;
    }

    horaEntrada = null;
}


// =============================================
// PETICIONES A FASTAPI
// =============================================

// Función reutilizable para comunicarse con la API
async function solicitarAPI(ruta, metodo = "GET", datos = null) {
    const opciones = {
        method: metodo,
        headers: {
            "Content-Type": "application/json"
        }
    };

    if (datos !== null) {
        opciones.body = JSON.stringify(datos);
    }

    const respuesta = await fetch(`${API_URL}${ruta}`, opciones);
    const resultado = await respuesta.json();

    if (!respuesta.ok) {
        throw new Error(resultado.detail || "Error en la solicitud.");
    }

    return resultado;
}


// =============================================
// CONSULTAR ESTADO DEL TRABAJADOR
// =============================================

async function consultarEstado() {
    const codigo = codigoInput.value.trim();
    const consultaActual = ++versionConsulta;

    detenerCronometro();
    tiempoElemento.textContent = "00:00:00";
    nombreTrabajador.textContent = "";
    estadoJornada.textContent = "Sin jornada activa";
    configurarBotones(false);

    if (!codigo) {
        mostrarMensaje("Ingrese su código de trabajador.", "error");
        return;
    }

    try {
        const resultado = await solicitarAPI(
            `/estado/${encodeURIComponent(codigo)}`
        );

        // Ignorar respuestas de una consulta anterior
        if (consultaActual !== versionConsulta) return;

        nombreTrabajador.textContent = resultado.trabajador;

        if (resultado.jornada_activa) {
            estadoJornada.textContent = "Jornada en curso";
            iniciarCronometro(resultado.hora_entrada);
            configurarBotones(true);
        } else {
            estadoJornada.textContent = "Sin jornada activa";
            configurarBotones(false);
        }

        mostrarMensaje("");

    } catch (error) {
        if (consultaActual !== versionConsulta) return;
        mostrarMensaje(error.message, "error");
    }
}


// =============================================
// INICIAR JORNADA
// =============================================

async function iniciarJornada() {
    const codigo = codigoInput.value.trim();

    if (!codigo) {
        mostrarMensaje("Debe ingresar un código.", "error");
        return;
    }

    peticionEnCurso = true;
    configurarBotones(false);

    try {
        const resultado = await solicitarAPI(
            "/iniciar",
            "POST",
            { codigo }
        );

        nombreTrabajador.textContent = resultado.trabajador;
        estadoJornada.textContent = "Jornada en curso";

        iniciarCronometro(resultado.hora_entrada);

        mostrarMensaje(resultado.mensaje, "exito");

    } catch (error) {
        mostrarMensaje(error.message, "error");
        await consultarEstado();
    } finally {
        peticionEnCurso = false;
        configurarBotones(horaEntrada !== null);
    }
}


// =============================================
// FINALIZAR JORNADA
// =============================================

async function finalizarJornada() {
    const codigo = codigoInput.value.trim();

    if (!codigo) {
        mostrarMensaje("Debe ingresar un código.", "error");
        return;
    }

    peticionEnCurso = true;
    configurarBotones(true);

    try {
        const resultado = await solicitarAPI(
            "/finalizar",
            "POST",
            { codigo }
        );

        detenerCronometro();

        tiempoElemento.textContent = formatearTiempo(
            resultado.duracion_segundos
        );

        estadoJornada.textContent = "Jornada finalizada";

        mostrarMensaje(
            `Jornada finalizada. Tiempo total: ${tiempoElemento.textContent}`,
            "exito"
        );

    } catch (error) {
        mostrarMensaje(error.message, "error");
        await consultarEstado();
    } finally {
        peticionEnCurso = false;
        configurarBotones(horaEntrada !== null);
    }
}


// =============================================
// EVENTOS DE LA INTERFAZ
// =============================================

// Iniciar jornada
btnIniciar.addEventListener("click", iniciarJornada);

// Finalizar jornada
btnFinalizar.addEventListener("click", finalizarJornada);

// Consultar estado al cambiar el código
codigoInput.addEventListener("change", consultarEstado);

// Si cambia el código, invalidar el estado anterior
codigoInput.addEventListener("input", () => {
    versionConsulta++;

    detenerCronometro();

    tiempoElemento.textContent = "00:00:00";
    nombreTrabajador.textContent = "";
    estadoJornada.textContent = "Sin jornada activa";

    configurarBotones(false);
    mostrarMensaje("");
});