import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog, messagebox
import mysql.connector
import datetime

class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("E-Commerce System")

        # Connect to the MySQL database
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Ahmed113",
            database="e-commerce"
        )
        self.cursor = self.connection.cursor()

        self.create_gui()

    def create_gui(self):
        # Create and set up the notebook
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True)

        # Create tabs for each table
        tables = ["CustomerAccount", "Orders", "Orderline", "Product", "StoredProduct", "Vendor", "Warehouse", "Staff", "PhoneNumber"]
        for table in tables:
            tab = ttk.Frame(self.notebook)
            self.notebook.add(tab, text=table)
            self.create_table_frame(tab, table)

        # Search entry
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(self.root, textvariable=self.search_var)
        search_entry.pack(pady=5)
        search_button = ttk.Button(self.root, text="Search", command=self.search_entries)
        search_button.pack(pady=5)

    def create_table_frame(self, parent, table_name):
        # Fetch column names from the table
        columns = self.get_columns(table_name)

        # Create a treeview to display data
        tree = ttk.Treeview(parent, columns=columns, show='headings')
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        tree.pack(side="right", anchor="e", pady=5)
        
        # Add buttons for data operations
        add_button = ttk.Button(parent, text="Add", command=lambda: self.add_data(table_name, tree))
        add_button.pack(side="top", anchor="w", pady=(230,5),padx=25)

        edit_button = ttk.Button(parent, text="Edit", command=lambda: self.edit_data(table_name, tree))
        edit_button.pack(side="top", anchor="w", pady=5,padx=25)

        remove_button = ttk.Button(parent, text="Remove", command=lambda: self.remove_data(table_name, tree))
        remove_button.pack(side="top", anchor="w", pady=5,padx=25)

        tree.pack(fill='both', expand=True)

        # Initial data fetch
        self.refresh_data(table_name, tree)

    def get_columns(self, table_name):
        # Fetch column names from the table
        self.cursor.execute(f"DESC {table_name}")
        columns = [col[0] for col in self.cursor.fetchall()]
        return columns

    def is_not_null_constraint(self, table_name, column_name):
        # Query the information schema to get constraint information
        query = """
            SELECT COLUMN_NAME
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_NAME = %s AND COLUMN_NAME = %s AND IS_NULLABLE = 'NO'
        """
        self.cursor.execute(query, (table_name, column_name))
        
        # Check if the column has a NOT NULL constraint
        return bool(self.cursor.fetchone())
    
    def phone_number_exists(self, PhoneNumber, table_name):
        # Check if the phone number already exists in the database
        query = f"SELECT COUNT(*) FROM {table_name} WHERE PhoneNumber = %s"
        self.cursor.execute(query, (PhoneNumber,))
        count = self.cursor.fetchone()[0]
        return count > 0

    def add_data(self, table_name, tree):
        # Get column names
        columns = self.get_columns(table_name)
        # Get values from the user
        values = []
        for col in columns:
            try:
                # Skip the first column if it isn't phonenumber
                if col!="PhoneNumber" and col==columns[0]:
                    continue
                if self.is_not_null_constraint(table_name, col):
                    value = simpledialog.askstring("Input", f"Enter value for {col}:", parent=self.root)
                else:
                    value = simpledialog.askstring("Input", f"Enter value for {col} (or press Enter for NULL):", parent=self.root)

                # Check if the user pressed Cancel
                if value is None:
                    return

                if not value:
                    if self.is_not_null_constraint(table_name, col):
                        raise ValueError(f"Invalid input for {col}. Please enter a non-null value.")
                    else:
                        value = None  # Use None for NULL values
                elif col.endswith("Date") or col.endswith("date"):  # Assuming these are date columns
                    # Use datetime to validate and format the date
                    try:
                        value = datetime.datetime.strptime(value, "%Y-%m-%d").date()
                    except ValueError:
                        raise ValueError(f"Invalid date format for {col}. Please enter a valid date (YYYY-MM-DD).")
                elif col==("Gender"):
                    if value.lower() not in ["male", "female"]:
                        raise ValueError(f"Invalid format for {col}. Please enter a valid gender (Male/Female).")
                elif col == "PhoneNumber":
                    # Check if the phone number already exists in the database
                    if self.phone_number_exists(value, table_name,value):
                        raise ValueError("Phone number already exists in the database.")
                else:
                    # Attempt to convert the value to the correct datatype
                    if col.endswith("Qty"):  # Assuming this is a numeric column
                        value = int(value)
                    elif col=="Price":
                        value = float(value)
                    else:
                        value = str(value)
                values.append(value)
            except (ValueError, mysql.connector.errors.DataError, mysql.connector.errors.IntegrityError) as e:
                tk.messagebox.showerror("Error", str(e))
                return
        # Convert None to NULL for database insertion
        values = [None if value is None else value for value in values]
        # Insert data into the database
        columns_str = ", ".join([col for col in columns if not(col!="PhoneNumber" and col==columns[0])])
        values_str = ", ".join(["%s" for _ in range(len(values))])
        query = f"INSERT INTO {table_name} ({columns_str}) VALUES ({values_str})"
        try:
            self.cursor.execute(query, values)
            self.connection.commit()
        except (mysql.connector.errors.IntegrityError) as e:
            tk.messagebox.showerror("Error", "Can't add a non-existent value as a foreign key.")
        except Exception:
            tk.messagebox.showerror("Error", "Incorrect or incompatible data was input.")
        
        # Refresh the treeview
        self.refresh_data(table_name, tree)

    def edit_data(self, table_name, tree):
        # Get selected item from the treeview
        selected_item = tree.selection()
        if not selected_item:
            return

        # Get column names
        columns = self.get_columns(table_name)

        # Get current values
        current_values = tree.item(selected_item)["values"]

        # Get new values from the user
        new_values = []
        for col in columns:
            try:
                # Skips the first column if it isn't phonenumber
                if col!="PhoneNumber" and col==columns[0]:
                    continue
                if self.is_not_null_constraint(table_name, col):
                    x=current_values[columns.index(col)]
                    if x == None or x=="None":
                        x =  ""
                    value = simpledialog.askstring("Input", f"Enter value for {col}:", initialvalue=x,parent=self.root)
                else:
                    x=current_values[columns.index(col)]
                    if x == None or x=="None":
                        x =  ""
                    value = simpledialog.askstring("Input", f"Enter value for {col} (or press Enter for NULL):", initialvalue=x,parent=self.root)
                
                # Check if the user pressed Cancel
                if value is None:
                    return
                
                if not value:
                    if self.is_not_null_constraint(table_name, col):
                        raise ValueError(f"Invalid input for {col}. Please enter a non-null value.")
                    else:
                        value = None  # Use None for NULL values
                elif col.endswith("Date") or col.endswith("date"):  # Assuming these are date columns
                    # Use datetime to validate and format the date
                    try:
                        value = datetime.datetime.strptime(value, "%Y-%m-%d").date()
                    except ValueError:
                        raise ValueError(f"Invalid date format for {col}. Please enter a valid date (YYYY-MM-DD).")
                elif col==("Gender"):
                    if value.lower() not in ["male", "female"]:
                        raise ValueError(f"Invalid format for {col}. Please enter a valid gender (Male/Female).")
                elif col == "PhoneNumber" and str(value) != str(current_values[columns.index(col)]):
                    # Check if the phone number already exists in the database
                    if self.phone_number_exists(value, table_name):
                        raise ValueError("Phone number already exists in the database.")
                else:
                    # Attempt to convert the value to the correct datatype
                    if col.endswith("Qty"):  # Assuming this is a numeric column
                        value = int(value)
                    elif col=="Price":
                        value = float(value)
                    else:
                        value = str(value)
                new_values.append(value)
            except (ValueError, mysql.connector.errors.DataError,mysql.connector.errors.IntegrityError) as e:
                tk.messagebox.showerror("Error", str(e))
                return

        # Update the record in the target table
        set_clause = ", ".join([f"{col} = %s" for col in columns if not(col!="PhoneNumber" and col==columns[0])])
        query = f"UPDATE {table_name} SET {set_clause} WHERE {columns[0]} = %s"
        try:
            self.cursor.execute(query, new_values + [current_values[0]])
            self.connection.commit()
        except (mysql.connector.errors.IntegrityError) as e:
            tk.messagebox.showerror("Error","Can't add a non-existant value as a foreign key.")
        except Exception:
            tk.messagebox.showerror("Error", "Incorrect or incompatible data was input.")

        # Refresh the treeview
        self.refresh_data(table_name, tree)

    def remove_data(self, table_name, tree):
        # Get selected item from the treeview
        selected_item = tree.selection()
        if not selected_item:
            return

        # Get column names
        columns = self.get_columns(table_name)

        # Get current values
        current_values = tree.item(selected_item)["values"]

        try:
            # Delete the record from the target table
            query = f"DELETE FROM {table_name} WHERE {columns[0]} = %s"
            self.cursor.execute(query, [current_values[0]])
            self.connection.commit()

            # Refresh the treeview
            self.refresh_data(table_name, tree)
        except mysql.connector.Error as err:
            tk.messagebox.showerror("Error", "This record has entries in another table in the database, please remove them first and then you can remove this record.")

    def refresh_data(self, table_name, tree):
        # Fetch data from the table and populate the treeview
        self.cursor.execute(f"SELECT * FROM {table_name}")
        data = self.cursor.fetchall()

        # Clear previous data
        for item in tree.get_children():
            tree.delete(item)

        # Insert new data
        for row in data:
            tree.insert("", "end", values=row)

    def search_entries(self):
        # Search for entries in the first column of the treeview based on the search term
        search_term = self.search_var.get().lower()
        if len(search_term) == 0:
            tk.messagebox.showinfo("Error", "The search term is empty.")
        else:
            for tab in self.notebook.tabs():
                tree = self.notebook.nametowidget(tab).winfo_children()[0]
                for item in tree.get_children():
                    # Retrieve the value of the first column
                    first_column_value = tree.item(item, "values")[0]
                    if search_term == str(first_column_value).lower():
                        tree.selection_set(item)
                        tree.focus(item)
                        
if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()