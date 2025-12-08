from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from .extensions import db
from .models import Order, Product, OrderItem

orders_bp = Blueprint('orders', __name__)

@orders_bp.route('/')
@login_required
def menu():
    orders = Order.query.order_by(Order.created_at.desc()).all()
    # Asume que 'menu.html' es la plantilla del menú principal
    return render_template('menu.html', orders=orders)

@orders_bp.route('/order/new', methods=['GET', 'POST'])
@login_required
def new_order():
    if request.method == 'POST':
        order_number = request.form['order_number']
        
        # 1. Validar duplicado antes de insertar
        if Order.query.filter_by(order_number=order_number).first():
            flash('Número de orden ya existe', 'danger') # Añadir categoría 'danger' para mejor estilo Bootstrap
            # Asegúrate de volver a pasar el formulario si es necesario
            return render_template('new_order.html') 

        order = Order(
            order_number=order_number,
            customer_name=request.form['customer_name'],
            address=request.form['address'],
            phone=request.form['phone'],
            commune=request.form['commune'],
            region=request.form['region']
        )
        
        try:
            db.session.add(order)
            
            # 2. PROCESAMIENTO DE PRODUCTOS
            names = request.form.getlist('product_name')
            prices = request.form.getlist('product_price')
            qtys = request.form.getlist('product_qty')
            
            for n, p, q in zip(names, prices, qtys):
                # Saltar si el nombre, precio o cantidad están vacíos
                if not n or not p or not q: 
                    continue
                
                # CONVERSIÓN CRÍTICA: Decimal a Entero (Centavos)
                try:
                    # El usuario ingresa un decimal (ej. '10.50')
                    price_float = float(p) 
                    
                    # Multiplicar por 100, redondear (para evitar 10.500000000000001) y convertir a entero.
                    price_in_cents = int(round(price_float * 100))
                    
                    qty_val = int(q)
                except ValueError:
                    # Si el precio o cantidad no son números válidos, saltar este item o manejar el error.
                    flash(f'Error: El precio o cantidad del producto "{n}" no es válido.', 'warning')
                    continue
                    
                # Crear Producto y OrderItem
                # El campo Product.price ahora almacena price_in_cents (entero)
                product = Product(name=n, price=price_in_cents) 
                
                db.session.add(product)
                db.session.flush() # Obtener el ID del producto antes del commit
                
                item = OrderItem(order=order, product=product, quantity=qty_val)
                db.session.add(item)
                
            db.session.commit()
            flash('Orden creada', 'success') # Añadir categoría 'success'
            return redirect(url_for('orders.menu'))
            
        except Exception as e:
            db.session.rollback()
            # En un entorno real, es mejor loguear 'str(e)' y mostrar un mensaje genérico al usuario
            flash('Error al crear orden: ocurrió un problema en el sistema.', 'danger') 
            return render_template('new_order.html')
            
    # Manejo del método GET
    return render_template('new_order.html')