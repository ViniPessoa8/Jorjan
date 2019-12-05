def qr_register_category(name):
    return f"INSERT INTO Jorjan.category(`name`) VALUES ('{name}');"

def qr_get_category_by_id(id):
    return f"SELECT * FROM Jorjan.category WHERE id = {id};"

def qr_get_category_by_name(name):
    return f"SELECT * FROM Jorjan.category WHERE name = '{name}';"
    
def qr_get_categories():
    return f"SELECT * FROM Jorjan.category;"

def qr_get_categories_seller_id(seller_id):
    return f"SELECT * from Jorjan.category c WHERE c.id = Jorjan.`user`.id AND Jorjan.`user`.id = '{seller_id}';"

def qr_remove_category_by_id(id):
    return f"DELETE FROM Jorjan.category WHERE id = '{id}';"
