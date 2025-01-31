from flask import Flask, request, jsonify
from flask_cors import CORS
from db import get_db_connection
import mysql.connector

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({"message": "Bienvenido a la API de Tareas con MySQL"})


# Crear una nueva tarea (CREATE)
@app.route('/todos', methods=['POST'])
def create_todo():
    data = request.get_json()
    
    if 'title' not in data:
        return jsonify({"error": "El título es requerido"}), 400
    
    connection = get_db_connection()
    if not connection:
        return jsonify({"error": "Error de conexión a la base de datos"}), 500
    
    cursor = connection.cursor(dictionary=True)
    try:
        sql = "INSERT INTO todos (title) VALUES (%s)"
        cursor.execute(sql, (data['title'],))
        connection.commit()
        
        # Obtener la tarea recién creada
        sql = "SELECT * FROM todos WHERE id = %s"
        cursor.execute(sql, (cursor.lastrowid,))
        new_todo = cursor.fetchone()
        
        return jsonify(new_todo), 201
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        connection.close()

# Obtener todas las tareas (READ)
@app.route('/todos', methods=['GET'])
def get_todos():
    connection = get_db_connection()
    if not connection:
        return jsonify({"error": "Error de conexión a la base de datos"}), 500
    
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM todos ORDER BY created_at DESC")
        todos = cursor.fetchall()
        return jsonify(todos)
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        connection.close()

# Obtener una tarea específica (READ)
@app.route('/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    connection = get_db_connection()
    if not connection:
        return jsonify({"error": "Error de conexión a la base de datos"}), 500
    
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM todos WHERE id = %s", (todo_id,))
        todo = cursor.fetchone()
        
        if todo is None:
            return jsonify({"error": "Tarea no encontrada"}), 404
            
        return jsonify(todo)
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        connection.close()

# Actualizar una tarea (UPDATE)
@app.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    data = request.get_json()
    connection = get_db_connection()
    if not connection:
        return jsonify({"error": "Error de conexión a la base de datos"}), 500
    
    cursor = connection.cursor(dictionary=True)
    try:
        # Verificar si la tarea existe
        cursor.execute("SELECT * FROM todos WHERE id = %s", (todo_id,))
        todo = cursor.fetchone()
        
        if todo is None:
            return jsonify({"error": "Tarea no encontrada"}), 404
        
        # Actualizar la tarea
        sql = "UPDATE todos SET title = %s, completed = %s WHERE id = %s"
        title = data.get('title', todo['title'])
        completed = data.get('completed', todo['completed'])
        cursor.execute(sql, (title, completed, todo_id))
        connection.commit()
        
        # Obtener la tarea actualizada
        cursor.execute("SELECT * FROM todos WHERE id = %s", (todo_id,))
        updated_todo = cursor.fetchone()
        
        return jsonify(updated_todo)
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        connection.close()

# Eliminar una tarea (DELETE)
@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    connection = get_db_connection()
    if not connection:
        return jsonify({"error": "Error de conexión a la base de datos"}), 500
    
    cursor = connection.cursor(dictionary=True)
    try:
        # Verificar si la tarea existe
        cursor.execute("SELECT * FROM todos WHERE id = %s", (todo_id,))
        todo = cursor.fetchone()
        
        if todo is None:
            return jsonify({"error": "Tarea no encontrada"}), 404
        
        # Eliminar la tarea
        cursor.execute("DELETE FROM todos WHERE id = %s", (todo_id,))
        connection.commit()
        
        return '', 204
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        connection.close()
        

@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": "Solicitud incorrecta"}), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Recurso no encontrado"}), 404

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({"error": "Error interno del servidor"}), 500


if __name__ == '__main__':
    app.run(debug=True)