def create_tables(connection):
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            hashed_password VARCHAR(200) NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS uom (
            uom_id INT AUTO_INCREMENT PRIMARY KEY,
            uom_name VARCHAR(50) NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id INT AUTO_INCREMENT PRIMARY KEY,
            product_name VARCHAR(150) NOT NULL,
            uom_id INT NOT NULL,
            price_per_unit FLOAT NOT NULL,
            is_active TINYINT(1) NOT NULL DEFAULT 1,
            FOREIGN KEY (uom_id) REFERENCES uom(uom_id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id INT AUTO_INCREMENT PRIMARY KEY,
            customer_name VARCHAR(150) NOT NULL,
            date DATETIME NOT NULL,
            total_cost FLOAT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders_details (
            id INT AUTO_INCREMENT PRIMARY KEY,
            order_id INT NOT NULL,
            product_id INT NOT NULL,
            quantity INT NOT NULL,
            total_price FLOAT NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(order_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM uom")
    (count,) = cursor.fetchone()
    if count == 0:
        cursor.executemany(
            "INSERT INTO uom (uom_name) VALUES (%s)",
            [("kg",), ("litre",), ("piece",), ("dozen",)]
        )

    connection.commit()
    cursor.close()