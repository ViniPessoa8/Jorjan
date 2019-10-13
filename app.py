from src.db.user import get_all_users, register_new_user, check_login

if __name__ == "__main__":
    print(check_login(email='vini.pessoa7@gmail.com', ps='senha'))
    register_new_user(name='Jansen', ps='Abacate1234', email='jansenalcantara@gmail.com')
    get_all_users()
  