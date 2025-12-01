from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from .extensions import db
from .models import Order, Invoice # Asegúrate de que OrderItem y Product sean accesibles

invoices_bp = Blueprint('invoices', __name__, url_prefix='/invoices')

@invoices_bp.route('/create/<int:order_id>', methods=['POST'])
@login_required
def create_invoice(order_id):
    order = Order.query.get_or_404(order_id)
    
    if order.status == 'facturada':
        flash('Orden ya facturada')
        # Asume que 'orders.menu' es la ruta a tu menú principal
        return redirect(url_for('orders.menu')) 
    
    # 1. CALCULAR TOTAL NETO (En Centavos)
    # item.product.price y item.quantity son enteros
    total_net_cents = sum(item.product.price * item.quantity for item in order.items)
    
    # 2. CALCULAR IVA (0.19)
    iva_rate = 0.19
    
    # Se calcula el IVA y se asegura que el resultado sea un entero (centavos)
    # Se multiplica el total_net_cents por 0.19, se redondea a 0 decimales y se convierte a entero.
    # Esto asegura precisión en el centavo.
    total_iva_cents = int(round(total_net_cents * iva_rate))
    
    # 3. CALCULAR TOTAL CON IMPUESTOS (En Centavos)
    total_with_tax_cents = total_net_cents + total_iva_cents

    # 4. CREAR FACTURA
    inv = Invoice(
        order=order, 
        iva_rate=iva_rate, 
        total_net=total_net_cents, # Se guardan los enteros
        total_iva=total_iva_cents,   # Se guardan los enteros
        total_with_tax=total_with_tax_cents # Se guardan los enteros
    )
    
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
    # Se usa la plantilla adaptada 'invoice.html' (que divide los valores por 100 para mostrar)
    return render_template('invoice.html', order=order, invoice=inv)