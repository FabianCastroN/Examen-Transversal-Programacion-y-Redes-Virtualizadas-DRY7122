from flask import Flask, request, redirect, render_template_string
import sqlite3
import hashlib

app = Flask(__name__)
PUERTO = 5800

# Crear tabla si no existe
def inicializar_bd():
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            clave_hash TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Convertir clave a hash
def generar_hash(clave):
    return hashlib.sha256(clave.encode()).hexdigest()

# Página principal
@app.route('/')
def home():
    return render_template_string('''
        <h2>Registrar nuevo usuario</h2>
        <form method="post" action="/registrar">
            Nombre: <input name="nombre"><br>
            Clave: <input type="password" name="clave"><br>
            <input type="submit" value="Registrar">
        </form>

        <h2>Iniciar sesión</h2>
        <form method="post" action="/login">
            Nombre: <input name="nombre"><br>
            Clave: <input type="password" name="clave"><br>
            <input type="submit" value="Ingresar">
        </form>
    ''')

# Ruta para registrar
@app.route('/registrar', methods=['POST'])
def registrar():
    nombre = request.form['nombre']
    clave = request.form['clave']
    hash_clave = generar_hash(clave)

    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO usuarios (nombre, clave_hash) VALUES (?, ?)', (nombre, hash_clave))
    conn.commit()
    conn.close()
    return redirect('/')

# Ruta para login
@app.route('/login', methods=['POST'])
def login():
    nombre = request.form['nombre']
    clave = request.form['clave']
    hash_clave = generar_hash(clave)

    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuarios WHERE nombre=? AND clave_hash=?', (nombre, hash_clave))
    resultado = cursor.fetchone()
    conn.close()

    if resultado:
        return f"<h2>✅ Bienvenido, {nombre}</h2>"
    else:
        return "<h2>❌ Usuario o clave incorrectos</h2>"

if __name__ == '__main__':
    inicializar_bd()
    app.run(host='0.0.0.0', port=PUERTO)
