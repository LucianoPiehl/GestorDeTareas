// CODIGO EQUIPOS

document.querySelector('#formInsertarEquipo').addEventListener('submit', async (e) => {
    e.preventDefault();

    const nombreEquipo = document.querySelector('#nombreEquipo').value;

    const response = await fetch('/equipos/insertarEquipo', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ nombreEquipo }),
    });

    const data = await response.json();
    alert(data.mensaje);
    obtenerEquipos();
});

async function obtenerEquipos() {
    const response = await fetch('/equipos/obtenerEquipos');
    const equipos = await response.json();

    const equiposTable = document.querySelector('#equiposTable tbody');
    equiposTable.innerHTML = ''; // Limpiar la tabla

    for (const equipo of equipos) {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${equipo.idEquipo}</td>
            <td contenteditable="false" id="nombreEquipo-${equipo.idEquipo}">${equipo.nombreEquipo}</td>
            <td>
                <button onclick="activarEdicion(${equipo.idEquipo})">Actualizar</button>
                <button onclick="eliminarEquipo(${equipo.idEquipo})">Eliminar</button>
            </td>
        `;
        equiposTable.appendChild(tr);
    }
}

window.onload = obtenerEquipos;

async function eliminarEquipo(id) {
    const response = await fetch(`/equipos/eliminarEquipo/${id}`, {
        method: 'DELETE',
    });

    const data = await response.json();
    alert(data.mensaje); // Mostrar mensaje de éxito
    obtenerEquipos(); // Actualizar la lista de equipos
}

async function activarEdicion(idEquipo) {
    document.querySelector(`#nombreEquipo-${idEquipo}`).contentEditable = "true";

    const botones = document.querySelectorAll('button');
    botones.forEach(boton => {
        if (boton.textContent === "Actualizar") {
            boton.textContent = "Guardar cambios";
            boton.onclick = () => guardarCambios(idEquipo);
        }
    });
}

async function guardarCambios(idEquipo) {
    const nombreEquipo = document.querySelector(`#nombreEquipo-${idEquipo}`).textContent;

    const response = await fetch(`/equipos/actualizarEquipo/${idEquipo}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ nombreEquipo }),
    });

    const data = await response.json();
    alert(data.mensaje);
    obtenerEquipos();
}


// Codigo Tareas


    // Función para obtener las tareas desde el servidor
    async function obtenerTareas() {
        const response = await fetch('/tareas/obtenerTareas');
        const tareas = await response.json();

        const tareasTable = document.querySelector('#tareasTable tbody');
        tareasTable.innerHTML = ''; // Limpiar la tabla

        tareas.forEach(tarea => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${tarea.idTarea}</td>
                <td id="nombreTarea-${tarea.idTarea}" contenteditable="false">${tarea.nombreTarea}</td>
                <td id="fechaInicio-${tarea.idTarea}" contenteditable="false">${tarea.fechaInicio}</td>
                <td id="fechaFin-${tarea.idTarea}" contenteditable="false">${tarea.fechaFin}</td>
                <td id="estado-${tarea.idTarea}" contenteditable="false">${tarea.estado}</td>
                <td>
                    <button onclick="activarEdicionTarea(${tarea.idTarea})">Actualizar</button>
                    <button onclick="eliminarTarea(${tarea.idTarea})">Eliminar</button>
                </td>
            `;
            tareasTable.appendChild(tr);
        });
    }

    window.onload = obtenerTareas;

        // Función para eliminar tarea
    async function eliminarTarea(idTarea) {
        const response = await fetch(`/tareas/eliminarTarea/${idTarea}`, {
            method: 'DELETE',
        });

        const data = await response.json();
        alert(data.mensaje); // Mostrar mensaje de éxito
        obtenerTareas(); // Actualizar la lista de tareas
    }

    document.querySelector('#formInsertarTarea').addEventListener('submit', async (e) => {
    e.preventDefault();

    const nombreTarea = document.querySelector('#nombreTarea').value;
    const fechaInicio = document.querySelector('#fechaInicio').value;
    const fechaFin = document.querySelector('#fechaFin').value;
    const estado = document.querySelector('#estado').value;

    const response = await fetch('/tareas/insertarTarea', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ nombreTarea, fechaInicio, fechaFin, estado }),
    });

    const data = await response.json();
    alert(data.mensaje); // Mostrar mensaje de éxito
    obtenerTareas(); // Actualizar la lista de tareas
});



