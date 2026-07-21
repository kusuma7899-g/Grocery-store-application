from sql_connection import get_sql_connection

def get_all_products(connection):
    cursor = connection.cursor()
    query = """
    SELECT p.product_id, p.product_name, p.uom_id, 
           p.price_per_unit, u.uom_name
    FROM products p
    INNER JOIN uom u ON p.uom_id = u.uom_id
    WHERE p.is_active = 1
    """
    cursor.execute(query)

    response = []
    for (product_id, product_name, uom_id, price_per_unit, uom_name) in cursor:
        response.append({
            'product_id': product_id,
            'product_name': product_name,
            'uom_id': uom_id,
            'price_per_unit': price_per_unit,
            'uom_name': uom_name
        })
    return response

def insert_new_product(connection, product):
    cursor = connection.cursor()
    query = """
    INSERT INTO products (product_name, uom_id, price_per_unit)
    VALUES (%s, %s, %s)
    """
    data = (product['product_name'], product['uom_id'], product['price_per_unit'])
    cursor.execute(query, data)
    connection.commit()
    return cursor.lastrowid

def delete_product(connection, product_id):
    cursor = connection.cursor()
    query = """
    UPDATE products
    SET is_active = 0
    WHERE product_id = %s
    """
    cursor.execute(query, (product_id,))
    connection.commit()
    return product_id


if __name__ == '__main__':
    connection = get_sql_connection()
    print(insert_new_product(connection, {
        'product_name': 'potatoes',
        'uom_id': 1,
        'price_per_unit': 10
    }))
