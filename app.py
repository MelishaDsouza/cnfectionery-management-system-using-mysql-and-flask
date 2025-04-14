from flask import Flask , render_template, request, redirect
from db_config import get_db_connection
import mysql.connector

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')


#ADD ORDER
@app.route('/add-order', methods=['POST'])
def add_order():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get customer name and item lists
    customer_name = request.form['customer_name']
    cake_types = request.form.getlist('cake_type[]')
    quantities = request.form.getlist('quantity[]')
    prices = request.form.getlist('price_per_item[]')

    grand_total = 0.0

    try:
        for cake, qty_str, price_str in zip(cake_types, quantities, prices):
            qty = int(qty_str)
            price = float(price_str)
            total = qty * price
            grand_total += total

            cursor.execute("""
                INSERT INTO orders (customer_name, cake_type, quantity, price_per_item, total_price)
                VALUES (%s, %s, %s, %s, %s)
            """, (customer_name, cake, qty, price, total))

        conn.commit()
        print(f"✅ Order for {customer_name} added. Grand Total: ₹{grand_total:.2f}")

    except mysql.connector.Error as err:
        print("❌ MySQL Error:", err)
    finally:
        cursor.close()
        conn.close()

    return redirect('/orders')

# @app.route('/add-order', methods=['POST'])
# def add_order():
#     conn = get_db_connection()
#     cursor = conn.cursor()

#     name=request.form['customer_name']
#     cake=request.form['cake_type']
#     qty = int(request.form['quantity'])
#     price = float(request.form['price_per_item'])
#     total = qty * price

#     try:

#         cursor.execute("""
#              INSERT INTO orders (customer_name, cake_type, quantity, price_per_item, total_price)
#              VALUES (%s, %s, %s, %s, %s)
#         """, (name, cake, qty, price, total))

#         conn.commit()
#     except mysql.connector.Error as err:
#          print("MySQL Error:", err)

#     conn.commit()
#     cursor.close()
#     conn.close()
#     return redirect('/orders')


# MODIFY ORDER
@app.route('/edit-order/<int:order_id>', methods=['POST'])
def edit_order(order_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    name = request.form['customer_name']
    cake = request.form['cake_type']
    qty = int(request.form['quantity'])
    price = float(request.form['price_per_item'])
    total = qty * price

    cursor.execute("""
        UPDATE orders
        SET customer_name = %s, cake_type = %s, quantity = %s, price_per_item = %s, total_price = %s
        WHERE order_id = %s
    """, (name, cake, qty, price, total, order_id))
    
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/orders')

# DELETE ORDER
@app.route('/delete-order/<int:order_id>', methods=['POST'])
def delete_order(order_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM orders WHERE order_id = %s", (order_id,))
    
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/orders')

# DISPLAY ORDERS
@app.route('/orders')
def list_orders():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM orders ORDER BY order_date DESC")
    orders = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template("orders.html", orders=orders)