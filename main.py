import sqlite3
import random

# Connect to database
conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

# Create tables (custom account_number)
cursor.execute('''
CREATE TABLE accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_number TEXT UNIQUE,
    name TEXT NOT NULL,
    password TEXT NOT NULL,
    balance REAL DEFAULT 0.0
)
''')

cursor.execute('''
CREATE TABLE transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_number TEXT,
    type TEXT,
    amount REAL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

conn.commit()

# --- Utility Functions ---

def generate_account_number():
    while True:
        acc_num = str(random.randint(10000000, 99999999))
        cursor.execute("SELECT 1 FROM accounts WHERE account_number = ?", (acc_num,))
        if not cursor.fetchone():
            return acc_num

def verify_login(account_number, password):
    cursor.execute(
        "SELECT password FROM accounts WHERE account_number = ?",
        (account_number,)
    )
    result = cursor.fetchone()
    return result and result[0] == password

def get_balance(account_number):
    cursor.execute(
        "SELECT balance FROM accounts WHERE account_number = ?",
        (account_number,)
    )
    result = cursor.fetchone()
    return result[0] if result else None


# --- Core Functions ---

def create_account(name, password, initial_deposit):
    acc_num = generate_account_number()

    cursor.execute(
        "INSERT INTO accounts (account_number, name, password, balance) VALUES (?, ?, ?, ?)",
        (acc_num, name, password, initial_deposit)
    )

    if initial_deposit > 0:
        cursor.execute(
            "INSERT INTO transactions (account_number, type, amount) VALUES (?, 'deposit', ?)",
            (acc_num, initial_deposit)
        )

    conn.commit()

    print(f"\nAccount created")
    print(f"Your Account Number: {acc_num}")


def deposit(account_number, amount):
    if amount <= 0:
        print("Deposit must be positive.")
        return

    cursor.execute(
        "UPDATE accounts SET balance = balance + ? WHERE account_number = ?",
        (amount, account_number)
    )

    cursor.execute(
        "INSERT INTO transactions (account_number, type, amount) VALUES (?, 'deposit', ?)",
        (account_number, amount)
    )

    conn.commit()
    print(f"Deposited ${amount:.2f}")


def withdraw(account_number, amount):
    balance = get_balance(account_number)

    if balance is None:
        print("Account not found.")
        return

    if amount <= 0:
        print("Withdrawal must be positive.")
        return

    if amount > balance:
        print("Insufficient funds.")
        return

    cursor.execute(
        "UPDATE accounts SET balance = balance - ? WHERE account_number = ?",
        (amount, account_number)
    )

    cursor.execute(
        "INSERT INTO transactions (account_number, type, amount) VALUES (?, 'withdrawal', ?)",
        (account_number, amount)
    )

    conn.commit()
    print(f"Withdrew ${amount:.2f}")


def list_accounts():
    cursor.execute("SELECT account_number, name, balance FROM accounts")
    accounts = cursor.fetchall()

    print("\n--- Accounts ---")
    for acc in accounts:
        print(f"Acc#: {acc[0]} | Name: {acc[1]} | Balance: ${acc[2]:.2f}")


# --- Menu System (Session-Based) ---

def menu():
    current_user = None

    while True:
        if current_user is None:
            print("\n" + "="*35)
            print("         BANKING APP")
            print("="*35)
            print("1. Login")
            print("2. Create Account")
            print("3. List Accounts")
            print("4. Exit")
            print("="*35)

            choice = input("\nEnter your choice:\n> ").strip()

            if choice == "1":
                print("\n--- Login ---")
                acc_num = input("Account Number:\n> ")
                password = input("Password:\n> ")

                if verify_login(acc_num, password):
                    current_user = acc_num
                    print("\nLogin successful!")
                else:
                    print("\nInvalid credentials.")

            elif choice == "2":
                print("\n--- Create Account ---")
                name = input("Name:\n> ")
                password = input("Password:\n> ")
                deposit_amt = float(input("Initial Deposit:\n> "))
                create_account(name, password, deposit_amt)
                
            elif choice == "3":
                
                list_accounts()

            elif choice == "4":
                print("\nGoodbye!\n")
                break

            else:
                print("\nInvalid choice.")

        else:
            print("\n" + "="*35)
            print(f"   Logged in (Acc#: {current_user})")
            print("="*35)
            print("1. Deposit")
            print("2. Withdraw")
            print("3. Check Balance")
            print("4. Logout")
            print("5. Exit")
            print("="*35)

            choice = input("\nEnter your choice:\n> ").strip()

            try:
                if choice == "1":
                    print("\n--- Deposit ---")
                    amt = float(input("Amount:\n> "))
                    deposit(current_user, amt)

                elif choice == "2":
                    print("\n--- Withdraw ---")
                    amt = float(input("Amount:\n> "))
                    withdraw(current_user, amt)

                elif choice == "3":
                    print("\n--- Balance ---")
                    balance = get_balance(current_user)
                    print(f"Balance: ${balance:.2f}")

                elif choice == "4":
                    current_user = None
                    print("\nLogged out.")

                elif choice == "5":
                    print("\nGoodbye!\n")
                    break

                else:
                    print("\nInvalid choice.")

            except ValueError:
                print("\nInvalid input.")


# Run app
menu()