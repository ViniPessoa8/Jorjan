def qr_register_category(name):
    return "INSERT INTO Jorjan.category(`name`) VALUES (\""+name+"\");"

def qr_get_category_by_id(id):
    return f"SELECT * FROM Jorjan.category WHERE id = {id};"

def qr_get_category_by_name(name):
    return f"SELECT * FROM Jorjan.category WHERE name = \"{name}\";"
    
def qr_get_categories():
    return "SELECT * FROM Jorjan.category;"

def qr_remove_category_by_id(id):
    return f"DELETE FROM Jorjan.category WHERE id = "{id}";"
