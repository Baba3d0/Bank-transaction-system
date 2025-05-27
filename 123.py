import datetime
import os
import csv
import uuid
from typing import Dict, List
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, scrolledtext

# Placeholder file path (modify this as needed)
DATA_FILE = "bank_transactions.csv"

# Transaction limit
TRANSFER_LIMIT = 5000.0

# Valid transaction types
TRANSACTION_TYPES = ["UPI", "Bank Transfer", "Net Banking"]

# Initial customer data with unique IDs, name, DOB, address, area, balance, and account type
customers: Dict[str, Dict] = {
    "CUST001": {
        "name": "Charan",
        "dob": "1990-05-15",
        "address": "123 Main St",
        "area": "Downtown",
        "balance": 1000.0,
        "account_type": "Savings",
        "transactions": []
    },
    "CUST002": {
        "name": "Baba",
        "dob": "1985-08-22",
        "address": "456 Oak Ave",
        "area": "Suburb",
        "balance": 1500.0,
        "account_type": "Current",
        "transactions": []
    },
    "CUST003": {
        "name": "Gowrav",
        "dob": "1992-03-10",
        "address": "789 Pine Rd",
        "area": "City Center",
        "balance": 2000.0,
        "account_type": "Savings",
        "transactions": []
    },
    "CUST004": {
        "name": "Rahul",
        "dob": "1988-11-30",
        "address": "101 Elm St",
        "area": "Downtown",
        "balance": 800.0,
        "account_type": "Current",
        "transactions": []
    },
    "CUST005": {
        "name": "Priya",
        "dob": "1995-07-19",
        "address": "202 Maple Dr",
        "area": "Suburb",
        "balance": 1200.0,
        "account_type": "Savings",
        "transactions": []
    },
    "CUST006": {
        "name": "Amit",
        "dob": "1987-04-25",
        "address": "303 Cedar Ln",
        "area": "City Center",
        "balance": 1800.0,
        "account_type": "Current",
        "transactions": []
    },
    "CUST007": {
        "name": "Sneha",
        "dob": "1993-09-12",
        "address": "404 Birch Ave",
        "area": "Downtown",
        "balance": 900.0,
        "account_type": "Savings",
        "transactions": []
    },
    "CUST008": {
        "name": "Vikram",
        "dob": "1986-02-17",
        "address": "505 Spruce St",
        "area": "Suburb",
        "balance": 2500.0,
        "account_type": "Current",
        "transactions": []
    },
    "CUST009": {
        "name": "Anjali",
        "dob": "1991-12-05",
        "address": "606 Willow Rd",
        "area": "City Center",
        "balance": 1100.0,
        "account_type": "Savings",
        "transactions": []
    },
    "CUST010": {
        "name": "Rohan",
        "dob": "1989-06-08",
        "address": "707 Ash Dr",
        "area": "Downtown",
        "balance": 1700.0,
        "account_type": "Current",
        "transactions": []
    },
}

class BankApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bank Transaction System")
        self.root.geometry("1000x700")
       
        # Create notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True)
       
        # Create tabs
        self.create_welcome_tab()
        self.create_register_tab()
        self.create_transfer_tab()
        self.create_summary_tab()
        self.create_history_tab()
       
        # Load data
        self.load_transactions()
       
    def create_welcome_tab(self):
        """Create the welcome tab with basic information"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Welcome")
       
        welcome_label = ttk.Label(tab, text="Bank Transaction System", font=("Arial", 16, "bold"))
        welcome_label.pack(pady=20)
       
        info_text = """Welcome to the Bank Transaction System!

This application allows you to:
- Register new customers
- Process money transfers between accounts
- View customer summaries
- Check transaction histories

