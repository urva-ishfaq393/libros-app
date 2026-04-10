import logging
import os
import time
import mysql.connector
from flask import Flask, render_template
from forms import LibroForm
from flask_wtf.csrf import CSRFProtect
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'devSecretKey123')
csrf = CSRFProtect(app)

logging.basicConfig(level=logging.DEBUG)

DB_HOST = os.environ.get('DB_HOST', 'db')
DB_USER = os.environ.get('DB_USER', 'root')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'rootpassword')
DB_NAME = os.environ.get('DB_NAME', 'libros_db')

def get_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

def init_db():
    for attempt in range(10):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS libros (
                    id VARCHAR(36) PRIMARY KEY,
                    titulo VARCHAR(100) NOT NULL,
                    autor VARCHAR(100) NOT NULL,
                    genero VARCHAR(50) NOT NULL,
                    anio_publicacion INT NOT NULL,
                    editorial VARCHAR(100) NOT NULL
                )
            """)
            conn.commit()
            cursor.close()
            conn.close()
            logging.info("Database initialized successfully.")
            return
        except Exception as e:
            logging.warning(f"DB not ready (attempt {attempt+1}/10): {e}")
            time.sleep(3)

init_db()

@app.route('/')
def home():
    form = LibroForm()
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM libros ORDER BY titulo")
    libros = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', form=form, libros=libros)

@app.route('/registrar_libro', methods=['GET', 'POST'])
def registrar_libro():
    form = LibroForm()
    if form.validate_on_submit():
        libro_id = str(uuid.uuid4())
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO libros (id, titulo, autor, genero, anio_publicacion, editorial) "
                "VALUES (%s, %s, %s, %s, %s, %s)",
                (libro_id, form.titulo.data, form.autor.data,
                 form.genero.data, form.anio_publicacion.data, form.editorial.data)
            )
            conn.commit()
            cursor.close()
            conn.close()
            return render_template('exito.html')
        except Exception as ex:
            logging.error(f'Error: {ex}')
            return render_template('index.html', form=form, error=str(ex), libros=[])
    return render_template('index.html', form=form, libros=[])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
