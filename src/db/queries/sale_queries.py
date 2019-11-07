from datetime import date

def qr_check_cart_exists(buyer_id):
    return f"SELECT * FROM sales WHERE (buyer_id='{buyer_id}' and status=1)"

def qr_create_cart(buyer_id, seller_id):
    return f"INSERT INTO sales(buyer_id, seller_id, date, status) \
    VALUES ({buyer_id}, {seller_id}, '{date.today()}', 1);"

def qr_add_to_cart(product_id, quantity, cart_id):
    return f"INSERT INTO sales_has_product(sales_id, product_id, quantity) \
    VALUES ({cart_id}, {product_id}, '{quantity}');"