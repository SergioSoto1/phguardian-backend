from flask import Flask, request, jsonify
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()  # Cargar las variables de entorno desde el archivo .env

app = Flask(__name__)

# Configuración de la base de datos
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        print("Conexión a la base de datos exitosa!")
        return conn
    except psycopg2.Error as e:
        print("Error connecting to PostgreSQL:", e)
        return None

@app.route('/data', methods=['GET'])
def get_data():
    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        cur.execute('SELECT * FROM lecturas_sensor')
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(rows)
    else:
        return jsonify({"error": "No se pudo conectar a la base de datos"})

@app.route('/data', methods=['POST'])
def post_data():
    data = request.json
    if not data:
        return jsonify({"error": "No se proporcionaron datos"})
    
    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        for item in data:
            fecha_hora = item.get('fecha_hora')
            ph = item.get('ph')
            humedad = item.get('humedad')
            temperatura = item.get('temperatura')
            usuario_rut = item.get('usuario_rut')

            cur.execute('INSERT INTO lecturas_sensor (fecha_hora, ph, humedad, temperatura, usuario_rut) VALUES (%s, %s, %s, %s, %s)',
                        (fecha_hora, ph, humedad, temperatura, usuario_rut))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Datos insertados correctamente"})
    else:
        return jsonify({"error": "No se pudo conectar a la base de datos"})

@app.route('/')
def index():
    return jsonify({"message": "Hello, World!"})

if __name__ == '__main__':
    app.run(debug=True)
