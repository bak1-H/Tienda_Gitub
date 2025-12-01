from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from .extensions import db
from .models import Order, Invoice

invoices_bp = Blueprint('invoices', __name__, url_prefix='/invoices')

@invoices_bp.route('/create/<int:order_id>', methods=['POST'])
@login_required
def create_invoice(order_id):
    order = Order.query.get_or_404(order_id)
    if order.status == 'facturada':
        flash('Orden ya facturada')
        return redirect(url_for('orders.menu'))
    # calcular totales
    total_net = sum(item.product.price * item.quantity for item in order.items)
    iva_rate = 0.19
    total_iva = total_net * iva_rate
    total_with_tax = total_net + total_iva

    inv = Invoice(order=order, iva_rate=iva_rate, total_net=total_net,
                  total_iva=total_iva, total_with_tax=total_with_tax)
    order.status = 'facturada'
    db.session.add(inv)
    db.session.commit()
    flash('Factura emitida')
    return redirect(url_for('orders.menu'))

@invoices_bp.route('/<int:order_id>')
@login_required
def view_invoice(order_id):
    order = Order.query.get_or_404(order_id)
    inv = order.invoice
    return render_template('invoice.html', order=order, invoice=inv)
