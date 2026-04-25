from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from models import db, Product, Order, OrderItem

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///brewtime.db'
app.config['SECRET_KEY'] = 'brew-time-secret-2024'  # needed for session
db.init_app(app)

# --- Barista access code (hardcoded) ---
BARISTA_CODE = '1234'

# ---------- Customer Routes ----------
@app.route('/')
def menu():
    products = Product.query.all()
    return render_template('index.html', products=products)

@app.route('/place_order', methods=['POST'])
def place_order():
    data = request.get_json()
    if not data or not data.get('items'):
        return jsonify({'error': 'Cart is empty'}), 400

    order = Order(status='Pending')
    db.session.add(order)
    total = 0.0
    for item in data['items']:
        product = Product.query.get(item['product_id'])
        if not product:
            continue
        qty = item['quantity']
        total += product.price * qty
        order_item = OrderItem(product=product, quantity=qty)
        db.session.add(order_item)
    order.total_price = total
    db.session.commit()
    return jsonify({'order_id': order.id, 'status': order.status})

@app.route('/track')
def track_order():
    # Optional: pass order_id via query param ?order_id=123
    return render_template('track.html')

@app.route('/status/<int:order_id>')
def get_status(order_id):
    order = Order.query.get_or_404(order_id)
    # Build item summary
    items = [{'name': i.product.name, 'qty': i.quantity} for i in order.items]
    return jsonify({
        'order_id': order.id,
        'status': order.status,
        'total': order.total_price,
        'items': items
    })

# ---------- Barista Routes ----------
@app.route('/barista/login', methods=['GET', 'POST'])
def barista_login():
    error = None
    if request.method == 'POST':
        if request.form.get('code') == BARISTA_CODE:
            session['barista_logged_in'] = True
            return redirect(url_for('barista_dashboard'))
        else:
            error = 'Invalid access code. Please try again.'
    return render_template('barista_login.html', error=error)

@app.route('/barista')
def barista_dashboard():
    if not session.get('barista_logged_in'):
        return redirect(url_for('barista_login'))
    return render_template('barista.html')

@app.route('/orders')
def get_active_orders():
    orders = Order.query.filter(Order.status != 'Completed').order_by(Order.created_at).all()
    result = []
    for o in orders:
        items = [{'name': i.product.name, 'qty': i.quantity} for i in o.items]
        result.append({
            'id': o.id,
            'status': o.status,
            'items': items,
            'total': o.total_price,
            'created_at': o.created_at.strftime('%H:%M:%S')
        })
    return jsonify(result)

@app.route('/update_status/<int:order_id>', methods=['POST'])
def update_status(order_id):
    if not session.get('barista_logged_in'):
        return jsonify({'error': 'Unauthorized'}), 403

    new_status = request.json.get('status')
    order = Order.query.get_or_404(order_id)

    # Allowed transitions
    allowed = {
        'Pending': ['Preparing'],
        'Preparing': ['Ready'],
        'Ready': ['Completed']
    }
    if new_status not in allowed.get(order.status, []):
        return jsonify({'error': 'Invalid status transition'}), 400

    order.status = new_status
    db.session.commit()
    return jsonify({'success': True})

@app.route('/barista/logout')
def barista_logout():
    session.pop('barista_logged_in', None)
    return redirect(url_for('barista_login'))

# ---------- Run ----------
if __name__ == '__main__':
    app.run(debug=True)

