from storage import save_data
from utils import now_text, hash_password, check_password

HARD_LIMIT = 6        # 6 sehv -> kart bloklanir


def password_is_strong(password):
    if len(password) < 8:
        return False
    has_upper = False
    has_lower = False
    has_digit = False
    for ch in password:
        if ch.isupper():
            has_upper = True
        elif ch.islower():
            has_lower = True
        elif ch.isdigit():
            has_digit = True
    return has_upper and has_lower and has_digit


def wrong_password(user):
    user["failed_attempts"] = user["failed_attempts"] + 1
    count = user["failed_attempts"]
    print("Incorrect password. Attempt: " + str(count) + "/" + str(HARD_LIMIT))

    if count >= HARD_LIMIT:
        user["blocked"] = True
        print("Maximum login attempts exceeded.")
        print("Your card has been blocked.")
        print("Please contact the bank administrator.")


def login(data):
    while True:
        username = input("Username (0 to exit): ").strip()
        if username == "0":
            return None

        if username not in data["users"]:
            print("Invalid username or password.")
            continue

        user = data["users"][username]

        if user["blocked"]:
            print("Your card has been blocked.")
            print("Please contact the bank administrator.")
            continue

        password = input("Password: ")
        if check_password(password, user["password_hash"]):
            user["failed_attempts"] = 0        # ugurlu giris sayaci sifirlayir
            user["last_login"] = now_text()
            save_data(data)
            return username