// Activar edición de una tarea
function activarEdicionTarea(idTarea) {
    // Habilitar la edición de los campos correspondientes
    const nombreTarea = document.getElementById(`nombreTarea-${idTarea}`);
    const fechaInicio = document.getElementById(`fechaInicio-${idTarea}`);
    const fechaFin = document.getElementById(`fechaFin-${idTarea}`);
    const estado = document.getElementById(`estado-${idTarea}`);

    // Hacer editable el campo de texto o fecha
    nombreTarea.contentEditable = "true";
    estado.contentEditable = "true";
    
// Modificar para mostrar la fecha anterior y luego el selector de fecha

    if (fechaInicio) {
        fechaInicio.innerHTML = `<p>Fecha Anterior: </p>${fechaInicio.innerHTML}<br><input type="date" id="fechaInicioInput-${idTarea}" value="${fechaInicio.innerHTML}" />`;
        fechaInicio.contentEditable = "false";
    }
    if (fechaFin) {
        fechaFin.innerHTML = `<p>Fecha Anterior: </p> ${fechaFin.innerHTML}<br><input type="date" id="fechaFinInput-${idTarea}" value="${fechaFin.innerHTML}" />`;
        fechaFin.contentEditable = "false";
    }

    // Cambiar el texto del botón a "Guardar"
    const button = document.querySelector(`#tareasTable button[onclick="activarEdicionTarea(${idTarea})"]`);
    button.textContent = "Guardar";
    button.setAttribute("onclick", `guardarCambiosTarea(${idTarea})`);
}

