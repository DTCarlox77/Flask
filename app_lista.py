from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

lista_productos = []

@app.route('/')
def main():
    return 'Hello world'

@app.route('/productos', methods=['GET', 'POST'])
def productos():
    
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        precio = request.form.get('precio')
        
        lista_productos.append({
            'id' : len(lista_productos) + 1,
            'nombre': nombre,
            'precio': precio
        })
        
    return render_template('commerce/pages/products.html', lista_productos=lista_productos)

@app.route('/productos/<int:id>', methods=['GET', 'POST'])
def producto_especifico(id):
    
    producto = lista_productos[id - 1]
    
    return render_template('commerce/pages/product.html', producto=producto)

@app.route('/productos/<int:id>/eliminar', methods=['GET', 'POST'])
def eliminar_producto(id):
    
    lista_productos.pop(id - 1)
    
    return redirect(url_for('productos'))

if __name__ == '__main__':
    app.run(debug=True)