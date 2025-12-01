from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from .extensions import db
from .models import Order, Product, OrderItem

orders_bp = Blueprint('orders', __name__)

@orders_bp.route('/')
@login_required
def menu():
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template('menu.html', orders=orders)

@orders_bp.route('/order/new', methods=['GET', 'POST'])
@login_required
def new_order():
    if request.method == 'POST':
        order_number = request.form['order_number']
        # validar duplicado antes de insertar
        if Order.query.filter_by(order_number=order_number).first():
            flash('Número de orden ya existe')
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
            # productos simples (name, price, quantity)
            names = request.form.getlist('product_name')
            prices = request.form.getlist('product_price')
            qtys = request.form.getlist('product_qty')
            for n, p, q in zip(names, prices, qtys):
                if not n:
                    continue
                price_val = float(p) if p else 0.0
                qty_val = int(q) if q else 1
                product = Product(name=n, price=price_val)
                db.session.add(product)
                db.session.flush()
                item = OrderItem(order=order, product=product, quantity=qty_val)
                db.session.add(item)
            db.session.commit()
            flash('Orden creada')
            return redirect(url_for('orders.menu'))
        except Exception as e:
            db.session.rollback()
            flash('Error al crear orden: ' + str(e))
            return render_template('new_order.html')
    return render_template('new_order.html')
