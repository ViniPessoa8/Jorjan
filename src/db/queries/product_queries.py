def qr_register_product(product, owner_id):
    return f"INSERT INTO product(name, description, category, price, stock, owner_id) \
        VALUES ('{product['name']}', '{product['description']}', {product['category_id']}, {product['price']}, {product['stock']}, {owner_id})"

def qr_get_products():
    print("SELECT * FROM product;")
    return "SELECT * FROM product;"

def qr_get_product_id(product_id):
    return f"SELECT * FROM product WHERE id={product_id};"

def qr_get_products_seller(seller_id):
    return f"""SELECT * FROM Jorjan.`user` u, Jorjan.product prod, Jorjan.category c
            WHERE p.owner_id={seller_id} AND u.id={seller_id} AND prod.owner_id = {seller_id}
            AND c.id = prod.category;"""

def qr_get_products_seller_category(seller_id, category_id):
    return f"""SELECT p.id, p.name, p.description, p.category, p.owner_id, p.price, p.stock   
            FROM Jorjan.product p, Jorjan.category c
            WHERE p.owner_id={seller_id} AND c.id = p.category AND p.category = {category_id};"""


def qr_update_product_stock(product_id, quantity):
    return f"UPDATE product SET stock={quantity} WHERE id={product_id}"