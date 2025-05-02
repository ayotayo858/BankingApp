import sqlite3 # Import the sqlite3 module for database operations

def init_db(): # Define a function to initialize the database and create the users table if it doesn't exist
    conn = sqlite3.connect('bank.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY, name TEXT, balance REAL, pin TEXT)''')
    conn.commit()
    conn.close() # Close the connection after creating the table

def menu(username): # Define a function to display the menu and handle user choices
    conn = sqlite3.connect('bank.db')
    c = conn.cursor()
    c.execute("SELECT name, balance FROM users WHERE username = ?", (username,))
    user_data = c.fetchone() # Fetch the user data from the database
    
    menuchoice = int(input(f"Hello {user_data[0]}! What would you like to do?\n1. Check balance\n2. Withdraw\n3. Deposit\n4. Logout\n5. Delete Account\n6. Change Pin\n"))
    if menuchoice == 1:
        print(f"Your balance is {user_data[1]}")
        conn.close()
        menu(username)
    elif menuchoice == 2:
        amount = float(input("Enter amount to withdraw: "))
        if amount <= user_data[1]:
            new_balance = user_data[1] - amount
            c.execute("UPDATE users SET balance = ? WHERE username = ?", (new_balance, username))
            conn.commit()
            print(f"Withdrawal successful. New balance: {new_balance}")
        else:
            print("Insufficient funds")
        conn.close()
        menu(username)
    elif menuchoice == 3:
        amount = float(input("Enter amount to deposit: "))
        new_balance = user_data[1] + amount
        c.execute("UPDATE users SET balance = ? WHERE username = ?", (new_balance, username))
        conn.commit()
        print(f"Deposit successful. New balance: {new_balance}")
        conn.close()
        menu(username)
    elif menuchoice == 4:
        print("You've been successfully logged out!")
        conn.close()
        return
    elif menuchoice == 5:
        confirm = input("Are you sure you want to delete your account? (y/n)")
        if confirm.lower() == "y":
            c.execute("DELETE FROM users WHERE username = ?", (username,))
            conn.commit()
            print("Account deleted successfully")
            conn.close()
            hi()
            return
        else:
            conn.close()
            menu(username)
    elif menuchoice == 6:
        c.execute("SELECT pin FROM users WHERE username = ?", (username,))
        current_pin = c.fetchone()[0]
        pin = input("Enter your new PIN: ")
        confirm_pin = input("Confirm your new PIN: ")
        while pin == current_pin:
            print("New PIN cannot be the same as the old PIN. Please try again.")
            pin = input("Enter your new PIN: ")
            confirm_pin = input("Confirm your new PIN: ")
        while len(pin) != 4:
            print("PIN must be 4 digits. Please try again.")
            pin = input("Enter your new PIN: ")
            confirm_pin = input("Confirm your new PIN: ")
        while pin != confirm_pin:
            print("PINs do not match. Please try again.")
            pin = input("Enter your new PIN: ")
            confirm_pin = input("Confirm your new PIN: ")
        c.execute("UPDATE users SET pin = ? WHERE username = ?", (pin, username))
        conn.commit()
        print("PIN changed successfully")
        conn.close()
        menu(username)
    else:
        print("Invalid choice")
        conn.close()
        menu(username)

def login(): # Define a function to handle user login
    conn = sqlite3.connect('bank.db')
    c = conn.cursor()
    incorrect_count = 0
    username = input("Enter your username: ")
    c.execute("SELECT COUNT(*) FROM users WHERE username = ?", (username,))
    while c.fetchone()[0] == 0:
        print("Invalid username. Please try again.")
        username = input("Enter your username: ")
        c.execute("SELECT COUNT(*) FROM users WHERE username = ?", (username,))
    
    while True:
        pin = input("Enter your PIN: ")
        c.execute("SELECT pin FROM users WHERE username = ?", (username,))
        correct_pin = c.fetchone()[0]
        if pin == correct_pin:
            print("Login successful!")
            conn.close()
            menu(username)
            break
        else:
            incorrect_count += 1
            print("Invalid PIN. Please try again.")
            if incorrect_count >= 3:
                print("Too many incorrect attempts. Exiting.")
                break
    conn.close()

def signup(): # Define a function to handle user signup
    conn = sqlite3.connect('bank.db')
    c = conn.cursor()
    username = input("Enter your username: ")
    c.execute("SELECT COUNT(*) FROM users WHERE username = ?", (username,))
    while c.fetchone()[0] > 0:
        print("Username already exists. Please choose another one.")
        username = input("Enter your username: ")
        c.execute("SELECT COUNT(*) FROM users WHERE username = ?", (username,))
    
    name = input("Enter your name: ")
    pin = input("Enter your PIN: ")
    confirm_pin = input("Confirm your PIN: ")
    while pin != confirm_pin:
        print("PINs do not match. Please try again.")
        pin = input("Enter your PIN: ")
        confirm_pin = input("Confirm your PIN: ")
    
    c.execute("INSERT INTO users (username, name, balance, pin) VALUES (?, ?, ?, ?)",
              (username, name, 0.0, pin))
    conn.commit()
    conn.close()
    print("Signup successful!")
    login()

def hi(): # Define a function to display the welcome message and handle user choices
    init_db()
    user_choice = int(input("Welcome to the bank! What would you like to do?\n1. Login\n2. Signup\n"))
    if user_choice == 1:
        login()
    elif user_choice == 2:
        signup()
    else:
        print("Invalid choice. Exiting.")

if __name__ == "__main__":
    hi()
