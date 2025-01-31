from flask import Flask, request, jsonify  # Importamos Flask y sus módulos para manejar solicitudes y respuestas JSON
from flask_cors import CORS  # Habilita CORS para permitir solicitudes desde diferentes dominios
from db import get_db_connection  # Importamos la función para obtener la conexión a la base de datos
import mysql.connector  # Importamos el conector de MySQL

app = Flask(__name__)  # Inicializamos la aplicación Flask
CORS(app)  # Habilitamos CORS para permitir peticiones desde clientes externos

@app.route('/')  # Definimos la ruta raíz de la API
def home():
    """Ruta de bienvenida a la API."""
    return jsonify({"message": "Bienvenido a la API de Tareas con MySQL"})  # Retornamos un mensaje de bienvenida en formato JSON


# Crear una nueva tarea (CREATE)
@app.route('/todos', methods=['POST'])
def create_todo():
    """Crea una nueva tarea en la base de datos."""
    data = request.get_json()  # Obtenemos los datos enviados en formato JSON
    
    # Validamos que el campo 'title' esté presente en la solicitud
    if 'title' not in data:
        return jsonify({"error": "El título es requerido"}), 400
    
    connection = get_db_connection()  # Establecemos la conexión con la base de datos
    if not connection:
        return jsonify({"error": "Error de conexión a la base de datos"}), 500
    
    cursor = connection.cursor(dictionary=True)  # Creamos un cursor con formato de diccionario
    try:
        # Insertamos la nueva tarea en la base de datos
        sql = "INSERT INTO todos (title) VALUES (%s)"
        cursor.execute(sql, (data['title'],))
        connection.commit()  # Confirmamos la transacción
        
        # Obtenemos la tarea recién creada
        sql = "SELECT * FROM todos WHERE id = %s"
        cursor.execute(sql, (cursor.lastrowid,))
        new_todo = cursor.fetchone()
        
        return jsonify(new_todo), 201  # Retornamos la tarea creada con código 201 (Created)
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500  # Manejo de errores en caso de fallo en la base de datos
    finally:
        cursor.close()  # Cerramos el cursor
        connection.close()  # Cerramos la conexión a la base de datos


# Obtener todas las tareas (READ)
@app.route('/todos', methods=['GET'])
def get_todos():
    """Obtiene todas las tareas almacenadas en la base de datos."""
    connection = get_db_connection()  # Establecemos la conexión con la base de datos
    if not connection:
        return jsonify({"error": "Error de conexión a la base de datos"}), 500
    
    cursor = connection.cursor(dictionary=True)  # Creamos un cursor con formato de diccionario
    try:
        # Consultamos todas las tareas ordenadas por fecha de creación descendente
        cursor.execute("SELECT * FROM todos ORDER BY created_at DESC")
        todos = cursor.fetchall()  # Obtenemos todas las tareas
        
        return jsonify(todos)  # Retornamos la lista de tareas en formato JSON
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500  # Manejo de errores en caso de fallo en la base de datos
    finally:
        cursor.close()  # Cerramos el cursor
        connection.close()  # Cerramos la conexión a la base de datos


# Obtener una tarea específica (READ)
@app.route('/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    """Obtiene una tarea específica por su ID."""
    connection = get_db_connection()  # Establecemos la conexión con la base de datos
    if not connection:
        return jsonify({"error": "Error de conexión a la base de datos"}), 500
    
    cursor = connection.cursor(dictionary=True)  # Creamos un cursor con formato de diccionario
    try:
        # Consultamos la tarea con el ID proporcionado
        cursor.execute("SELECT * FROM todos WHERE id = %s", (todo_id,))
        todo = cursor.fetchone()  # Obtenemos la tarea
        
        # Si no se encuentra la tarea, devolvemos un error 404 (Not Found)
        if todo is None:
            return jsonify({"error": "Tarea no encontrada"}), 404
            
        return jsonify(todo)  # Retornamos la tarea encontrada en formato JSON
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500  # Manejo de errores en caso de fallo en la base de datos
    finally:
        cursor.close()  # Cerramos el cursor
        connection.close()  # Cerramos la conexión a la base de datos


# Ruta para actualizar una tarea (UPDATE)
@app.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    # Obtener los datos enviados en el cuerpo de la solicitud
    data = request.get_json()
    
    # Obtener una conexión a la base de datos
    connection = get_db_connection()
    
    # Si no hay conexión a la base de datos, devolver un error 500
    if not connection:
        return jsonify({"error": "Error de conexión a la base de datos"}), 500
    
    # Crear un cursor para ejecutar consultas SQL
    cursor = connection.cursor(dictionary=True)
    try:
        # Verificar si la tarea con el ID proporcionado existe en la base de datos
        cursor.execute("SELECT * FROM todos WHERE id = %s", (todo_id,))
        todo = cursor.fetchone()
        
        # Si la tarea no existe, devolver un error 404
        if todo is None:
            return jsonify({"error": "Tarea no encontrada"}), 404
        
        # Actualizar la tarea con los datos proporcionados (si no se proporciona un valor, se usa el actual)
        sql = "UPDATE todos SET title = %s, completed = %s WHERE id = %s"
        title = data.get('title', todo['title'])
        completed = data.get('completed', todo['completed'])
        cursor.execute(sql, (title, completed, todo_id))
        
        # Confirmar los cambios en la base de datos
        connection.commit()
        
        # Obtener la tarea actualizada
        cursor.execute("SELECT * FROM todos WHERE id = %s", (todo_id,))
        updated_todo = cursor.fetchone()
        
        # Devolver la tarea actualizada como respuesta
        return jsonify(updated_todo)
    
    except mysql.connector.Error as err:
        # En caso de error en la consulta, devolver un mensaje de error
        return jsonify({"error": str(err)}), 500
    
    finally:
        # Cerrar el cursor y la conexión
        cursor.close()
        connection.close()


# Ruta para eliminar una tarea (DELETE)
@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    # Obtener una conexión a la base de datos
    connection = get_db_connection()
    
    # Si no hay conexión a la base de datos, devolver un error 500
    if not connection:
        return jsonify({"error": "Error de conexión a la base de datos"}), 500
    
    # Crear un cursor para ejecutar consultas SQL
    cursor = connection.cursor(dictionary=True)
    try:
        # Verificar si la tarea con el ID proporcionado existe
        cursor.execute("SELECT * FROM todos WHERE id = %s", (todo_id,))
        todo = cursor.fetchone()
        
        # Si la tarea no existe, devolver un error 404
        if todo is None:
            return jsonify({"error": "Tarea no encontrada"}), 404
        
        # Eliminar la tarea de la base de datos
        cursor.execute("DELETE FROM todos WHERE id = %s", (todo_id,))
        
        # Confirmar los cambios
        connection.commit()
        
        # Devolver un estado 204 sin contenido, ya que la tarea fue eliminada
        return '', 204
    
    except mysql.connector.Error as err:
        # En caso de error, devolver un mensaje de error
        return jsonify({"error": str(err)}), 500
    
    finally:
        # Cerrar el cursor y la conexión
        cursor.close()
        connection.close()

# Manejo de errores: Solicitud incorrecta (400)
@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": "Solicitud incorrecta"}), 400

# Manejo de errores: Recurso no encontrado (404)
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Recurso no encontrado"}), 404

# Manejo de errores: Error interno del servidor (500)
@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({"error": "Error interno del servidor"}), 500

# Iniciar la aplicación en modo de depuración
if __name__ == '__main__':
    app.run(debug=True)
