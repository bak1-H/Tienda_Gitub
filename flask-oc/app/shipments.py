from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from .extensions import db
from .models import Invoice, Shipment, Order

shipments_bp = Blueprint('shipments', __name__, url_prefix='/shipments')

@shipments_bp.route('/dispatch/<int:invoice_id>', methods=['POST'])
@login_required
def dispatch(invoice_id):
    invoice = Invoice.query.get_or_404(invoice_id)
    note = request.form.get('note', 'Despachado')
    shipment = Shipment(invoice=invoice, note=note)
    db.session.add(shipment)
    # marcar orden como despachada
    invoice.order.status = 'despachada'
    db.session.commit()
    flash('Productos despachados')
    return redirect(url_for('orders.menu'))
