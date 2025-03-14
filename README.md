# Documentación de la API

## Endpoints de Empleados

### Obtener todos los empleados
**URL:** `/obtenerEmpleados`  
**Método:** `GET`  
**Descripción:** Devuelve una lista con todos los empleados.  
**Respuesta:**
```json
[
    {
        "idEmpleado": 1,
        "nombreEmpleado": "Juan",
        "apellidoEmpleado": "Pérez",
        "rol": "Desarrollador"
    }
]
```

---
### Obtener un empleado por ID
**URL:** `/obtenerEmpleado/<int:id>`  
**Método:** `GET`  
**Descripción:** Devuelve la información de un empleado específico por su ID.  
**Respuesta:**
```json
{
    "idEmpleado": 1,
    "nombreEmpleado": "Juan",
    "apellidoEmpleado": "Pérez",
    "rol": "Desarrollador"
}
```

---
### Insertar un nuevo empleado
**URL:** `/insertarEmpleado`  
**Método:** `POST`  
**Descripción:** Crea un nuevo empleado.  
**Cuerpo de la petición:**
```json
{
    "nombre": "Juan",
    "apellido": "Pérez",
    "rol": "Desarrollador"
}
```
**Respuesta:**
```json
{
    "mensaje": "Empleado creado",
    "idEmpleado": 1,
    "nombreEmpleado": "Juan",
    "apellidoEmpleado": "Pérez",
    "rol": "Desarrollador"
}
```

---
### Eliminar un empleado
**URL:** `/eliminarEmpleado/<int:id>`  
**Método:** `DELETE`  
**Descripción:** Elimina un empleado por su ID.  
**Respuesta:**
```json
{
    "mensaje": "Empleado eliminado",
    "idEmpleado": 1
}
```

---
### Actualizar un empleado
**URL:** `/actualizarEmpleado/<int:id>`  
**Método:** `PUT`  
**Descripción:** Actualiza la información de un empleado existente.  
**Cuerpo de la petición:**
```json
{
    "nombre": "Juan",
    "apellido": "Gómez",
    "rol": "Gerente"
}
```
**Respuesta:**
```json
{
    "mensaje": "Empleado actualizado",
    "idEmpleado": 1,
    "nombreEmpleado": "Juan",
    "apellidoEmpleado": "Gómez",
    "rol": "Gerente"
}
```

---
### Asociar una tarea a un empleado
**URL:** `/asociarTareaAEmpleado/<int:idEmpleado>`  
**Método:** `POST`  
**Descripción:** Asocia una tarea a un empleado.  
**Cuerpo de la petición:**
```json
{
    "idTarea": 5,
    "rol": "Líder"
}
```
**Respuesta:**
```json
{
    "mensaje": "Tarea asociada correctamente",
    "idEmpleado": 1,
    "idTarea": 5
}
```


## Endpoints de Equipos  

### Obtener todos los equipos  
**URL:** `/obtenerEquipos`  
**Método:** `GET`  
**Descripción:** Devuelve una lista de todos los equipos.  

---

### Obtener un equipo por ID  
**URL:** `/obtenerEquipo/<int:id>`  
**Método:** `GET`  
**Descripción:** Devuelve la información de un equipo por su ID.  

---

### Insertar un nuevo equipo  
**URL:** `/insertarEquipo`  
**Método:** `POST`  
**Descripción:** Crea un nuevo equipo.  

---

### Eliminar un equipo  
**URL:** `/eliminarEquipo/<int:id>`  
**Método:** `DELETE`  
**Descripción:** Elimina un equipo por su ID.  

---

### Asociar un empleado a un equipo  
**URL:** `/asociarEmpleadoAEquipo/<int:idEquipo>`  
**Método:** `POST`  
**Descripción:** Asocia un empleado a un equipo.  

---

## Endpoints de Tareas  

### Obtener todas las tareas  
**URL:** `/obtenerTareas`  
**Método:** `GET`  
**Descripción:** Devuelve una lista de todas las tareas.  

---

### Obtener una tarea por ID  
**URL:** `/obtenerTarea/<int:id>`  
**Método:** `GET`  
**Descripción:** Devuelve la información de una tarea específica por su ID.  

---

### Insertar una nueva tarea  
**URL:** `/insertarTarea`  
**Método:** `POST`  
**Descripción:** Crea una nueva tarea.  

---

### Eliminar una tarea  
**URL:** `/eliminarTarea/<int:id>`  
**Método:** `DELETE`  
**Descripción:** Elimina una tarea por su ID.  

---

### Actualizar una tarea  
**URL:** `/actualizarTarea/<int:id>`  
**Método:** `PUT`  
**Descripción:** Actualiza la información de una tarea existente.  

---

Esta documentación cubre los endpoints principales de la API para gestionar empleados, equipos y tareas.
