# Construyendo una API RESTful con Flask y MySQL 🔥

Este proyecto es una API RESTful desarrollada con **Flask** y **MySQL**, diseñada para gestionar tareas (To-Do List). La API proporciona endpoints para realizar operaciones CRUD (Crear, Leer, Actualizar y Eliminar) sobre una tabla `todos`.

![Resultado final](https://raw.githubusercontent.com/urian121/imagenes-proyectos-github/refs/heads/master/Resultado-api-flask-mysql.png)

## Tabla de Contenidos
1. [Descripción](#descripción)
2. [Requisitos](#requisitos)
3. [Instalación](#instalación)
4. [Uso](#uso)
5. [Endpoints](#endpoints)
6. [Ejemplos de Solicitudes](#ejemplos-de-solicitudes)

## Descripción

Esta **API** permite gestionar una lista de tareas (**To-Do List**) utilizando una base de datos **MySQL**. Los usuarios pueden crear, leer, actualizar y eliminar tareas mediante solicitudes **HTTP**.

## Requisitos

Para ejecutar este proyecto, necesitas:

- Python 3.x
- Flask (`pip install flask`)
- Flask-CORS (`pip install flask-cors`)
- mysql-connector-python (`pip install mysql-connector-python`)
- Una base de datos MySQL configurada con la tabla `todos`.

### Estructura de la tabla `todos`

```sql
CREATE TABLE todos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Instalación

1. Clona este repositorio:
    
    ```bash
    git clone https://github.com/urian121/construyendo-una-APIs-REST-con-Flask-y-MySQL
    cd construyendo-una-APIs-REST-con-Flask-y-MySQL
    ```

2. Crea un entorno virtual (opcional pero recomendado):
    
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    venv\Scripts\activate  # Windows
    ```
    
3. Instala las dependencias:
    
    ```bash
    pip install -r requirements.txt
    ```
    
4. Configura la conexión a la base de datos:
    
    - Abre `db.py` y actualiza los valores de `host`, `user`, `passwd` y `database` con tus credenciales de MySQL.

5. Ejecuta la aplicación:
    
    ```bash
    python app.py
    ```
    
La API estará disponible en `http://localhost:5000`.


## Uso

La **API** proporciona endpoints para gestionar tareas. A continuación, se detallan los endpoints disponibles.


### Endpoints

| Método HTTP | Endpoint | Descripción |
|------------|---------|-------------|
| `GET`  | `/` | Mensaje de bienvenida |
| `POST` | `/todos` | Crear una nueva tarea |
| `GET`  | `/todos` | Obtener todas las tareas |
| `GET`  | `/todos/<int:todo_id>` | Obtener una tarea específica por su ID |
| `PUT`  | `/todos/<int:todo_id>` | Actualizar una tarea específica por su ID |
| `DELETE` | `/todos/<int:todo_id>` | Eliminar una tarea específica por su ID |


## Ejemplos de Solicitudes

### Crear una nueva tarea

**Solicitud:**
```bash
curl -X POST http://localhost:5000/todos
```

**Respuesta:**
```json
{
    "id": 1,
    "title": "Comprar leche",
    "completed": false,
    "created_at": "2023-10-01T12:00:00"
}
```

### Obtener todas las tareas
**Solicitud:**

```bash
curl http://localhost:5000/todos
```

**Respuesta:**
```json
[
    {
        "id": 1,
        "title": "Comprar leche",
        "completed": false,
        "created_at": "2023-10-01T12:00:00"
    },
    {
        "id": 2,
        "title": "Estudiar Flask",
        "completed": true,
        "created_at": "2023-10-01T12:05:00"
    }
]
```

### Obtener una tarea específica
**Solicitud:**
```bash
curl http://localhost:5000/todos/1
```

**Respuesta:**
```json
{
    "id": 1,
    "title": "Comprar leche",
    "completed": false,
    "created_at": "2023-10-01T12:00:00"
}
```

### Actualizar una tarea
**Solicitud:**
```bash
curl -X PUT http://localhost:5000/todos/1
```

**Respuesta:**
```json
{
    "id": 1,
    "title": "Comprar pan",
    "completed": true,
    "created_at": "2023-10-01T12:00:00"
}
```

### Eliminar una tarea
**Solicitud:**

```bash
curl -X DELETE http://localhost:5000/todos/1
```

**Respuesta:**
```bash
HTTP/1.1 204 No Content
```

### 🙌 Cómo puedes apoyar 📢:

✨ **Comparte este proyecto** con otros desarrolladores para que puedan beneficiarse 📢.

☕ **Invítame un café o una cerveza 🍺**:
   - [Paypal](https://www.paypal.me/iamdeveloper86) (`iamdeveloper86@gmail.com`).

### ⚡ ¡No olvides SUSCRIBIRTE a la [Comunidad WebDeveloper](https://www.youtube.com/WebDeveloperUrianViera?sub_confirmation=1)!


#### ⭐ **Déjanos una estrella en GitHub**:
   - Dicen que trae buena suerte 🍀.
**Gracias por tu apoyo 🤓.**
