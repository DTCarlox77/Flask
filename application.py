from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv
from cs50 import SQL

load_dotenv()

app = Flask(__name__)

db = SQL('sqlite:///database.db')

def create_table():
    db.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            precio REAL NOT NULL
        )
    ''')
    
create_table()

lista_productos = []

@app.route('/')
def main():
    return 'Hello world'

@app.route('/productos', methods=['GET', 'POST'])
def productos():
    
    # Obtención de todos los productos de la tabla productos
    lista_productos = db.execute('SELECT * FROM productos')
    
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        precio = request.form.get('precio')
        
        try:
            precio = float(precio)
            # Inserción de un producto en la base de datos
            db.execute(f'''
                INSERT INTO productos (nombre, precio)
                VALUES (?, ?)
            ''', nombre, precio)
        except:
            print('Hubo un error al insertar el producto')
            return 'El precio debe ser un número'
        
    return render_template('commerce/pages/products.html', lista_productos=lista_productos)

@app.route('/productos/<int:id>', methods=['GET', 'POST'])
def producto_especifico(id):
    
    # Obtención de un producto de la base de datos dada su PK
    producto = db.execute('SELECT * FROM productos WHERE id = ?', id)
    
    return render_template('commerce/pages/product.html', producto=producto[0])

@app.route('/productos/<int:id>/eliminar', methods=['GET', 'POST'])
def eliminar_producto(id):
    
    # Eliminación de un producto de la base de datos dada su PK
    db.execute('DELETE FROM productos WHERE id = ?', id)
    
    return redirect(url_for('productos'))

if __name__ == '__main__':
    
    app.run(debug=True)