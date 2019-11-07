def qr_create_category(name):
    return "INSERT INTO Jorjan.category(`name`) VALUES ("+name+");"

def qr_get_category_by_id(name):
    return "SELECT `name` FROM Jorjan.category WHERE id = "+id+";"

def qr_get_category_by_name(name):
    return "SELECT `name` FROM Jorjan.category WHERE id = "+id+";"
    
def qr_get_categories():
    return "SELECT * FROM Jorjan.category;"

def qr_remove_category(id):
    return "DELETE FROM Jorjan.category WHERE id = "+id+";"
