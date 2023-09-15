import sqlite3
conn = sqlite3.connect('atm.db')
cursor = conn.cursor()

# here we are create the accounts table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS accounts (
        account_number TEXT PRIMARY KEY,
        pin TEXT,
        balance REAL
    )
''')

# some of the Sample account data
cursor.execute("INSERT OR IGNORE INTO accounts VALUES ('123456', '1234', 1000.0)")
cursor.execute("INSERT OR IGNORE INTO accounts VALUES ('789012', '5678', 500.0)")

conn.commit()
def check_balance(account_number):
    cursor.execute("SELECT balance FROM accounts WHERE account_number=?", (account_number,))
    result = cursor.fetchone()
    if result:
        return result[0]
    return None

def deposit(account_number, amount):
    cursor.execute("UPDATE accounts SET balance = balance + ? WHERE account_number=?", (amount, account_number))
    conn.commit()
    return True

def withdraw(account_number, amount):
    current_balance = check_balance(account_number)
    if current_balance is not None and current_balance >= amount:
        cursor.execute("UPDATE accounts SET balance = balance - ? WHERE account_number=?", (amount, account_number))
        conn.commit()
        return True
    return False

def change_pin(account_number, new_pin):
    cursor.execute("UPDATE accounts SET pin = ? WHERE account_number=?", (new_pin, account_number))
    conn.commit()
    return True
while True:
    print("Welcome to the ATM")
    account_number = input("Enter your account number: ")
    pin = input("Enter your PIN: ")

    cursor.execute("SELECT * FROM accounts WHERE account_number=? AND pin=?", (account_number, pin))
    account_data = cursor.fetchone()

    if account_data:
        while True:
            print("\n1. Check Balance\n2. Deposit\n3. Withdraw\n4. Change PIN\n5. Exit")
            choice = input("Select an option: ")

            if choice == '1':
                print("Your balance is:", check_balance(account_number))
            elif choice == '2':
                amount = float(input("Enter the deposit amount: "))
                if deposit(account_number, amount):
                    print("Deposit successful.")
                else:
                    print("Insufficient balance.")
            elif choice == '3':
                amount = float(input("Enter the withdrawal amount: "))
                if withdraw(account_number, amount):
                    print("Withdrawal successful.")
                else:
                    print("Insufficient balance.")
            elif choice == '4':
                new_pin = input("Enter your new PIN: ")
                change_pin(account_number, new_pin)
                print("PIN changed successfully.")
            elif choice == '5':
                break
            else:
                print("Invalid choice. Please select again.")
    else:
        print("Invalid account number or PIN. Please try again.")