// Función para guardar los cambios realizados en la tarea
async function guardarCambiosTarea(idTarea) {
    // Obtener los nuevos valores de los campos editados
    const nombreTarea = document.getElementById(`nombreTarea-${idTarea}`).textContent;
    const estado = document.getElementById(`estado-${idTarea}`).textContent;
    const fechaInicio = document.getElementById(`fechaInicioInput-${idTarea}`).value;
    const fechaFin = document.getElementById(`fechaFinInput-${idTarea}`).value;

    // Enviar los datos actualizados al servidor
    const response = await fetch(`/tareas/actualizarTarea/${idTarea}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ nombreTarea, fechaInicio, fechaFin, estado }),
    });

    const data = await response.json();
    alert(data.mensaje); // Mostrar mensaje de éxito
    obtenerTareas(); // Actualizar la lista de tareas

    // Desactivar la edición de los campos
    document.getElementById(`nombreTarea-${idTarea}`).contentEditable = "false";
    document.getElementById(`estado-${idTarea}`).contentEditable = "false";
    document.getElementById(`fechaInicio-${idTarea}`).innerHTML = fechaInicio;
    document.getElementById(`fechaFin-${idTarea}`).innerHTML = fechaFin;

    // Cambiar el texto del botón a "Actualizar"
    const button = document.querySelector(`#tareasTable button[onclick="guardarCambiosTarea(${idTarea})"]`);
    button.textContent = "Actualizar";
    button.setAttribute("onclick", `activarEdicionTarea(${idTarea})`);
}

//Codigo Empleados

async function activarEdicion(idEmpleado) {
    // Hacer que las celdas sean editables
    document.querySelector(`#nombre-${idEmpleado}`).contentEditable = "true";
    document.querySelector(`#apellido-${idEmpleado}`).contentEditable = "true";
    document.querySelector(`#rol-${idEmpleado}`).contentEditable = "true";

    // Cambiar el texto del botón a "Guardar cambios"
    const botones = document.querySelectorAll('button');
    botones.forEach(boton => {
        if (boton.textContent === "Actualizar") {
            boton.textContent = "Guardar cambios";
            boton.onclick = () => guardarCambios(idEmpleado);
        }
    });
}
async function guardarCambios(idEmpleado) {
    // Obtener los nuevos valores
    const nombre = document.querySelector(`#nombre-${idEmpleado}`).textContent;
    const apellido = document.querySelector(`#apellido-${idEmpleado}`).textContent;
    const rol = document.querySelector(`#rol-${idEmpleado}`).textContent;

    const response = await fetch(`/empleados/actualizarEmpleado/${idEmpleado}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ nombre, apellido, rol }),
    });

    const data = await response.json();
    alert(data.mensaje); // Mostrar mensaje de éxito
    obtenerEmpleados(); // Actualizar la lista de empleados

    // Desactivar la edición y restablecer el botón a "Actualizar"
    document.querySelector(`#nombre-${idEmpleado}`).contentEditable = "false";
    document.querySelector(`#apellido-${idEmpleado}`).contentEditable = "false";
    document.querySelector(`#rol-${idEmpleado}`).contentEditable = "false";

    const botones = document.querySelectorAll('button');
    botones.forEach(boton => {
        if (boton.textContent === "Guardar cambios") {
            boton.textContent = "Actualizar";
            boton.onclick = () => activarEdicion(idEmpleado);
        }
    });
}

window.onload = obtenerEmpleados;
async function obtenerTareasEmpleado(idEmpleado) {
const response = await fetch(`/empleados/${idEmpleado}/tareas`);
const tareas = await response.json();
const tareasTd = document.querySelector(`#tareas-${idEmpleado}`);

tareasTd.innerHTML = ''; // Limpiar las tareas previas

if (tareas.length === 0) {
    tareasTd.innerHTML = 'No tiene tareas asociadas';
} else {
    tareas.forEach((tarea, index) => {
        const [idTarea, nombreTarea, rol] = tarea;

        if (nombreTarea) {
            const tareaDiv = document.createElement('div');
            tareaDiv.classList.add('tarea');

            // Mostrar la tarea y el rol actual
            const nombreTareaSpan = document.createElement('span');
            nombreTareaSpan.textContent = nombreTarea;
            tareaDiv.appendChild(nombreTareaSpan);

            const rolSpan = document.createElement('span');
            rolSpan.textContent = rol == 1 ? 'Jefe' : 'Empleado';
            rolSpan.style.fontWeight = 'bold';
            rolSpan.style.marginLeft = '10px';
            tareaDiv.appendChild(rolSpan);
            const br = document.createElement('br');
            tareaDiv.append(br)
            // Botón para cambiar rol
            const btnCambiarRol = document.createElement('button');
            btnCambiarRol.textContent = 'Cambiar Rol';
            btnCambiarRol.onclick = () => cambiarRolTareaEmpleado(idEmpleado, idTarea);
            btnCambiarRol.style.marginLeft = '10px';
            tareaDiv.appendChild(btnCambiarRol);

            // Botón para desasignar tarea
            const btnEliminar = document.createElement('button');
            btnEliminar.textContent = 'Desasignar Tarea';
            btnEliminar.onclick = () => eliminarTareaEmpleado(idEmpleado, idTarea);
            btnEliminar.style.marginLeft = '10px';
            tareaDiv.appendChild(btnEliminar);

            // Separador si no es la última tarea
            if (index < tareas.length - 1) {
                const hr = document.createElement('hr');
                tareaDiv.appendChild(hr);
            }

            tareasTd.appendChild(tareaDiv);
        } else {
            console.error('nombreTarea no encontrado:', tarea);
        }
    });
}
}
const cambiarRolTareaEmpleado = async (empleadoId, tareaId) => {
try {
    const response = await fetch(`/empleados/cambiarRol/${empleadoId}/${tareaId}/`, {
        method: 'PUT'
    });

    if (!response.ok) {
        throw new Error('Error al cambiar el rol del empleado en la tarea');
    }

    // Opcional: actualizar la UI si es necesario
    console.log('Cambio de rol exitoso');
} catch (error) {
    console.error(error);
}
obtenerEmpleados(); 

};
let idEmpleadoSeleccionado = null;

async function asociarTareaAEmpleado(idEmpleado) {
// Guardar el ID del empleado seleccionado para asociar la tarea más tarde
idEmpleadoSeleccionado = idEmpleado;

// Mostrar el formulario para asociar tarea
document.querySelector('#asociarTareaEmpleado').style.display = 'block';

// Obtener las tareas disponibles
await obtenerTareas();
}

// Añadir evento de submit al formulario solo una vez
document.querySelector('#formAsociarTarea').addEventListener('submit', async (e) => {
    e.preventDefault();

    // Usar el idEmpleado guardado
    if (!idEmpleadoSeleccionado) {
        alert("No se ha seleccionado un empleado.");
        return;
    }

    const idTarea = document.querySelector('#seleccionarTarea').value;
    const rol = document.querySelector('#rolTarea').value;

    // Realizar la solicitud POST para asociar la tarea al empleado
    const response = await fetch(`/empleados/asociarTareaAEmpleado/${idEmpleadoSeleccionado}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ idTarea, rol }),
    });

    const data = await response.json();
    alert(data.mensaje); // Mostrar mensaje de éxito
    document.querySelector('#asociarTareaEmpleado').style.display = 'none'; // Ocultar el formulario
    obtenerEmpleados(); // Actualizar la lista de empleados
});


async function eliminarTareaEmpleado(idEmpleado, idTarea) {
    const response = await fetch(`/empleados/${idEmpleado}/eliminarTareaDeEmpleado/${idTarea}`, {
        method: 'DELETE',
    });

    const data = await response.json();
    alert(data.mensaje); // Mostrar mensaje de éxito
    obtenerEmpleados(); // Actualizar la lista de empleados y tareas
}

// Llamada a la función para cargar empleados al cargar la página
window.onload = obtenerEmpleados;
document.querySelector('#formInsertarEmpleado').addEventListener('submit', async (e) => {
    e.preventDefault();

    const nombre = document.querySelector('#nombre').value;
    const apellido = document.querySelector('#apellido').value;
    const rol = document.querySelector('#rol').value;

    const response = await fetch('/empleados/insertarEmpleado', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ nombre, apellido, rol }),
    });

    const data = await response.json();
    alert(data.mensaje); // Mostrar mensaje de éxito
    // Comprobar si el campo 'id' existe, indicando que el empleado se insertó correctamente
    if (data.id) {
        obtenerEmpleados(); // Actualizar la lista de empleados
    } else {
        console.log(data,data.id)
        console.error('Error al crear empleado');
    }
   
});

async function obtenerEmpleados() {
    const response = await fetch('/empleados/obtenerEmpleados');
    const empleados = await response.json();

    const empleadosTable = document.querySelector('#empleadosTable tbody');
    empleadosTable.innerHTML = ''; // Limpiar la tabla

    for (const empleado of empleados) {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${empleado.idEmpleado}</td>
            <td contenteditable="false" id="nombre-${empleado.idEmpleado}">${empleado.nombre}</td>
            <td contenteditable="false" id="apellido-${empleado.idEmpleado}">${empleado.apellido}</td>
            <td contenteditable="false" id="rol-${empleado.idEmpleado}">${empleado.rol}</td>
            <td id="tareas-${empleado.idEmpleado}"></td>
            <td>
                <button onclick="activarEdicion(${empleado.idEmpleado})">Actualizar</button>
                <button onclick="eliminarEmpleado(${empleado.idEmpleado})">Eliminar</button>
                <button onclick="asociarTareaAEmpleado(${empleado.idEmpleado})">Asociar Tarea</button>
            </td>
        `;
        empleadosTable.appendChild(tr);

        // Obtener tareas asociadas
        await obtenerTareasEmpleado(empleado.idEmpleado);
    }
}

window.onload = obtenerEmpleados;
async function obtenerTareas() {
const response = await fetch('/tareas/obtenerTareas');
const tareas = await response.json();
const seleccionarTarea = document.querySelector('#seleccionarTarea');

// Limpiar el select antes de agregar las nuevas opciones
seleccionarTarea.innerHTML = '<option value="">Seleccione una tarea</option>'; 

// Llenar el select con las tareas obtenidas
tareas.forEach(tarea => {
    const option = document.createElement('option');
    option.value = tarea.idTarea; // El valor del option será el id de la tarea
    option.textContent = tarea.nombreTarea; // El texto será el nombre de la tarea
    seleccionarTarea.appendChild(option);
});
}
async function eliminarEmpleado(id) {
    const response = await fetch(`/empleados/eliminarEmpleado/${id}`, {
        method: 'DELETE',
    });

    const data = await response.json();
    alert(data.mensaje); // Mostrar mensaje de éxito
    obtenerEmpleados(); // Actualizar la lista de empleados
}