Please select the appropriate tab to perform your desired action."""
       
        info_label = ttk.Label(tab, text=info_text, justify=tk.LEFT)
        info_label.pack(pady=10, padx=20)
       
        # Add current time
        time_label = ttk.Label(tab, text="")
        time_label.pack(pady=10)
       
        def update_time():
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            time_label.config(text=f"Current Date & Time: {current_time}")
            self.root.after(1000, update_time)
       
        update_time()
   
    def create_register_tab(self):
        """Create the customer registration tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Register Customer")
       
        # Form fields
        ttk.Label(tab, text="Register New Customer", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
       
        ttk.Label(tab, text="Name:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        self.name_entry = ttk.Entry(tab, width=30)
        self.name_entry.grid(row=1, column=1, padx=5, pady=5)
       
        ttk.Label(tab, text="Account Type:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        self.account_type_var = tk.StringVar()
        self.account_type_combobox = ttk.Combobox(tab, textvariable=self.account_type_var,
                                                values=["Savings", "Current"], state="readonly", width=27)
        self.account_type_combobox.grid(row=2, column=1, padx=5, pady=5)
       
        ttk.Label(tab, text="Date of Birth (YYYY-MM-DD):").grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)
        self.dob_entry = ttk.Entry(tab, width=30)
        self.dob_entry.grid(row=3, column=1, padx=5, pady=5)
       
        ttk.Label(tab, text="Address:").grid(row=4, column=0, padx=5, pady=5, sticky=tk.E)
        self.address_entry = ttk.Entry(tab, width=30)
        self.address_entry.grid(row=4, column=1, padx=5, pady=5)
       
        ttk.Label(tab, text="Area:").grid(row=5, column=0, padx=5, pady=5, sticky=tk.E)
        self.area_entry = ttk.Entry(tab, width=30)
        self.area_entry.grid(row=5, column=1, padx=5, pady=5)
       
        ttk.Label(tab, text="Initial Deposit:").grid(row=6, column=0, padx=5, pady=5, sticky=tk.E)
        self.balance_entry = ttk.Entry(tab, width=30)
        self.balance_entry.grid(row=6, column=1, padx=5, pady=5)
       
        # Register button
        register_btn = ttk.Button(tab, text="Register", command=self.register_customer_gui)
        register_btn.grid(row=7, column=0, columnspan=2, pady=10)
       
        # Status label
        self.register_status = ttk.Label(tab, text="", foreground="green")
        self.register_status.grid(row=8, column=0, columnspan=2)
   
    def create_transfer_tab(self):
        """Create the money transfer tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Process Transfer")
       
        # Form fields
        ttk.Label(tab, text="Process Money Transfer", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
       
        ttk.Label(tab, text="Your Customer ID:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        self.sender_id_entry = ttk.Entry(tab, width=30)
        self.sender_id_entry.grid(row=1, column=1, padx=5, pady=5)
       
        ttk.Label(tab, text="Recipient Customer ID:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        self.recipient_id_entry = ttk.Entry(tab, width=30)
        self.recipient_id_entry.grid(row=2, column=1, padx=5, pady=5)
       
        ttk.Label(tab, text="Amount:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)
        self.amount_entry = ttk.Entry(tab, width=30)
        self.amount_entry.grid(row=3, column=1, padx=5, pady=5)
       
        ttk.Label(tab, text="Transaction Type:").grid(row=4, column=0, padx=5, pady=5, sticky=tk.E)
        self.trans_type_var = tk.StringVar()
        self.trans_type_combobox = ttk.Combobox(tab, textvariable=self.trans_type_var,
                                              values=TRANSACTION_TYPES, state="readonly", width=27)
        self.trans_type_combobox.grid(row=4, column=1, padx=5, pady=5)
       
        # Transfer button
        transfer_btn = ttk.Button(tab, text="Process Transfer", command=self.process_transfer_gui)
        transfer_btn.grid(row=5, column=0, columnspan=2, pady=10)
       
        # Status label
        self.transfer_status = ttk.Label(tab, text="", foreground="green")
        self.transfer_status.grid(row=6, column=0, columnspan=2)
       
        # Balance display
        self.sender_balance_label = ttk.Label(tab, text="")
        self.sender_balance_label.grid(row=7, column=0, columnspan=2)
       
        # Transaction details
        self.transaction_details = scrolledtext.ScrolledText(tab, width=60, height=10, state=tk.DISABLED)
        self.transaction_details.grid(row=8, column=0, columnspan=2, padx=10, pady=10)
   
    def create_summary_tab(self):
        """Create the customer summary tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Customer Summary")
       
        # Title
        ttk.Label(tab, text="Customer Summary", font=("Arial", 12, "bold")).pack(pady=10)
       
        # Treeview for displaying customer data
        self.summary_tree = ttk.Treeview(tab, columns=("ID", "Name", "Account Type", "DOB", "Area", "Balance"), show="headings")
       
        # Define headings
        self.summary_tree.heading("ID", text="Customer ID")
        self.summary_tree.heading("Name", text="Name")
        self.summary_tree.heading("Account Type", text="Account Type")
        self.summary_tree.heading("DOB", text="DOB")
        self.summary_tree.heading("Area", text="Area")
        self.summary_tree.heading("Balance", text="Balance")
       
        # Set column widths
        self.summary_tree.column("ID", width=100)
        self.summary_tree.column("Name", width=150)
        self.summary_tree.column("Account Type", width=100)
        self.summary_tree.column("DOB", width=100)
        self.summary_tree.column("Area", width=150)
        self.summary_tree.column("Balance", width=100)
       
        # Add scrollbar
        scrollbar = ttk.Scrollbar(tab, orient=tk.VERTICAL, command=self.summary_tree.yview)
        self.summary_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.summary_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
       
        # Refresh button
        refresh_btn = ttk.Button(tab, text="Refresh Summary", command=self.display_customer_summary_gui)
        refresh_btn.pack(pady=5)
   
    def create_history_tab(self):
        """Create the transaction history tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Transaction History")
       
        # Form fields
        ttk.Label(tab, text="View Transaction History", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
       
        ttk.Label(tab, text="Customer ID:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        self.history_cust_id_entry = ttk.Entry(tab, width=30)
        self.history_cust_id_entry.grid(row=1, column=1, padx=5, pady=5)
       
        # View button
        view_btn = ttk.Button(tab, text="View History", command=self.display_history_gui)
        view_btn.grid(row=2, column=0, columnspan=2, pady=10)
       
        # Current balance display
        self.current_balance_label = ttk.Label(tab, text="", font=("Arial", 10, "bold"))
        self.current_balance_label.grid(row=3, column=0, columnspan=2)
       
        # Treeview for displaying transaction history
        self.history_tree = ttk.Treeview(tab, columns=("Date", "Type", "Amount", "Balance", "Recipient", "Txn ID", "UTR"), show="headings")
       
        # Define headings
        self.history_tree.heading("Date", text="Date")
        self.history_tree.heading("Type", text="Type")
        self.history_tree.heading("Amount", text="Amount")
        self.history_tree.heading("Balance", text="Balance")
        self.history_tree.heading("Recipient", text="Recipient ID")
        self.history_tree.heading("Txn ID", text="Transaction ID")
        self.history_tree.heading("UTR", text="UTR")
       
        # Set column widths
        self.history_tree.column("Date", width=120)
        self.history_tree.column("Type", width=100)
        self.history_tree.column("Amount", width=80)
        self.history_tree.column("Balance", width=80)
        self.history_tree.column("Recipient", width=100)
        self.history_tree.column("Txn ID", width=100)
        self.history_tree.column("UTR", width=120)
       
        # Add scrollbar
        scrollbar = ttk.Scrollbar(tab, orient=tk.VERTICAL, command=self.history_tree.yview)
        self.history_tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=4, column=2, sticky=tk.NS)
        self.history_tree.grid(row=4, column=0, columnspan=2, sticky=tk.NSEW, padx=5, pady=5)
       
        # Configure grid weights
        tab.grid_rowconfigure(4, weight=1)
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_columnconfigure(1, weight=1)
   
    def save_transactions(self):
        """Save all transactions and customer details to CSV file"""
        try:
            with open(DATA_FILE, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Customer ID", "Name", "Account Type", "DOB", "Address", "Area", "Date", "Type", "Amount", "Balance", "Recipient ID", "Transaction ID", "UTR"])
                for cust_id, info in customers.items():
                    for trans in info["transactions"]:
                        writer.writerow([
                            cust_id,
                            info["name"],
                            info["account_type"],
                            info["dob"],
                            info["address"],
                            info["area"],
                            trans["date"],
                            trans["type"],
                            trans["amount"],
                            trans["balance"],
                            trans.get("recipient_id", ""),
                            trans.get("transaction_id", ""),
                            trans.get("utr", "")
                        ])
                    # Write customer details even if no transactions
                    if not info["transactions"]:
                        writer.writerow([
                            cust_id,
                            info["name"],
                            info["account_type"],
                            info["dob"],
                            info["address"],
                            info["area"],
                            "", "", "", "", "", "", ""
                        ])
            print(f"Transactions and customer details saved to {DATA_FILE}")
        except PermissionError:
            messagebox.showerror("Error", f"No permission to write to {DATA_FILE}. Check file permissions.")
        except Exception as e:
            messagebox.showerror("Error", f"Error saving transactions: {e}")
   
    def load_transactions(self):
        """Load transactions and customer details from CSV file if it exists"""
        if not os.path.exists(DATA_FILE):
            print(f"No transaction file found at {DATA_FILE}. Starting fresh.")
            return
        try:
            with open(DATA_FILE, 'r') as file:
                reader = csv.reader(file)
                header = next(reader, None)  # Skip header
                expected_header = ["Customer ID", "Name", "Account Type", "DOB", "Address", "Area", "Date", "Type", "Amount", "Balance", "Recipient ID", "Transaction ID", "UTR"]
                if header != expected_header:
                    print(f"Invalid CSV header in {DATA_FILE}. Expected {expected_header}, got {header}")
                    return
                for row in reader:
                    if len(row) >= 13 and row[6]:  # Transaction row
                        cust_id = row[0].upper()
                        if cust_id in customers:
                            try:
                                customers[cust_id]["transactions"].append({
                                    "date": row[6],
                                    "type": row[7],
                                    "amount": float(row[8]),
                                    "balance": float(row[9]),
                                    "recipient_id": row[10],
                                    "transaction_id": row[11],
                                    "utr": row[12]
                                })
                                # Update customer details
                                customers[cust_id]["name"] = row[1]
                                customers[cust_id]["account_type"] = row[2]
                                customers[cust_id]["dob"] = row[3]
                                customers[cust_id]["address"] = row[4]
                                customers[cust_id]["area"] = row[5]
                            except ValueError as e:
                                print(f"Skipping invalid transaction row {row}: {e}")
                        else:
                            print(f"Skipping transaction for unknown customer ID: {cust_id}")
                    elif len(row) >= 6:  # Customer details row
                        cust_id = row[0].upper()
                        if cust_id in customers:
                            customers[cust_id]["name"] = row[1]
                            customers[cust_id]["account_type"] = row[2]
                            customers[cust_id]["dob"] = row[3]
                            customers[cust_id]["address"] = row[4]
                            customers[cust_id]["area"] = row[5]
                        else:
                            print(f"Skipping details for unknown customer ID: {cust_id}")
                    else:
                        print(f"Skipping invalid row: {row}")
            print(f"Transactions and customer details loaded from {DATA_FILE}")
        except PermissionError:
            messagebox.showerror("Error", f"No permission to read {DATA_FILE}. Check file permissions.")
        except Exception as e:
            messagebox.showerror("Error", f"Error loading transactions: {e}")
   
    def verify_customer_details(self, cust_id: str, expected_details: Dict) -> bool:
        """Verify customer details against stored data (simulated automatic check)"""
        if cust_id not in customers:
            messagebox.showerror("Error", f"Customer ID {cust_id} not found!")
            return False
        customer = customers[cust_id]
        # Simulate server verification (in a real system, this would query a database)
        if (customer["name"].lower() != expected_details["name"].lower() or
            customer["dob"] != expected_details["dob"] or
            customer["address"].lower() != expected_details["address"].lower() or
            customer["area"].lower() != expected_details["area"].lower()):
            messagebox.showerror("Error", f"Verification failed for Customer ID {cust_id}! Details do not match.")
            return False
        return True
   
    def process_transfer_gui(self):
        """Process a transfer from the GUI"""
        cust_id = self.sender_id_entry.get().strip().upper()
        recipient_id = self.recipient_id_entry.get().strip().upper()
        amount_str = self.amount_entry.get().strip()
        trans_type = self.trans_type_combobox.get().strip()
       
        # Clear previous messages
        self.transfer_status.config(text="")
        self.sender_balance_label.config(text="")
        self.transaction_details.config(state=tk.NORMAL)
        self.transaction_details.delete(1.0, tk.END)
        self.transaction_details.config(state=tk.DISABLED)
       
        # Validate inputs
        if not cust_id or not recipient_id or not amount_str or not trans_type:
            self.transfer_status.config(text="Please fill all fields!", foreground="red")
            return
       
        try:
            amount = float(amount_str)
        except ValueError:
            self.transfer_status.config(text="Invalid amount! Please enter a number.", foreground="red")
            return
       
        if cust_id not in customers:
            self.transfer_status.config(text="Sender ID not found!", foreground="red")
            return
        if recipient_id not in customers:
            self.transfer_status.config(text="Recipient ID not found!", foreground="red")
            return
        if cust_id == recipient_id:
            self.transfer_status.config(text="Cannot transfer to the same account!", foreground="red")
            return
       
        if trans_type not in TRANSACTION_TYPES:
            self.transfer_status.config(text=f"Invalid transaction type! Choose from {TRANSACTION_TYPES}", foreground="red")
            return
       
        if amount <= 0:
            self.transfer_status.config(text="Amount must be positive!", foreground="red")
            return
       
        if amount > TRANSFER_LIMIT:
            self.transfer_status.config(text=f"Amount exceeds limit of ₹{TRANSFER_LIMIT:.2f}!", foreground="red")
            return
       
        if customers[cust_id]["balance"] < amount:
            self.transfer_status.config(text="Insufficient funds!", foreground="red")
            return
       
        # Automatic verification of sender and recipient details
        sender_details = {
            "name": customers[cust_id]["name"],
            "dob": customers[cust_id]["dob"],
            "address": customers[cust_id]["address"],
            "area": customers[cust_id]["area"]
        }
        recipient_details = {
            "name": customers[recipient_id]["name"],
            "dob": customers[recipient_id]["dob"],
            "address": customers[recipient_id]["address"],
            "area": customers[recipient_id]["area"]
        }
       
        if not self.verify_customer_details(cust_id, sender_details):
            return
        if not self.verify_customer_details(recipient_id, recipient_details):
            return
       
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        transaction_id = str(uuid.uuid4())[:8].upper()  # Shortened random Transaction ID
        utr = str(uuid.uuid4())[:12].upper()  # Shortened random UTR
       
        # Display balance before transaction
        self.sender_balance_label.config(
            text=f"Current Balance for {customers[cust_id]['name']}: ₹{customers[cust_id]['balance']:.2f}",
            foreground="blue"
        )
       
        # Process transaction
        customers[cust_id]["balance"] -= amount
        customers[recipient_id]["balance"] += amount
       
        # Record sender's transaction
        customers[cust_id]["transactions"].append({
            "date": current_time,
            "type": f"{trans_type.lower()}_out",
            "amount": amount,
            "balance": customers[cust_id]["balance"],
            "recipient_id": recipient_id,
            "transaction_id": transaction_id,
            "utr": utr
        })
       
        # Record recipient's transaction
        customers[recipient_id]["transactions"].append({
            "date": current_time,
            "type": f"{trans_type.lower()}_in",
            "amount": amount,
            "balance": customers[recipient_id]["balance"],
            "recipient_id": cust_id,
            "transaction_id": transaction_id,
            "utr": utr
        })
       
        self.save_transactions()
       
        # Display transaction details
        details = f"Transaction successful!\n\n"
        details += f"Sender: {customers[cust_id]['name']} (ID: {cust_id}, {customers[cust_id]['account_type']})\n"
        details += f"Recipient: {customers[recipient_id]['name']} (ID: {recipient_id}, {customers[recipient_id]['account_type']})\n"
        details += f"Transaction Type: {trans_type}\n"
        details += f"Amount: ₹{amount:.2f}\n"
        details += f"Date and Time: {current_time}\n"
        details += f"Transaction ID: {transaction_id}\n"
        details += f"UTR: {utr}\n"
        details += f"\nUpdated Balance for {customers[cust_id]['name']}: ₹{customers[cust_id]['balance']:.2f}\n"
        details += f"Updated Balance for {customers[recipient_id]['name']}: ₹{customers[recipient_id]['balance']:.2f}"
       
        self.transaction_details.config(state=tk.NORMAL)
        self.transaction_details.delete(1.0, tk.END)
        self.transaction_details.insert(tk.END, details)
        self.transaction_details.config(state=tk.DISABLED)
       
        self.transfer_status.config(text="Transfer completed successfully!", foreground="green")
   
    def register_customer_gui(self):
        """Register a new customer from the GUI"""
        name = self.name_entry.get().strip().capitalize()
        account_type = self.account_type_var.get()
        dob = self.dob_entry.get().strip()
        address = self.address_entry.get().strip()
        area = self.area_entry.get().strip()
        balance_str = self.balance_entry.get().strip()
       
        # Clear previous status
        self.register_status.config(text="")
       
        # Validate inputs
        if not name or not account_type or not dob or not address or not area or not balance_str:
            self.register_status.config(text="Please fill all fields!", foreground="red")
            return
       
        # Check if customer with this name already exists
        for cust_id, info in customers.items():
            if info["name"].lower() == name.lower():
                self.register_status.config(text="Customer with this name already exists!", foreground="red")
                return
       
        try:
            initial_balance = float(balance_str)
            if initial_balance < 0:
                self.register_status.config(text="Initial balance cannot be negative!", foreground="red")
                return
        except ValueError:
            self.register_status.config(text="Invalid amount! Please enter a number.", foreground="red")
            return
       
        # Generate unique customer ID
        cust_id = f"CUST{len(customers) + 1:03d}"
       
        customers[cust_id] = {
            "name": name,
            "dob": dob,
            "address": address,
            "area": area,
            "balance": initial_balance,
            "account_type": account_type,
            "transactions": []
        }
       
        self.save_transactions()
       
        # Clear form
        self.name_entry.delete(0, tk.END)
        self.account_type_combobox.set('')
        self.dob_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)
        self.area_entry.delete(0, tk.END)
        self.balance_entry.delete(0, tk.END)
       
        # Show success message
        message = f"Account created successfully for {name} ({account_type})!\nCustomer ID: {cust_id}\nCurrent Balance: ₹{initial_balance:.2f}"
        self.register_status.config(text=message, foreground="green")
       
        # Update summary tab
        self.display_customer_summary_gui()
   
    def display_customer_summary_gui(self):
        """Display customer summary in the GUI"""
        # Clear existing data
        for item in self.summary_tree.get_children():
            self.summary_tree.delete(item)
       
        # Add customer data to treeview
        for cust_id, info in customers.items():
            self.summary_tree.insert("", tk.END, values=(
                cust_id,
                info["name"],
                info["account_type"],
                info["dob"],
                info["area"],
                f"₹{info['balance']:.2f}"
            ))
   
    def display_history_gui(self):
        """Display transaction history in the GUI"""
        cust_id = self.history_cust_id_entry.get().strip().upper()
       
        # Clear existing data
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        self.current_balance_label.config(text="")
       
        if not cust_id:
            messagebox.showerror("Error", "Please enter a Customer ID")
            return
       
        if cust_id not in customers:
            messagebox.showerror("Error", "Customer ID not found!")
            return
       
        customer = customers[cust_id]
       
        # Display current balance
        self.current_balance_label.config(
            text=f"Current Balance for {customer['name']} (ID: {cust_id}, {customer['account_type']}): ₹{customer['balance']:.2f}",
            foreground="blue"
        )
       
        if not customer["transactions"]:
            self.history_tree.insert("", tk.END, values=("No transactions found", "", "", "", "", "", ""))
            return
       
        # Add transactions to treeview
        for trans in customer["transactions"]:
            recipient_id = trans.get("recipient_id", "")
            trans_type = trans["type"].replace("_", " ").title()
            transaction_id = trans.get("transaction_id", "")
            utr = trans.get("utr", "")
           
            self.history_tree.insert("", tk.END, values=(
                trans["date"],
                trans_type,
                f"₹{trans['amount']:.2f}",
                f"₹{trans['balance']:.2f}",
                recipient_id,
                transaction_id,
                utr
            ))

def main():
    """Main function to run the application"""
    root = tk.Tk()
    app = BankApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
