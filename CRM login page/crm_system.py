
import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect("crm.db")
cursor = conn.cursor()

# Create customers table
cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    phone TEXT,
    address TEXT
)
""")
conn.commit()

# Function to add a new customer
def add_customer():
    name = input("Enter customer name: ")
    email = input("Enter customer email: ")
    phone = input("Enter customer phone: ")
    address = input("Enter customer address: ")

    try:
        cursor.execute("INSERT INTO customers (name, email, phone, address) VALUES (?, ?, ?, ?)",
                       (name, email, phone, address))
        conn.commit()
        print("Customer added successfully!")
    except sqlite3.IntegrityError:
        print("Error: Email already exists!")

# Function to view all customers
def view_customers():
    cursor.execute("SELECT * FROM customers")
    rows = cursor.fetchall()
    if rows:
        for row in rows:
            print(f"\nID: {row[0]}\nName: {row[1]}\nEmail: {row[2]}\nPhone: {row[3]}\nAddress: {row[4]}")
    else:
        print("No customers found.")

# Function to update a customer
def update_customer():
    id = input("Enter customer ID to update: ")
    cursor.execute("SELECT * FROM customers WHERE id=?", (id,))
    result = cursor.fetchone()
    if result:
        name = input("Enter new name (leave blank to keep current): ") or result[1]
        email = input("Enter new email (leave blank to keep current): ") or result[2]
        phone = input("Enter new phone (leave blank to keep current): ") or result[3]
        address = input("Enter new address (leave blank to keep current): ") or result[4]

        cursor.execute("UPDATE customers SET name=?, email=?, phone=?, address=? WHERE id=?",
                       (name, email, phone, address, id))
        conn.commit()
        print("Customer updated successfully!")
    else:
        print("Customer not found.")

# Function to delete a customer
def delete_customer():
    id = input("Enter customer ID to delete: ")
    cursor.execute("DELETE FROM customers WHERE id=?", (id,))
    conn.commit()
    if cursor.rowcount:
        print("Customer deleted successfully!")
    else:
        print("Customer not found.")

# Function to search for a customer
def search_customer():
    keyword = input("Enter name or email to search: ")
    cursor.execute("SELECT * FROM customers WHERE name LIKE ? OR email LIKE ?", 
                   (f"%{keyword}%", f"%{keyword}%"))
    rows = cursor.fetchall()
    if rows:
        for row in rows:
            print(f"\nID: {row[0]}\nName: {row[1]}\nEmail: {row[2]}\nPhone: {row[3]}\nAddress: {row[4]}")
    else:
        print("No matching customers found.")

# Menu
def menu():
    while True:
        print("\n--- Customer Relationship Management (CRM) System ---")
        print("1. Add Customer")
        print("2. View All Customers")
        print("3. Update Customer")
        print("4. Delete Customer")
        print("5. Search Customer")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ")

        if choice == '1':
            add_customer()
        elif choice == '2':
            view_customers()
        elif choice == '3':
            update_customer()
        elif choice == '4':
            delete_customer()
        elif choice == '5':
            search_customer()
        elif choice == '6':
            print("Exiting CRM System.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")

if __name__ == "__main__":
    menu()
    conn.close()
