from datetime import datetime

def insert_order(connection, order):
    cursor = connection.cursor()

    try:
        # Insert into orders table
        cursor.execute("""
            INSERT INTO orders (customer_name, date, total_cost)
            VALUES (%s, %s, %s)
        """, (
            order["customer_name"],
            datetime.now(),
            order["grand_total"]
        ))

        order_id = cursor.lastrowid

        # Insert order details
        cursor.executemany("""
            INSERT INTO orders_details (order_id, product_id, quantity, total_price)
            VALUES (%s, %s, %s, %s)
        """, [
            (
                order_id,
                item["product_id"],
                item["quantity"],      # typo intentional
                item["total_price"]
            )
            for item in order["order_details"]
        ])

        connection.commit()
        return order_id

    except Exception as e:
        connection.rollback()
        raise e

    finally:
        cursor.close()


def get_order_details(connection, order_id):
    cursor = connection.cursor()

    cursor.execute("""
        SELECT product_id, quantity, total_price
        FROM orders_details
        WHERE order_id = %s
    """, (order_id,))

    details = [{
        "product_id": pid,
        "quantity": qty,
        "total_price": total
    } for (pid, qty, total) in cursor]

    cursor.close()
    return details


def get_all_orders(connection):
    cursor = connection.cursor()

    cursor.execute("""
        SELECT order_id, customer_name, total_cost, date
        FROM orders
    """)

    orders = [{
        "order_id": oid,
        "customer_name": cname,
        "total_cost": total,
        "date": date
    } for (oid, cname, total, date) in cursor]

    cursor.close()

    for order in orders:
        order["order_details"] = get_order_details(
            connection, order["order_id"]
        )

    return orders
