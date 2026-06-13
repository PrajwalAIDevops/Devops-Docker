from flask import Flask, request, redirect, url_for, render_template_string

app = Flask(__name__)
app.secret_key = "dev"

# In-memory catalog (replace with DB later)
PRODUCTS = [
    {
        "id": "p1",
        "name": "Wireless Headphones",
        "price": 59.99,
        "desc": "Comfort fit with clear sound.",
        "image": "https://via.placeholder.com/300x220.png?text=Headphones",
    },
    {
        "id": "p2",
        "name": "Smart Watch",
        "price": 79.99,
        "desc": "Track steps, sleep & workouts.",
        "image": "https://via.placeholder.com/300x220.png?text=Smart+Watch",
    },
    {
        "id": "p3",
        "name": "Mechanical Keyboard",
        "price": 109.99,
        "desc": "Tactile switches, smooth typing.",
        "image": "https://via.placeholder.com/300x220.png?text=Keyboard",
    },
]

# Simple cart stored per client using cookie-like hidden field (server-side not used here)
# For production use sessions/redis/db.

STORE_HTML = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{{ title }}</title>
  <style>
    body{font-family:Arial,Helvetica,sans-serif;margin:0;background:#0b1220;color:#e6edf3}
    header{padding:18px 20px;background:#0f172a;border-bottom:1px solid rgba(255,255,255,.08)}
    .wrap{max-width:1100px;margin:0 auto;padding:0 20px}
    h1{margin:0;font-size:20px}
    .row{display:flex;gap:14px;flex-wrap:wrap;align-items:center;justify-content:space-between}
    .btn{display:inline-block;background:#60a5fa;color:#0b1220;text-decoration:none;padding:10px 14px;border-radius:10px;font-weight:700;border:0;cursor:pointer}
    .btn2{background:#a78bfa}
    .content{padding:22px 0}
    .grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
    @media(max-width:980px){.grid{grid-template-columns:repeat(2,1fr)}}
    @media(max-width:620px){.grid{grid-template-columns:1fr}}
    .card{background:#111827;border:1px solid rgba(255,255,255,.08);border-radius:12px;padding:14px}
    .img{width:100%;height:180px;background:#0b1220;border-radius:10px;object-fit:cover}
    .name{font-weight:800;margin:10px 0 6px}
    .price{font-weight:800;color:#93c5fd}
    .muted{opacity:.8}
    .cartbar{padding:12px 0;display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap}
    input[type=text],input[type=email]{width:100%;padding:10px;border-radius:10px;border:1px solid rgba(255,255,255,.15);background:#0b1220;color:#e6edf3}
    select{padding:10px;border-radius:10px;border:1px solid rgba(255,255,255,.15);background:#0b1220;color:#e6edf3}
    .cart{background:#111827;border:1px solid rgba(255,255,255,.08);border-radius:12px;padding:14px}
    .line{display:flex;justify-content:space-between;gap:12px;padding:8px 0;border-bottom:1px dashed rgba(255,255,255,.12)}
    .line:last-child{border-bottom:0}
    .total{font-size:18px;font-weight:900;color:#a78bfa}
    footer{padding:25px 20px;color:#94a3b8;text-align:center}
  </style>
</head>
<body>
  <header>
    <div class="wrap row">
      <h1>{{ store_name }}</h1>
      <div style="display:flex;gap:10px;flex-wrap:wrap;align-items:center">
        <a class="btn" href="{{ url_for('cart') }}">Cart ({{ cart_count }})</a>
        <a class="btn btn2" href="{{ url_for('checkout') }}">Checkout</a>
      </div>
    </div>
  </header>

  <div class="content wrap">
    <div class="grid">
      {% for p in products %}
      <div class="card">
        <img class="img" src="{{ p.image }}" alt="{{ p.name }}">
        <div class="name">{{ p.name }}</div>
        <div class="price">${{ '%.2f'|format(p.price) }}</div>
        <div class="muted" style="margin-top:8px">{{ p.desc }}</div>
        <form method="post" action="{{ url_for('add_to_cart') }}" style="margin-top:12px">
          <input type="hidden" name="product_id" value="{{ p.id }}">
          <label class="muted">Qty</label>
          <select name="qty">
            {% for q in range(1,6) %}<option value="{{ q }}">{{ q }}</option>{% endfor %}
          </select>
          <button class="btn" type="submit" style="margin-top:10px">Add to cart</button>
        </form>
      </div>
      {% endfor %}
    </div>

    <div style="height:18px"></div>
    <div class="cartbar">
      <div class="muted">Tip: This is a simple demo cart stored in-memory for the server process.</div>
      <a class="btn" href="{{ url_for('clear_cart') }}">Clear cart</a>
    </div>

  </div>

  <footer>
    <div>© {{ year }} {{ store_name }} • Flask demo ecommerce</div>
  </footer>
</body>
</html>
"""

CART_HTML = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Cart</title>
  <style>
    body{font-family:Arial,Helvetica,sans-serif;margin:0;background:#0b1220;color:#e6edf3}
    header{padding:18px 20px;background:#0f172a;border-bottom:1px solid rgba(255,255,255,.08)}
    .wrap{max-width:900px;margin:0 auto;padding:0 20px}
    .btn{display:inline-block;background:#60a5fa;color:#0b1220;text-decoration:none;padding:10px 14px;border-radius:10px;font-weight:700;border:0;cursor:pointer}
    .btn2{background:#a78bfa}
    .content{padding:22px 0}
    .cart{background:#111827;border:1px solid rgba(255,255,255,.08);border-radius:12px;padding:14px}
    .line{display:flex;justify-content:space-between;gap:12px;padding:8px 0;border-bottom:1px dashed rgba(255,255,255,.12)}
    .line:last-child{border-bottom:0}
    input[type=number]{width:90px;padding:8px;border-radius:10px;border:1px solid rgba(255,255,255,.15);background:#0b1220;color:#e6edf3}
    footer{padding:25px 20px;color:#94a3b8;text-align:center}
  </style>
</head>
<body>
  <header>
    <div class="wrap" style="display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap">
      <div><b>Cart</b> <span style="opacity:.8">({{ cart_count }} items)</span></div>
      <div style="display:flex;gap:10px;flex-wrap:wrap">
        <a class="btn" href="{{ url_for('index') }}">Continue shopping</a>
        <a class="btn btn2" href="{{ url_for('checkout') }}">Checkout</a>
      </div>
    </div>
  </header>

  <div class="content wrap">
    <div class="cart">
      {% if cart_items %}
        {% for item in cart_items %}
          <div class="line">
            <div>
              <div style="font-weight:900">{{ item.name }}</div>
              <div style="opacity:.8">${{ '%.2f'|format(item.price) }} each</div>
            </div>
            <div style="text-align:right">
              <form method="post" action="{{ url_for('update_qty') }}" style="display:inline-block">
                <input type="hidden" name="product_id" value="{{ item.id }}">
                <input type="number" min="0" name="qty" value="{{ item.qty }}">
                <button class="btn" type="submit" style="padding:8px 10px;margin-left:6px">Update</button>
              </form>
              <div style="margin-top:8px;font-weight:900">${{ '%.2f'|format(item.line_total) }}</div>
            </div>
          </div>
        {% endfor %}
        <div class="line" style="align-items:center">
          <div class="total">Total</div>
          <div class="total">${{ '%.2f'|format(cart_total) }}</div>
        </div>
      {% else %}
        <div class="muted" style="padding:10px 0;opacity:.8">Your cart is empty.</div>
      {% endif %}
    </div>
  </div>

  <footer>
    <div>Flask demo ecommerce</div>
  </footer>
</body>
</html>
"""

CHECKOUT_HTML = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Checkout</title>
  <style>
    body{font-family:Arial,Helvetica,sans-serif;margin:0;background:#0b1220;color:#e6edf3}
    header{padding:18px 20px;background:#0f172a;border-bottom:1px solid rgba(255,255,255,.08)}
    .wrap{max-width:900px;margin:0 auto;padding:0 20px}
    .btn{display:inline-block;background:#60a5fa;color:#0b1220;text-decoration:none;padding:10px 14px;border-radius:10px;font-weight:700;border:0;cursor:pointer}
    .btn2{background:#a78bfa}
    .content{padding:22px 0}
    .grid{display:grid;grid-template-columns:1fr 1fr;gap:16px}
    @media(max-width:820px){.grid{grid-template-columns:1fr}}
    .card{background:#111827;border:1px solid rgba(255,255,255,.08);border-radius:12px;padding:14px}
    input[type=text],input[type=email]{width:100%;padding:10px;border-radius:10px;border:1px solid rgba(255,255,255,.15);background:#0b1220;color:#e6edf3}
    footer{padding:25px 20px;color:#94a3b8;text-align:center}
    .muted{opacity:.8}
  </style>
</head>
<body>
  <header>
    <div class="wrap" style="display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap">
      <div><b>Checkout</b></div>
      <a class="btn" href="{{ url_for('cart') }}">Back to cart</a>
    </div>
  </header>

  <div class="content wrap">
    <div class="grid">
      <div class="card">
        <h3 style="margin-top:0">Shipping details</h3>
        <form method="post" action="{{ url_for('place_order') }}">
          <label class="muted">Full name</label>
          <input type="text" name="full_name" required placeholder="John Doe" style="margin-top:6px">

          <div style="height:10px"></div>

          <label class="muted">Email</label>
          <input type="email" name="email" required placeholder="john@example.com" style="margin-top:6px">

          <div style="height:10px"></div>

          <label class="muted">Address</label>
          <input type="text" name="address" required placeholder="Street, City" style="margin-top:6px">

          <div style="height:14px"></div>

          <button class="btn btn2" type="submit">Place order</button>
        </form>
      </div>

      <div class="card">
        <h3 style="margin-top:0">Order summary</h3>
        {% if cart_items %}
          {% for item in cart_items %}
            <div style="display:flex;justify-content:space-between;gap:12px;padding:8px 0;border-bottom:1px dashed rgba(255,255,255,.12)">
              <div>
                <b>{{ item.name }}</b>
                <div class="muted">Qty: {{ item.qty }}</div>
              </div>
              <div style="font-weight:900">${{ '%.2f'|format(item.line_total) }}</div>
            </div>
          {% endfor %}
          <div style="display:flex;justify-content:space-between;gap:12px;padding:14px 0 0">
            <div class="muted">Total</div>
            <div style="font-size:20px;font-weight:900;color:#a78bfa">${{ '%.2f'|format(cart_total) }}</div>
          </div>
        {% else %}
          <div class="muted">Cart is empty. Add items first.</div>
        {% endif %}
      </div>
    </div>
  </div>

  <footer>
    <div>Demo ecommerce • No real payments</div>
  </footer>
</body>
</html>
"""

ORDER_OK_HTML = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Order placed</title>
  <style>
    body{font-family:Arial,Helvetica,sans-serif;margin:0;background:#0b1220;color:#e6edf3}
    .wrap{max-width:900px;margin:0 auto;padding:60px 20px;text-align:center}
    .box{background:#111827;border:1px solid rgba(255,255,255,.08);border-radius:12px;padding:22px}
    .btn{display:inline-block;background:#60a5fa;color:#0b1220;text-decoration:none;padding:10px 14px;border-radius:10px;font-weight:700;margin-top:16px}
    .muted{opacity:.8}
  </style>
</head>
<body>
  <div class="wrap">
    <div class="box">
      <h1 style="margin-top:0">Order placed ✅</h1>
      <p class="muted">Thanks, {{ full_name }}. Your total was <b>${{ '%.2f'|format(cart_total) }}</b>.</p>
      <p class="muted">(Demo) No payment was processed.</p>
      <a class="btn" href="{{ url_for('index') }}">Back to shop</a>
    </div>
  </div>
</body>
</html>
"""

# ---------------- Cart logic (in-memory) ----------------
# NOTE: For demo only. In-memory means cart is shared among users on same server.
CART = {}  # product_id -> qty


def find_product(product_id: str):
    for p in PRODUCTS:
        if p["id"] == product_id:
            return p
    return None


def cart_items():
    items = []
    total = 0.0
    for pid, qty in CART.items():
        p = find_product(pid)
        if not p or qty <= 0:
            continue
        line_total = qty * float(p["price"])
        items.append({
            "id": p["id"],
            "name": p["name"],
            "price": float(p["price"]),
            "qty": qty,
            "line_total": line_total,
        })
        total += line_total
    # Stable order
    items.sort(key=lambda x: x["id"])
    return items, total


def cart_count():
    return sum(q for q in CART.values())


@app.route('/', methods=['GET'])
def index():
    items, total = cart_items()
    return render_template_string(
        STORE_HTML,
        title="Shop",
        store_name="My E-Commerce",
        products=PRODUCTS,
        cart_items=items,
        cart_total=total,
        cart_count=cart_count(),
        year=__import__('datetime').datetime.now().year,
    )


@app.route('/cart', methods=['GET'])
def cart():
    items, total = cart_items()
    return render_template_string(
        CART_HTML,
        cart_items=items,
        cart_total=total,
        cart_count=cart_count(),
    )


@app.route('/add', methods=['POST'])
def add_to_cart():
    product_id = request.form.get('product_id', '').strip()
    qty = int(request.form.get('qty', '1'))
    if qty < 1:
        qty = 1
    p = find_product(product_id)
    if p:
        CART[product_id] = CART.get(product_id, 0) + qty
    return redirect(url_for('cart'))


@app.route('/update', methods=['POST'])
def update_qty():
    product_id = request.form.get('product_id', '').strip()
    qty = int(request.form.get('qty', '0'))
    if qty <= 0:
        CART.pop(product_id, None)
    else:
        if find_product(product_id):
            CART[product_id] = qty
    return redirect(url_for('cart'))


@app.route('/clear', methods=['GET'])
def clear_cart():
    CART.clear()
    return redirect(url_for('index'))


@app.route('/checkout', methods=['GET'])
def checkout():
    items, total = cart_items()
    return render_template_string(
        CHECKOUT_HTML,
        cart_items=items,
        cart_total=total,
    )


@app.route('/order', methods=['POST'])
def place_order():
    items, total = cart_items()
    full_name = request.form.get('full_name', '').strip() or 'Customer'
    # Demo: accept order even if empty
    CART.clear()
    return render_template_string(
        ORDER_OK_HTML,
        full_name=full_name,
        cart_total=total,
    )


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)

