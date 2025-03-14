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
    "mensaje": "Tar
