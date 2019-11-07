def qr_register_product(product, owner_id):
    return f"INSERT INTO product(name, description, category, price, stock, owner_id) \
        VALUES ('{product['name']}', '{product['description']}', {product['category_id']}, {product['price']}, {product['stock']}, {owner_id})"

def qr_get_products():
    return "SELECT * FROM product;"