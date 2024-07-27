import tkinter as tk
from tkinter import ttk, filedialog
import pandas as pd
import mysql.connector
from datetime import datetime
import re
from tkinter import Tk, ttk, StringVar, messagebox
from ttkthemes import ThemedStyle
class DBMSApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("DBMS")
        self.configure(bg="#e0e0e0")
        self.geometry("800x650")
        self.style = ThemedStyle(self)
        self.style.theme_use('breeze')
        style = ttk.Style(self)
        style.configure('TFrame', background="#ffffff", relief="solid", borderwidth=1)
        style.configure('TButton', background="#4caf50", foreground="black", font=('Arial', 12, 'bold'), relief="flat")
        style.map('TButton', background=[('active', '#45a049')])
        style.configure('TLabel', background="#ffffff", font=('Arial', 14, 'bold'))

        self.current_window = None

        # Raw Section
        raw_frame = ttk.Frame(self, padding=(10, 10, 10, 10))
        raw_frame.pack(fill='x', padx=20, pady=10)
        raw_label = ttk.Label(raw_frame, text="RAW")
        raw_label.grid(row=0, column=0, columnspan=3, pady=10)
        button1 = ttk.Button(raw_frame, text="Checker 1", command=lambda: self.open_new_window("RAW", "Checker 1", self.custom_function1))
        button1.grid(row=1, column=0, sticky='ew', padx=5, pady=5)
        button2 = ttk.Button(raw_frame, text="Checker 2", command=lambda: self.open_new_window("RAW", "Checker 2", self.custom_function2))
        button2.grid(row=1, column=1, sticky='ew', padx=5, pady=5)
        button3 = ttk.Button(raw_frame, text="Checker 3", command=lambda: self.open_new_window("RAW", "Checker 3", self.custom_function3))
        button3.grid(row=1, column=2, sticky='ew', padx=5, pady=5)
        raw_frame.columnconfigure(0, weight=1)
        raw_frame.columnconfigure(1, weight=1)
        raw_frame.columnconfigure(2, weight=1)

        # Checked Section
        checked_frame = ttk.Frame(self, padding=(10, 10, 10, 10))
        checked_frame.pack(fill='x', padx=20, pady=10)
        checked_label = ttk.Label(checked_frame, text="CHECKED")
        checked_label.grid(row=0, column=0, columnspan=2, pady=10)
        button1_checked = ttk.Button(checked_frame, text="Checker 1", command=lambda: self.open_new_window("CHECKED", "Checker 1", self.custom_function4))
        button1_checked.grid(row=1, column=0, sticky='ew', padx=5, pady=5)
        button2_checked = ttk.Button(checked_frame, text="Checker 2", command=lambda: self.open_new_window("CHECKED", "Checker 2", self.custom_function5))
        button2_checked.grid(row=1, column=1, sticky='ew', padx=5, pady=5)
        checked_frame.columnconfigure(0, weight=1)
        checked_frame.columnconfigure(1, weight=1)

        # Complete Section
        complete_frame = ttk.Frame(self, padding=(10, 10, 10, 10))
        complete_frame.pack(fill='x', padx=20, pady=10)
        complete_label = ttk.Label(complete_frame, text="COMPLETE")
        complete_label.pack(pady=10)
        complete_button = ttk.Button(complete_frame, text="Checker", command=lambda: self.open_new_window("COMPLETE", "Checker", self.custom_function6))
        complete_button.pack(pady=5, padx=5, fill='x')
        
        # Filteration Section
        checked_frame = ttk.Frame(self, padding=(10, 10, 10, 10))
        checked_frame.pack(fill='x', padx=20, pady=10)
        checked_label = ttk.Label(checked_frame, text="Filtration")
        checked_label.grid(row=0, column=0, columnspan=3, pady=10)
        button3_checked = ttk.Button(checked_frame, text="Raw", command=lambda: self.open_new_window("Raw", "Filtration", self.custom_function9))
        button3_checked.grid(row=1, column=0, sticky='ew', padx=5, pady=5)
        button1_checked = ttk.Button(checked_frame, text="Checked", command=lambda: self.open_new_window("Checked", "Filtration", self.custom_function7))
        button1_checked.grid(row=1, column=1, sticky='ew', padx=5, pady=5)
        button2_checked = ttk.Button(checked_frame, text="Complete", command=lambda: self.open_new_window("Complete", "Filtration", self.custom_function8))
        button2_checked.grid(row=1, column=2, sticky='ew', padx=5, pady=5)

       # Suppress Section
        suppress_frame = ttk.Frame(self, padding=(10, 10, 10, 10))
        suppress_frame.pack(fill='x', padx=20, pady=10)
        suppress_label = ttk.Label(suppress_frame, text="SUPPRESS OPTION")
        suppress_label.pack(pady=10)
        button_suppress = ttk.Button(suppress_frame, text="Suppress", command=lambda: self.open_new_window("Suppress", "Suppress Option", self.custom_function10))
        button_suppress.pack(pady=5, fill='x')


        checked_frame.columnconfigure(0, weight=1)
        checked_frame.columnconfigure(1, weight=1)
        checked_frame.columnconfigure(2, weight=1)

        

    def open_new_window(self, section_name, button_name, custom_function):
        if self.current_window:
            self.current_window.destroy()

        new_window = tk.Toplevel(self)
        new_window.title(f"{section_name} - {button_name}")
        new_window.geometry("400x300")
        new_window.configure(bg="#e0e0e0")

        style = ttk.Style(new_window)
        style.configure('TFrame', background="#ffffff", relief="solid", borderwidth=1)
        style.configure('TButton', background="#4caf50", foreground="black", font=('Arial', 12, 'bold'), relief="flat")
        style.map('TButton', background=[('active', '#45a049')])
        style.configure('TLabel', background="#ffffff", font=('Arial', 14, 'bold'))
        custom_function(new_window)

        self.current_window = new_window
    
    def custom_function7(self, window):
        self.window = window
        self.window.title("Checked: Viewer and Filtration")
        self.window.geometry("1350x350")

        # Initialize MySQL connection
        try:
            self.connection = mysql.connector.connect(
                host='localhost',
                database='search_engine_new',
                user='root',
                password=''
            )
            self.cursor = self.connection.cursor()
        except mysql.connector.Error as err:
            messagebox.showerror("MySQL Connection Error", f"Error connecting to MySQL: {err}")
            self.window.destroy()
            return

        # Initialize variables
        self.page_size = 10  # Number of rows per page
        self.current_page = 1
        self.total_pages = 0
        self.filtered_data = pd.DataFrame()

        # Initialize filters
        self.ins_type_filter = tk.StringVar()
        self.ins_name_filter = tk.StringVar()
        self.active_date_from = tk.StringVar()
        self.active_date_to = tk.StringVar()
        self.dob_from = tk.StringVar()
        self.dob_to = tk.StringVar()

        # Create GUI elements
        self.create_widgets()

    def create_widgets(self):
        # Frame for filter inputs
        filter_frame = ttk.Frame(self.window, padding=(10, 10, 10, 0))
        filter_frame.pack(fill=tk.X)

        # Insurance Type dropdown filter
        ttk.Label(filter_frame, text="Insurance Type:",font=("Arial", 8, "bold")).grid(row=0, column=0, padx=5, pady=5)
        self.ins_type_entry = ttk.Combobox(filter_frame, textvariable=self.ins_type_filter, width=20, state="readonly")
        self.ins_type_entry.grid(row=0, column=1, padx=5, pady=5)
        self.populate_ins_type_dropdown()

        # Insurance Name dropdown filter
        ttk.Label(filter_frame, text="Insurance Name:",font=("Arial", 8, "bold")).grid(row=0, column=2, padx=5, pady=5)
        self.ins_name_entry = ttk.Combobox(filter_frame, textvariable=self.ins_name_filter, width=20, state="readonly")
        self.ins_name_entry.grid(row=0, column=3, padx=5, pady=5)
        self.populate_ins_name_dropdown()

        # Active Date range filter
        ttk.Label(filter_frame, text="Active Date Range:",font=("Arial", 8, "bold")).grid(row=0, column=4, padx=5, pady=5)
        self.active_date_from_entry = ttk.Entry(filter_frame, textvariable=self.active_date_from, width=12)
        self.active_date_from_entry.grid(row=0, column=5, padx=5, pady=5)
        ttk.Label(filter_frame, text="to",font=("Arial", 5, "bold")).grid(row=0, column=6, padx=5, pady=5)
        self.active_date_to_entry = ttk.Entry(filter_frame, textvariable=self.active_date_to, width=12)
        self.active_date_to_entry.grid(row=0, column=7, padx=5, pady=5)

        # DOB range filter
        ttk.Label(filter_frame, text="DOB Range:",font=("Arial", 8, "bold")).grid(row=0, column=8, padx=5, pady=5)
        self.dob_from_entry = ttk.Entry(filter_frame, textvariable=self.dob_from, width=12)
        self.dob_from_entry.grid(row=0, column=9, padx=5, pady=5)
        ttk.Label(filter_frame, text="to",font=("Arial", 5, "bold")).grid(row=0, column=10, padx=5, pady=5)
        self.dob_to_entry = ttk.Entry(filter_frame, textvariable=self.dob_to, width=12)
        self.dob_to_entry.grid(row=0, column=11, padx=5, pady=5)

        # Filter button
        filter_button = ttk.Button(filter_frame, text="Filter", command=self.fetch_and_filter_data)
        filter_button.grid(row=0, column=12, padx=5, pady=5)

        # Export button
        export_button = ttk.Button(filter_frame, text="Excel", command=self.export_to_excel)
        export_button.grid(row=0, column=13, padx=5, pady=5)

        # Treeview for displaying data
        self.tree = ttk.Treeview(self.window, columns=("medicare_number", "first_name", "last_name", "gender", "active_date", "ins_name", "ins_type", "dob"), show="headings")
        self.tree.heading("medicare_number", text="MED ID")
        self.tree.heading("first_name", text="First Name")
        self.tree.heading("last_name", text="Last Name")
        self.tree.heading("gender", text="Gender")
        self.tree.heading("active_date", text="Active Date")
        self.tree.heading("ins_name", text="Insurance Name")
        self.tree.heading("ins_type", text="Insurance Type")
        self.tree.heading("dob", text="DOB")
        self.tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.fetch_and_filter_data()

    def populate_ins_type_dropdown(self):
        try:
            query = "SELECT DISTINCT ins_type FROM checked"
            self.cursor.execute(query)
            ins_types = [row[0] for row in self.cursor.fetchall()]
            self.ins_type_entry['values'] = [""] + ins_types  # Adding empty option
        except mysql.connector.Error as err:
            messagebox.showerror("MySQL Error", f"Error fetching InsType data: {err}")

    def populate_ins_name_dropdown(self):
        try:
            query = "SELECT DISTINCT ins_name FROM checked"
            self.cursor.execute(query)
            ins_names = [row[0] for row in self.cursor.fetchall()]
            self.ins_name_entry['values'] = [""] + ins_names  
        except mysql.connector.Error as err:
            messagebox.showerror("MySQL Error", f"Error fetching InsName data: {err}")

    def fetch_and_filter_data(self):
        ins_type = self.ins_type_filter.get()
        ins_name = self.ins_name_filter.get()
        active_date_from = self.active_date_from_entry.get()
        active_date_to = self.active_date_to_entry.get()
        dob_from = self.dob_from_entry.get()
        dob_to = self.dob_to_entry.get()

        # Validate and convert active dates
        try:
            active_date_from = datetime.strptime(active_date_from, "%Y-%m-%d").date() if active_date_from else None
            active_date_to = datetime.strptime(active_date_to, "%Y-%m-%d").date() if active_date_to else None
        except ValueError:
            messagebox.showerror("Date Format Error", "Invalid date format for Active Date. Please use YYYY-MM-DD.")
            return

        # Validate and convert DOB dates
        try:
            dob_from = datetime.strptime(dob_from, "%Y-%m-%d").date() if dob_from else None
            dob_to = datetime.strptime(dob_to, "%Y-%m-%d").date() if dob_to else None
        except ValueError:
            messagebox.showerror("Date Format Error", "Invalid date format for DOB. Please use YYYY-MM-DD.")
            return

        # Construct SQL query based on filters
        query = "SELECT medicare_number, first_name, last_name, gender, active_date, ins_name, ins_type, dob FROM checked WHERE 1=1"

        if ins_type:
            query += f" AND ins_type = '{ins_type}'"

        if ins_name:
            query += f" AND ins_name = '{ins_name}'"

        if active_date_from and active_date_to:
            query += f" AND active_date BETWEEN '{active_date_from}' AND '{active_date_to}'"

        if dob_from and dob_to:
            query += f" AND dob BETWEEN '{dob_from}' AND '{dob_to}'"

        # Fetch filtered data from MySQL table (limited by pagination)
        try:
            offset = (self.current_page - 1) * self.page_size
            query += f" LIMIT {self.page_size} OFFSET {offset}"
            self.cursor.execute(query)
            rows = self.cursor.fetchall()

            # Convert fetched data to DataFrame
            self.filtered_data = pd.DataFrame(rows, columns=['medicare_number', 'first_name', 'last_name', 'gender', 'active_date', 'ins_name', 'ins_type', 'dob'])

            # Clear previous data in Treeview
            for child in self.tree.get_children():
                self.tree.delete(child)

            # Insert data into Treeview
            for i, row in self.filtered_data.iterrows():
                self.tree.insert("", "end", values=list(row))

            # Update pagination information
            self.total_pages = self.get_total_pages()
            self.page_label.config(text=f"Page {self.current_page} of {self.total_pages}")

        except mysql.connector.Error as err:
            messagebox.showerror("MySQL Error", f"Error fetching data: {err}")

    def export_to_excel(self):
        ins_type = self.ins_type_filter.get()
        ins_name = self.ins_name_filter.get()
        active_date_from = self.active_date_from_entry.get()
        active_date_to = self.active_date_to_entry.get()
        dob_from = self.dob_from_entry.get()
        dob_to = self.dob_to_entry.get()

        # Validate and convert active dates
        try:
            active_date_from = datetime.strptime(active_date_from, "%Y-%m-%d").date() if active_date_from else None
            active_date_to = datetime.strptime(active_date_to, "%Y-%m-%d").date() if active_date_to else None
        except ValueError:
            messagebox.showerror("Date Format Error", "Invalid date format for Active Date. Please use YYYY-MM-DD.")
            return

        # Validate and convert DOB dates
        try:
            dob_from = datetime.strptime(dob_from, "%Y-%m-%d").date() if dob_from else None
            dob_to = datetime.strptime(dob_to, "%Y-%m-%d").date() if dob_to else None
        except ValueError:
            messagebox.showerror("Date Format Error", "Invalid date format for DOB. Please use YYYY-MM-DD.")
            return

        # Construct SQL query based on filters
        query = "SELECT * FROM checked WHERE 1=1"

        if ins_type:
            query += f" AND ins_type = '{ins_type}'"

        if ins_name:
            query += f" AND ins_name = '{ins_name}'"

        if active_date_from and active_date_to:
            query += f" AND active_date BETWEEN '{active_date_from}' AND '{active_date_to}'"

        if dob_from and dob_to:
            query += f" AND dob BETWEEN '{dob_from}' AND '{dob_to}'"

        # Fetch filtered data from MySQL table (limited by pagination)
        try:
            offset = (self.current_page - 1) * self.page_size
            # query += f" LIMIT {self.page_size} OFFSET {offset}"
            self.cursor.execute(query)
            rows = self.cursor.fetchall()

             # Convert fetched data to DataFrame
            column_names = [desc[0] for desc in self.cursor.description]
            self.filtered_data = pd.DataFrame(rows, columns=column_names)
            if not self.filtered_data['dob'].empty:
                self.filtered_data['dob'] = pd.to_datetime(self.filtered_data['dob'], errors='coerce')  # Convert to datetime, handle errors
                self.filtered_data['dob'] = self.filtered_data['dob'].dt.strftime('%m/%d/%Y')  # Format 'dob' column to MM/DD/YYYY
        except mysql.connector.Error as err:
            messagebox.showerror("MySQL Error", f"Error fetching data: {err}")
        # Export filtered data to Excel file
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            try:
                chunk_size = 50000  
                num_chunks = (len(self.filtered_data) // chunk_size) + 1

                for i in range(num_chunks):
                    start = i * chunk_size
                    end = min(start + chunk_size, len(self.filtered_data))
                    chunk = self.filtered_data.iloc[start:end]
                    chunk_file_path = f"{file_path[:-5]}_part{i+1}.xlsx"
                    chunk.to_excel(chunk_file_path, sheet_name='Sheet1', index=False)

                messagebox.showinfo("Export Successful", "Data exported to multiple Excel files successfully.")
            except Exception as e:
                messagebox.showerror("Export Error", f"An error occurred while exporting data: {e}")

    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.fetch_and_filter_data()

    def next_page(self):
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.fetch_and_filter_data()

    def get_total_pages(self):
        total_records = len(self.filtered_data)
        return (total_records // self.page_size) + (1 if total_records % self.page_size > 0 else 0)

    def custom_function8(self, window):
        self.window = window
        self.window.title("Complete: Viewer and Filtration")
        self.window.geometry("1350x350")

        # Initialize MySQL connection
        try:
            self.connection = mysql.connector.connect(
                host='localhost',
                database='search_engine_new',
                user='root',
                password=''
            )
            self.cursor = self.connection.cursor()
        except mysql.connector.Error as err:
            messagebox.showerror("MySQL Connection Error", f"Error connecting to MySQL: {err}")
            self.window.destroy()
            return

        # Initialize variables
        self.page_size = 10  # Number of rows per page
        self.current_page = 1
        self.total_pages = 0
        self.filtered_data = pd.DataFrame()

        # Initialize filters
        self.clients = tk.StringVar()
        self.dob_from = tk.StringVar()
        self.dob_to = tk.StringVar()

        # Create GUI elements
        self.create_widgets_()
        
    def custom_function9(self, window):
        self.window = window
        self.window.title("Raw: Viewer and Filtration")
        self.window.geometry("1350x350")

        # Initialize MySQL connection
        try:
            self.connection = mysql.connector.connect(
                host='localhost',
                database='search_engine_new',
                user='root',
                password=''
            )
            self.cursor = self.connection.cursor()
        except mysql.connector.Error as err:
            messagebox.showerror("MySQL Connection Error", f"Error connecting to MySQL: {err}")
            self.window.destroy()
            return

        # Initialize variables
        self.page_size = 10  # Number of rows per page
        self.current_page = 1
        self.total_pages = 0
        self.filtered_data = pd.DataFrame()

        # Initialize filters
        self.payer_options = []  # List to hold distinct payer values
        self.provider_name_options = []  # List to hold distinct provider names

        # Create GUI elements
        self.create_widgets_1()
        
    def populate_payer_dropdown(self):
        try:
            query = "SELECT DISTINCT payer FROM raw"
            self.cursor.execute(query)
            ins_types = [row[0] for row in self.cursor.fetchall()]
            self.payer['values'] = [""] + ins_types  # Adding empty option
        except mysql.connector.Error as err:
            messagebox.showerror("MySQL Error", f"Error fetching InsType data: {err}")

    def populate_provider_dropdown(self):
        try:
            query = "SELECT DISTINCT provider_name FROM raw"
            self.cursor.execute(query)
            ins_names = [row[0] for row in self.cursor.fetchall()]
            self.provider_name['values'] = [""] + ins_names  # Adding empty option
        except mysql.connector.Error as err:
            messagebox.showerror("MySQL Error", f"Error fetching InsName data: {err}")

    # def create_widgets_1(self):
    #     # Frame for filter inputs
    #     filter_frame = ttk.Frame(self.window, padding=(10, 10, 10, 0))
    #     filter_frame.pack(fill=tk.X)

    #     # Insurance Type dropdown filter
    #     ttk.Label(filter_frame, text="Payer:", font=("Arial", 8, "bold")).grid(row=0, column=0, padx=5, pady=5)
    #     self.payer = ttk.Combobox(filter_frame, values=self.payer_options, width=20, state="readonly")
    #     self.payer.grid(row=0, column=1, padx=5, pady=5)
    #     self.populate_payer_dropdown()

    #     ttk.Label(filter_frame, text="Provider Name:", font=("Arial", 8, "bold")).grid(row=0, column=2, padx=5, pady=5)
    #     self.provider_name = ttk.Combobox(filter_frame, values=self.provider_name_options, width=20, state="readonly")
    #     self.provider_name.grid(row=0, column=3, padx=5, pady=5)
    #     self.populate_provider_dropdown()
        
    #     # col 1 filter
    #     ttk.Label(filter_frame, text="Col 1:", font=("Arial", 8, "bold")).grid(row=0, column=2, padx=5, pady=5)
    #     self.provider_name = ttk.Combobox(filter_frame, values=self.provider_name_options, width=20, state="readonly")
    #     self.provider_name.grid(row=0, column=3, padx=5, pady=5)
    #     self.populate_provider_dropdown()
        
    #     # col2  filter 
    #     ttk.Label(filter_frame, text="Col 2:", font=("Arial", 8, "bold")).grid(row=0, column=2, padx=5, pady=5)
    #     self.provider_name = ttk.Combobox(filter_frame, values=self.provider_name_options, width=20, state="readonly")
    #     self.provider_name.grid(row=0, column=3, padx=5, pady=5)
    #     self.populate_provider_dropdown()
        
    #     # insight message 
    #     ttk.Label(filter_frame, text="Insight Message:", font=("Arial", 8, "bold")).grid(row=0, column=2, padx=5, pady=5)
    #     self.provider_name = ttk.Combobox(filter_frame, values=self.provider_name_options, width=20, state="readonly")
    #     self.provider_name.grid(row=0, column=3, padx=5, pady=5)
    #     self.populate_provider_dropdown()

    #     # Filter button
    #     filter_button = ttk.Button(filter_frame, text="Filter", command=self.fetch_and_filter_data_2)
    #     filter_button.grid(row=0, column=4, padx=5, pady=5)

    #     # Export button
    #     export_button = ttk.Button(filter_frame, text="Excel", command=self.export_to_excel_2)
    #     export_button.grid(row=0, column=5, padx=5, pady=5)

    #     # Treeview for displaying data
    #     self.tree = ttk.Treeview(self.window, columns=("medicare_number", "first_name", "last_name", "dob", "address","payer","provider_name"), show="headings")
    #     self.tree.heading("medicare_number", text="MED ID")
    #     self.tree.heading("first_name", text="First Name")
    #     self.tree.heading("last_name", text="Last Name")
    #     self.tree.heading("dob", text="DOB")
    #     self.tree.heading("address", text="Address")
    #     self.tree.heading("payer", text="Payer")
    #     self.tree.heading("provider_name", text="Provider Name")
    #     self.tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    #     # Populate dropdown values
    #     # self.populate_dropdown_values()
    #     self.fetch_and_filter_data_2()

    def create_widgets_1(self):
        # Frame for filter inputs
        filter_frame = ttk.Frame(self.window, padding=(10, 10, 10, 0))
        filter_frame.pack(fill=tk.X)

        # Payer dropdown filter
        ttk.Label(filter_frame, text="Payer:", font=("Arial", 8, "bold")).grid(row=0, column=0, padx=5, pady=5)
        self.payer = ttk.Combobox(filter_frame, values=self.payer_options, width=20, state="readonly")
        self.payer.grid(row=0, column=1, padx=5, pady=5)
        self.populate_payer_dropdown()

        # Provider Name dropdown filter
        ttk.Label(filter_frame, text="Provider Name:", font=("Arial", 8, "bold")).grid(row=0, column=2, padx=5, pady=5)
        self.provider_name = ttk.Combobox(filter_frame, values=self.provider_name_options, width=20, state="readonly")
        self.provider_name.grid(row=0, column=3, padx=5, pady=5)
        self.populate_provider_dropdown()
        
        # Col 1 filter
        ttk.Label(filter_frame, text="Col 1:", font=("Arial", 8, "bold")).grid(row=0, column=4, padx=5, pady=5)
        self.col_1 = ttk.Entry(filter_frame, width=20)
        self.col_1.grid(row=0, column=5, padx=5, pady=5)

        # Col 2 filter
        ttk.Label(filter_frame, text="Col 2:", font=("Arial", 8, "bold")).grid(row=0, column=6, padx=5, pady=5)
        self.col_2 = ttk.Entry(filter_frame, width=20)
        self.col_2.grid(row=0, column=7, padx=5, pady=5)

        # Insight Message filter
        ttk.Label(filter_frame, text="Ins Msg:", font=("Arial", 8, "bold")).grid(row=0, column=8, padx=5, pady=5)
        self.insight_message = ttk.Entry(filter_frame, width=20)
        self.insight_message.grid(row=0, column=9, padx=5, pady=5)

        # Filter button
        filter_button = ttk.Button(filter_frame, text="Filter", command=self.fetch_and_filter_data_2)
        filter_button.grid(row=0, column=10, padx=5, pady=5)

        # Export button
        export_button = ttk.Button(filter_frame, text="Excel", command=self.export_to_excel_2)
        export_button.grid(row=0, column=11, padx=5, pady=5)

        # Treeview for displaying data
        self.tree = ttk.Treeview(self.window, columns=("medicare_number", "first_name", "last_name", "dob", "address", "payer", "provider_name","col_1","col_2","insights_message"), show="headings")
        self.tree.heading("medicare_number", text="MED ID")
        self.tree.heading("first_name", text="First Name")
        self.tree.heading("last_name", text="Last Name")
        self.tree.heading("dob", text="DOB")
        self.tree.heading("address", text="Address")
        self.tree.heading("payer", text="Payer")
        self.tree.heading("provider_name", text="Provider Name")
        self.tree.heading("col_1", text="Col 1")
        self.tree.heading("col_2", text="Col 2")
        self.tree.heading("insights_message", text="Insight Message")
        self.tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Populate dropdown values
        # self.populate_dropdown_values()
        self.fetch_and_filter_data_2()  # Call this to initially populate data

        
    def fetch_and_filter_data_2(self):
        payer_filter = self.payer.get()  # Get selected payer filter value
        provider_name_filter = self.provider_name.get()  # Get selected provider name filter value
        col_1 = self.col_1.get()  # Get selected provider name filter value
        col_2 = self.col_2.get()  # Get selected provider name filter value
        insights_message = self.insight_message.get()  # Get selected provider name filter value
        # Construct base SQL query
        query = "SELECT medicare_number, first_name, last_name, dob, address , payer,provider_name,col_1,col_2,insights_message FROM raw WHERE 1=1"

        if payer_filter:
            query += f" AND payer = '{payer_filter}'"  # Assuming 'payer' is a column in your table

        if provider_name_filter:
            query += f" AND provider_name = '{provider_name_filter}'"  # Assuming 'provider_name' is a column in your table
 
        if col_1 and col_1 != None:
            query += f" AND col_1 = '{col_1}'"  
        if col_2 and col_2 != None:
            query += f" AND col_2 = '{col_2}'" 
        if insights_message and insights_message != None:
            query += f" AND insights_message = '{insights_message}'"  
        # Fetch filtered data from MySQL table (limited by pagination)
        try:
            offset = (self.current_page - 1) * self.page_size
            query += f" LIMIT {self.page_size} OFFSET {offset}"
            self.cursor.execute(query)
            rows = self.cursor.fetchall()

            # Convert fetched data to DataFrame
            self.filtered_data = pd.DataFrame(rows, columns=['medicare_number', 'first_name', 'last_name', 'dob', 'address','payer','provider_name','col_1','col_2','insights_message'])

            # Clear previous data in Treeview
            for child in self.tree.get_children():
                self.tree.delete(child)

            # Insert data into Treeview
            for i, row in self.filtered_data.iterrows():
                self.tree.insert("", "end", values=list(row))

        except mysql.connector.Error as err:
            messagebox.showerror("MySQL Error", f"Error fetching data: {err}")
            
    def export_to_excel_2(self):
        payer_filter = self.payer.get()  # Get selected payer filter value
        provider_name_filter = self.provider_name.get()  # Get selected provider name filter value
        col_1 = self.col_1.get()  # Get selected provider name filter value
        col_2 = self.col_2.get()  # Get selected provider name filter value
        insights_message = self.insight_message.get()  # Get selected provider name filter value

        # Construct base SQL query
        query = "SELECT * FROM raw WHERE 1=1"

        if payer_filter and payer_filter != None:
            query += f" AND payer = '{payer_filter}'"  # Assuming 'payer' is a column in your table

        if provider_name_filter and provider_name_filter != None:
            query += f" AND provider_name = '{provider_name_filter}'" 
        if col_1 and col_1 != None:
            query += f" AND col_1 = '{col_1}'"  
        if col_2 and col_2 != None:
            query += f" AND col_2 = '{col_2}'" 
        if insights_message and insights_message != None:
            query += f" AND insights_message = '{insights_message}'"  

        # Fetch filtered data from MySQL table (limited by pagination)
        try:
            offset = (self.current_page - 1) * self.page_size
            # query += f" LIMIT {self.page_size} OFFSET {offset}"
            self.cursor.execute(query)
            rows = self.cursor.fetchall()

            column_names = [desc[0] for desc in self.cursor.description]
            self.filtered_data = pd.DataFrame(rows, columns=column_names)
            if not self.filtered_data['dob'].empty:
                self.filtered_data['dob'] = pd.to_datetime(self.filtered_data['dob'], errors='coerce')  # Convert to datetime, handle errors
                self.filtered_data['dob'] = self.filtered_data['dob'].dt.strftime('%m/%d/%Y')  # Format 'dob' column to MM/DD/YYYY
                
        except mysql.connector.Error as err:
            messagebox.showerror("MySQL Error", f"Error fetching data: {err}")
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            try:
                chunk_size = 50000  
                num_chunks = (len(self.filtered_data) // chunk_size) + 1

                for i in range(num_chunks):
                    start = i * chunk_size
                    end = min(start + chunk_size, len(self.filtered_data))
                    chunk = self.filtered_data.iloc[start:end]
                    chunk_file_path = f"{file_path[:-5]}_part{i+1}.xlsx"
                    chunk.to_excel(chunk_file_path, sheet_name='Sheet1', index=False)

                messagebox.showinfo("Export Successful", "Data exported to multiple Excel files successfully.")
            except Exception as e:
                messagebox.showerror("Export Error", f"An error occurred while exporting data: {e}")
                
    def populate_dropdown_values(self):
        try:
            # Query distinct payer values
            self.cursor.execute("SELECT DISTINCT payer FROM raw")
            payer_results = self.cursor.fetchall()
            self.payer_options = [row[0] for row in payer_results]

            # Query distinct provider names
            self.cursor.execute("SELECT DISTINCT provider_name FROM raw")
            provider_name_results = self.cursor.fetchall()
            self.provider_name_options = [row[0] for row in provider_name_results]

            # Update Combobox values
            self.payer['values'] = self.payer_options
            self.provider_name['values'] = self.provider_name_options

        except mysql.connector.Error as err:
            messagebox.showerror("MySQL Query Error", f"Error querying MySQL: {err}")
        
    def populate_clients_dropdown(self):
        try:
            # Connect to MySQL database
            connection = mysql.connector.connect(
                host='localhost',
                database='search_engine_new',
                user='root',
                password=''
            )
            cursor = connection.cursor()

            # Fetch all clients from 'checked' table
            query = "SELECT client FROM complete"
            cursor.execute(query)
            clients = set()  # Using a set to ensure unique clients

            # Iterate through rows and collect unique clients
            for row in cursor.fetchall():
                client_list = row[0].split(',')  # Assuming clients are comma-separated
                clients.update(client_list)

            # Update dropdown values
            self.clients_entry['values'] = list(clients)

        except mysql.connector.Error as err:
            print(f"Error fetching clients from database: {err}")

        finally:
            # Close cursor and connection
            cursor.close()
            connection.close()
            
    def create_widgets_(self):
        # Frame for filter inputs
        filter_frame = ttk.Frame(self.window, padding=(10, 10, 10, 0))
        filter_frame.pack(fill=tk.X)

        # Insurance Type dropdown filter
        ttk.Label(filter_frame, text="Client:",font=("Arial", 8, "bold")).grid(row=0, column=0, padx=5, pady=5)
        self.clients_entry = ttk.Combobox(filter_frame, textvariable=self.clients, width=20, state="readonly")
        self.clients_entry.grid(row=0, column=1, padx=5, pady=5)
        self.populate_clients_dropdown()

        # DOB range filter
        ttk.Label(filter_frame, text="DOB Range:",font=("Arial", 8, "bold")).grid(row=0, column=8, padx=5, pady=5)
        self.dob_from_entry = ttk.Entry(filter_frame, textvariable=self.dob_from, width=12)
        self.dob_from_entry.grid(row=0, column=9, padx=5, pady=5)
        ttk.Label(filter_frame, text="to",font=("Arial", 5, "bold")).grid(row=0, column=10, padx=5, pady=5)
        self.dob_to_entry = ttk.Entry(filter_frame, textvariable=self.dob_to, width=12)
        self.dob_to_entry.grid(row=0, column=11, padx=5, pady=5)

        # Filter button
        filter_button = ttk.Button(filter_frame, text="Filter", command=self.fetch_and_filter_data_)
        filter_button.grid(row=0, column=12, padx=5, pady=5)

        # Export button
        export_button = ttk.Button(filter_frame, text="Excel", command=self.export_to_excel_)
        export_button.grid(row=0, column=13, padx=5, pady=5)

        # Treeview for displaying data
        self.tree = ttk.Treeview(self.window, columns=("medicare_number", "first_name", "last_name","gender", "dob", "address", "phone", "client"), show="headings")
        self.tree.heading("medicare_number", text="MED ID")
        self.tree.heading("first_name", text="First Name")
        self.tree.heading("last_name", text="Last Name")
        self.tree.heading("gender", text="Gender")
        self.tree.heading("dob", text="DOB")
        self.tree.heading("address", text="Address")
        self.tree.heading("phone", text="Phone")
        self.tree.heading("client", text="Client")
        self.tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Pagination buttons
        # pagination_frame = ttk.Frame(self.window)
        # pagination_frame.pack(fill=tk.X, padx=10, pady=10)

        # prev_button = ttk.Button(pagination_frame, text="Previous", command=self.prev_page)
        # prev_button.pack(side=tk.LEFT, padx=5)

        # self.page_label = ttk.Label(pagination_frame, text="")
        # self.page_label.pack(side=tk.LEFT, padx=5)

        # next_button = ttk.Button(pagination_frame, text="Next", command=self.next_page)
        # next_button.pack(side=tk.LEFT, padx=5)

        # Initialize with first page data
        self.fetch_and_filter_data_()
        
    

    def fetch_and_filter_data_(self):
        client = self.clients.get()
        dob_from = self.dob_from_entry.get()
        dob_to = self.dob_to_entry.get()


        # Validate and convert DOB dates
        try:
            dob_from = datetime.strptime(dob_from, "%Y-%m-%d").date() if dob_from else None
            dob_to = datetime.strptime(dob_to, "%Y-%m-%d").date() if dob_to else None
        except ValueError:
            messagebox.showerror("Date Format Error", "Invalid date format for DOB. Please use YYYY-MM-DD.")
            return

        # Construct SQL query based on filters
        query = "SELECT medicare_number, first_name, last_name, gender, dob, address, phone, client FROM complete WHERE 1=1"

        if client:
            query += f" AND client LIKE '%{client}%'"

        if dob_from and dob_to:
            query += f" AND dob BETWEEN '{dob_from}' AND '{dob_to}'"

        # Fetch filtered data from MySQL table (limited by pagination)
        try:
            offset = (self.current_page - 1) * self.page_size
            query += f" LIMIT {self.page_size} OFFSET {offset}"
            self.cursor.execute(query)
            rows = self.cursor.fetchall()

            # Convert fetched data to DataFrame
            self.filtered_data = pd.DataFrame(rows, columns=['medicare_number', 'first_name', 'last_name', 'gender', 'dob', 'address', 'phone', 'client'])

            # Clear previous data in Treeview
            for child in self.tree.get_children():
                self.tree.delete(child)

            # Insert data into Treeview
            for i, row in self.filtered_data.iterrows():
                self.tree.insert("", "end", values=list(row))

            # # Update pagination information
            # self.total_pages = self.get_total_pages()
            # self.page_label.config(text=f"Page {self.current_page} of {self.total_pages}")

        except mysql.connector.Error as err:
            messagebox.showerror("MySQL Error", f"Error fetching data: {err}")

    def export_to_excel_(self):
        client = self.clients.get()
        dob_from = self.dob_from_entry.get()
        dob_to = self.dob_to_entry.get()


        # Validate and convert DOB dates
        try:
            dob_from = datetime.strptime(dob_from, "%Y-%m-%d").date() if dob_from else None
            dob_to = datetime.strptime(dob_to, "%Y-%m-%d").date() if dob_to else None
        except ValueError:
            messagebox.showerror("Date Format Error", "Invalid date format for DOB. Please use YYYY-MM-DD.")
            return

        # Construct SQL query based on filters
        query = "SELECT * FROM complete WHERE 1=1"

        if client:
            query += f" AND client LIKE '%{client}%'"

        if dob_from and dob_to:
            query += f" AND dob BETWEEN '{dob_from}' AND '{dob_to}'"

        try:
            self.cursor.execute(query)
            rows = self.cursor.fetchall()

            column_names = [desc[0] for desc in self.cursor.description]
            self.filtered_data = pd.DataFrame(rows, columns=column_names)
            if not self.filtered_data['dob'].empty:
                self.filtered_data['dob'] = pd.to_datetime(self.filtered_data['dob'], errors='coerce')  # Convert to datetime, handle errors
                self.filtered_data['dob'] = self.filtered_data['dob'].dt.strftime('%m/%d/%Y')  # Format 'dob' column to MM/DD/YYYY
        except mysql.connector.Error as err:
            messagebox.showerror("MySQL Error", f"Error fetching data: {err}")
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            try:
                chunk_size = 50000  
                num_chunks = (len(self.filtered_data) // chunk_size) + 1

                for i in range(num_chunks):
                    start = i * chunk_size
                    end = min(start + chunk_size, len(self.filtered_data))
                    chunk = self.filtered_data.iloc[start:end]
                    chunk_file_path = f"{file_path[:-5]}_part{i+1}.xlsx"
                    chunk.to_excel(chunk_file_path, sheet_name='Sheet1', index=False)

                messagebox.showinfo("Export Successful", "Data exported to multiple Excel files successfully.")
            except Exception as e:
                messagebox.showerror("Export Error", f"An error occurred while exporting data: {e}")

    def custom_function1(self, window):
        window.title("Raw Checker 1")
        window.geometry("700x600")
        window.configure(bg="#f0f0f0")

        style = ttk.Style(window)
        style.configure('TFrame', background="#ffffff", relief="solid", borderwidth=1)
        style.configure('TButton', background="#4caf50", foreground="black", font=('Arial', 12, 'bold'), relief="flat")
        style.map('TButton', background=[('active', '#45a049')])
        style.configure('TLabel', background="#ffffff", font=('Arial', 14, 'bold'))

        upload_frame = ttk.Frame(window, padding=(20, 20, 20, 10))
        upload_frame.pack(fill='x')

        upload_label = ttk.Label(upload_frame, text="Upload Excel File:")
        upload_label.grid(row=0, column=0, padx=10, pady=10)

        self.file_path_var = tk.StringVar()
        upload_entry = ttk.Entry(upload_frame, textvariable=self.file_path_var, width=50)
        upload_entry.grid(row=0, column=1, padx=10, pady=10)

        upload_button = ttk.Button(upload_frame, text="Browse", command=self.browse_file)
        upload_button.grid(row=0, column=2, padx=10, pady=10)

        dropdown_frame = ttk.Frame(window, padding=(20, 10, 20, 20))
        dropdown_frame.pack(fill='both', expand=True)

        self.dropdown_vars = {}  
        self.dropdowns = []     
        
        columns = [
            ("First Name", "first_name"),
            ("Last Name", "last_name"),
            ("DOB", "dob"),
            ("Address", "address"),
            ("City", "city"),
            ("State", "state"),
            ("Zip", "zip"),
            ("Medicare Number(MBI)", "medicare_number")
        ]


        for i, (label_text, db_column) in enumerate(columns):
            label = ttk.Label(dropdown_frame, text=label_text)
            label.grid(row=i, column=0, padx=10, pady=10, sticky='w')

            self.dropdown_vars[db_column] = tk.StringVar()
            dropdown = ttk.Combobox(dropdown_frame, textvariable=self.dropdown_vars[db_column], state='disabled', width=30)
            dropdown.grid(row=i, column=1, padx=10, pady=10)
            self.dropdowns.append(dropdown)

        import_button = ttk.Button(dropdown_frame, text="Import Data", command=lambda: self.import_data(window))
        import_button.grid(row=len(columns), column=1, padx=10, pady=10)

    def custom_function2(self, window):
        window.title("Raw Checker 2")
        window.geometry("700x350")
        window.configure(bg="#f0f0f0")
        style = ttk.Style(window)
        style.configure('TFrame', background="#ffffff", relief="solid", borderwidth=1)
        style.configure('TButton', background="#4caf50", foreground="black", font=('Arial', 12, 'bold'), relief="flat")
        style.map('TButton', background=[('active', '#45a049')])
        style.configure('TLabel', background="#ffffff", font=('Arial', 14, 'bold'))

        upload_frame = ttk.Frame(window, padding=(20, 20, 20, 10))
        upload_frame.pack(fill='x')

        upload_label = ttk.Label(upload_frame, text="Upload Excel File:")
        upload_label.grid(row=0, column=0, padx=10, pady=10)

        self.file_path_var = tk.StringVar()
        upload_entry = ttk.Entry(upload_frame, textvariable=self.file_path_var, width=50)
        upload_entry.grid(row=0, column=1, padx=10, pady=10)

        upload_button = ttk.Button(upload_frame, text="Browse", command=self.browse_file)
        upload_button.grid(row=0, column=2, padx=10, pady=10)

        dropdown_frame = ttk.Frame(window, padding=(20, 10, 20, 20))
        dropdown_frame.pack(fill='both', expand=True)

        self.dropdown_vars = {}  
        self.dropdowns = []     

        columns = [
            ("Full Name", "full_name"),
            ("DOB", "dob"),
            ("State", "state"),
            ("Medicare Number(MBI)", "medicare_number")
        ]


        for i, (label_text, db_column) in enumerate(columns):
            label = ttk.Label(dropdown_frame, text=label_text)
            label.grid(row=i, column=0, padx=10, pady=10, sticky='w')

            self.dropdown_vars[db_column] = tk.StringVar()
            dropdown = ttk.Combobox(dropdown_frame, textvariable=self.dropdown_vars[db_column], state='disabled', width=30)
            dropdown.grid(row=i, column=1, padx=10, pady=10)
            self.dropdowns.append(dropdown)

        import_button = ttk.Button(dropdown_frame, text="Import Data", command=lambda: self.import_data_1(window))
        import_button.grid(row=len(columns), column=1, padx=10, pady=10)

    def custom_function3(self, window):
        window.title("Raw Checker 3")
        window.geometry("700x530")
        window.configure(bg="#f0f0f0")
        style = ttk.Style(window)
        style.configure('TFrame', background="#ffffff", relief="solid", borderwidth=1)
        style.configure('TButton', background="#4caf50", foreground="black", font=('Arial', 12, 'bold'), relief="flat")
        style.map('TButton', background=[('active', '#45a049')])
        style.configure('TLabel', background="#ffffff", font=('Arial', 14, 'bold'))
        upload_frame = ttk.Frame(window, padding=(20, 20, 20, 10))
        upload_frame.pack(fill='x')

        upload_label = ttk.Label(upload_frame, text="Upload Excel File:")
        upload_label.grid(row=0, column=0, padx=10, pady=10)

        self.file_path_var = tk.StringVar()
        upload_entry = ttk.Entry(upload_frame, textvariable=self.file_path_var, width=50)
        upload_entry.grid(row=0, column=1, padx=10, pady=10)

        upload_button = ttk.Button(upload_frame, text="Browse", command=self.browse_file)
        upload_button.grid(row=0, column=2, padx=10, pady=10)

        dropdown_frame = ttk.Frame(window, padding=(20, 10, 20, 20))
        dropdown_frame.pack(fill='both', expand=True)

        self.dropdown_vars = {}  
        self.dropdowns = []     

        columns = [
            ("Patient Name", "full_name"),
            ("Medicare Number(MBI)", "medicare_number"),
            ("Payer", "payer"),
            ("Provider Name", "provider_name"),
            ("Insights Message", "insights_message"),
            ("Coloumn 1", "col_1"),
            ("Coloumn 2", "col_2")
        ]

        for i, (label_text, db_column) in enumerate(columns):
            label = ttk.Label(dropdown_frame, text=label_text)
            label.grid(row=i, column=0, padx=10, pady=10, sticky='w')

            self.dropdown_vars[db_column] = tk.StringVar()
            dropdown = ttk.Combobox(dropdown_frame, textvariable=self.dropdown_vars[db_column], state='disabled', width=30)
            dropdown.grid(row=i, column=1, padx=10, pady=10)
            self.dropdowns.append(dropdown)

        import_button = ttk.Button(dropdown_frame, text="Import Data", command=lambda: self.import_data_2(window))
        import_button.grid(row=len(columns), column=1, padx=10, pady=10)

    def custom_function4(self, window):
        window.title("Checked Checker 1")
        window.geometry("800x450")
        window.configure(bg="#f0f0f0")
        style = ttk.Style(window)
        style.configure('TFrame', background="#ffffff", relief="solid", borderwidth=1)
        style.configure('TButton', background="#4caf50", foreground="black", font=('Arial', 12, 'bold'), relief="flat")
        style.map('TButton', background=[('active', '#45a049')])
        style.configure('TLabel', background="#ffffff", font=('Arial', 14, 'bold'))

        upload_frame = ttk.Frame(window, padding=(20, 20, 20, 10))
        upload_frame.pack(fill='x')

        upload_label = ttk.Label(upload_frame, text="Upload Excel File:")
        upload_label.grid(row=0, column=0, padx=10, pady=10)

        self.file_path_var = tk.StringVar()
        upload_entry = ttk.Entry(upload_frame, textvariable=self.file_path_var, width=50)
        upload_entry.grid(row=0, column=1, padx=10, pady=10)

        upload_button = ttk.Button(upload_frame, text="Browse", command=self.browse_file)
        upload_button.grid(row=0, column=2, padx=10, pady=10)

        dropdown_frame = ttk.Frame(window, padding=(20, 10, 20, 20))
        dropdown_frame.pack(fill='both', expand=True)

        self.dropdown_vars = {}  
        self.dropdowns = []     

        columns = [
            ("Patient Name", "full_name"),
            ("Medicare Number(MBI)", "medicare_number"),
            ("DOB", "dob"),
            ("Gender", "gender"),
            ("Address", "address"),
            ("Payer", "payer"),
            ("Plan", "plan"),
            ("Ins Name", "ins_name"),
            ("Ins Type", "ins_type"),
            ("MSP", "msp"),
            ("Modify", "checked")  
        ]

        num_columns = 2 

        for i, (label_text, db_column) in enumerate(columns):
            col = i % num_columns  
            row = i // num_columns 

            label = ttk.Label(dropdown_frame, text=label_text)
            label.grid(row=row, column=col * 2, padx=10, pady=10, sticky='w')

            if db_column == "checked":
                self.dropdown_vars[db_column] = tk.IntVar()
                checked_button = ttk.Checkbutton(dropdown_frame, variable=self.dropdown_vars[db_column], text="Checked")
                checked_button.grid(row=row, column=col * 2 + 1, padx=10, pady=10, sticky='w')
            else:
                self.dropdown_vars[db_column] = tk.StringVar()
                dropdown = ttk.Combobox(dropdown_frame, textvariable=self.dropdown_vars[db_column], state='disabled', width=30)
                dropdown.grid(row=row, column=col * 2 + 1, padx=10, pady=10)
                self.dropdowns.append(dropdown)

        import_button = ttk.Button(dropdown_frame, text="Import Data", command=lambda: self.import_data_4(window))
        import_button.grid(row=(len(columns) // num_columns) + 1, column=1, padx=10, pady=10)


    def custom_function5(self, window):
        window.title("Checked Checker 2")
        window.geometry("800x480")
        window.configure(bg="#f0f0f0")
        style = ttk.Style(window)
        style.configure('TFrame', background="#ffffff", relief="solid", borderwidth=1)
        style.configure('TButton', background="#4caf50", foreground="black", font=('Arial', 12, 'bold'), relief="flat")
        style.map('TButton', background=[('active', '#45a049')])
        style.configure('TLabel', background="#ffffff", font=('Arial', 14, 'bold'))

        upload_frame = ttk.Frame(window, padding=(20, 20, 20, 10))
        upload_frame.pack(fill='x')

        upload_label = ttk.Label(upload_frame, text="Upload Excel File:")
        upload_label.grid(row=0, column=0, padx=10, pady=10)

        self.file_path_var = tk.StringVar()
        upload_entry = ttk.Entry(upload_frame, textvariable=self.file_path_var, width=50)
        upload_entry.grid(row=0, column=1, padx=10, pady=10)

        upload_button = ttk.Button(upload_frame, text="Browse", command=self.browse_file)
        upload_button.grid(row=0, column=2, padx=10, pady=10)

        dropdown_frame = ttk.Frame(window, padding=(20, 10, 20, 20))
        dropdown_frame.pack(fill='both', expand=True)

        self.dropdown_vars = {} 
        self.dropdowns = []     

        columns = [
            ("Patient Name", "full_name"),
            ("DOB", "dob"),
            ("Gender", "gender"),
            ("Address", "address"),
            ("City", "city"),
            ("State", "state"),
            ("Zip", "zip"),
            ("Active Date", "active_date"),
            ("Ins Name", "ins_name"),
            ("Ins Type", "ins_type"),
            ("MSP", "msp"),
            ("Modify", "checked")  
        ]

        num_columns = 2  
        for i, (label_text, db_column) in enumerate(columns):
            col = i % num_columns  
            row = i // num_columns  

            label = ttk.Label(dropdown_frame, text=label_text)
            label.grid(row=row, column=col * 2, padx=10, pady=10, sticky='w')

            if db_column == "checked":
                self.dropdown_vars[db_column] = tk.IntVar()
                checked_button = ttk.Checkbutton(dropdown_frame, variable=self.dropdown_vars[db_column], text="Checked")
                checked_button.grid(row=row, column=col * 2 + 1, padx=10, pady=10, sticky='w')
            else:
                self.dropdown_vars[db_column] = tk.StringVar()
                dropdown = ttk.Combobox(dropdown_frame, textvariable=self.dropdown_vars[db_column], state='disabled', width=30)
                dropdown.grid(row=row, column=col * 2 + 1, padx=10, pady=10)
                self.dropdowns.append(dropdown)

        import_button = ttk.Button(dropdown_frame, text="Import Data", command=lambda: self.import_data_3(window))
        import_button.grid(row=len(columns) // num_columns + 1, column=1, padx=10, pady=10)  

        
    def custom_function10(self, window):
        window.title("Suppress")
        window.geometry("660x250")
        window.configure(bg="#f0f0f0")
        style = ttk.Style(window)
        style.configure('TFrame', background="#ffffff", relief="solid", borderwidth=1)
        style.configure('TButton', background="#4caf50", foreground="black", font=('Arial', 12, 'bold'), relief="flat")
        style.map('TButton', background=[('active', '#45a049')])
        style.configure('TLabel', background="#ffffff", font=('Arial', 14, 'bold'))

        upload_frame = ttk.Frame(window, padding=(20, 20, 20, 10))
        upload_frame.pack(fill='x')

        upload_label = ttk.Label(upload_frame, text="Upload Excel File:")
        upload_label.grid(row=0, column=0, padx=10, pady=10)

        self.file_path_var = tk.StringVar()
        upload_entry = ttk.Entry(upload_frame, textvariable=self.file_path_var, width=50)
        upload_entry.grid(row=0, column=1, padx=10, pady=10)

        upload_button = ttk.Button(upload_frame, text="Browse", command=self.browse_file)
        upload_button.grid(row=0, column=2, padx=10, pady=10)

        dropdown_frame = ttk.Frame(window, padding=(20, 10, 20, 20))
        dropdown_frame.pack(fill='both', expand=True)

        self.dropdown_vars = {}
        self.dropdowns = []

        # Dropdown for selecting between RAW, CHECKED, and COMPLETE
        label_type = ttk.Label(dropdown_frame, text="Select Type:")
        label_type.grid(row=0, column=0, padx=10, pady=10, sticky='w')

        self.type_var = tk.StringVar()
        type_dropdown = ttk.Combobox(dropdown_frame, textvariable=self.type_var, values=["RAW", "CHECKED", "COMPLETE"], state='readonly', width=20)
        type_dropdown.grid(row=0, column=1, padx=10, pady=10)

        columns = [
            ("Medicare ID", "med_id"),
        ]

        for i, (label_text, db_column) in enumerate(columns, start=1):
            label = ttk.Label(dropdown_frame, text=label_text)
            label.grid(row=i, column=0, padx=10, pady=10, sticky='w')

            self.dropdown_vars[db_column] = tk.StringVar()
            dropdown = ttk.Combobox(dropdown_frame, textvariable=self.dropdown_vars[db_column], state='disabled', width=30)
            dropdown.grid(row=i, column=1, padx=10, pady=10)
            self.dropdowns.append(dropdown)

        import_button = ttk.Button(dropdown_frame, text="Delete Data", command=lambda: self.delete_data(window))
        import_button.grid(row=len(columns) + 1, column=1, padx=10, pady=10)

        
    def delete_data(self, window):
        # Get the selected type (RAW, CHECKED, COMPLETE) from the dropdown
        selected_type = self.type_var.get()

        if not selected_type:
            messagebox.showerror("Error", "Please select a data type to delete.")
            return

        confirmed = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete data from {selected_type} table? This action cannot be undone.")

        if not confirmed:
            return

        try:
            file_path = self.file_path_var.get()
            selected_columns = [self.dropdown_vars[db_col].get() for db_col in self.dropdown_vars if self.dropdown_vars[db_col].get()]

            if not file_path or not selected_columns:
                messagebox.showerror("Error", "Please select a file and columns to delete.")
                return

            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path, usecols=selected_columns)
            else:
                df = pd.read_excel(file_path, usecols=selected_columns)

            connection = mysql.connector.connect(
                host='localhost',
                database='search_engine_new',
                user='root',
                password=''
            )
            cursor = connection.cursor()
            row_count = 0
            skipped_count = 0

            for index, row in df.iterrows():
                medicare_number = row[selected_columns[0]]

                # Handle empty or NaN values
                if pd.isnull(medicare_number) or medicare_number == '':
                    skipped_count += 1
                    continue

                # Delete row from selected table based on selected_type
                if selected_type == "RAW":
                    table_name = "raw"
                elif selected_type == "CHECKED":
                    table_name = "checked"
                elif selected_type == "COMPLETE":
                    table_name = "complete"
                else:
                    messagebox.showerror("Error", "Invalid data type selected.")
                    return

                try:
                    query = f"DELETE FROM {table_name} WHERE medicare_number = %s"
                    cursor.execute(query, (medicare_number,))
                    connection.commit()
                    row_count += 1
                except mysql.connector.Error as e:
                    print(f"Error deleting row with Medicare number {medicare_number}: {e}")
                    skipped_count += 1

            messagebox.showinfo("Success", f"Data deletion completed.\nRows deleted: {row_count}\nRows skipped: {skipped_count}")
            window.after(0, window.destroy)

        except Exception as e:
            print(f"")

        finally:
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()
    def custom_function6(self, window):
        window.title("Complete Checker 1")
        window.geometry("800x500")
        window.configure(bg="#f0f0f0")
        style = ttk.Style(window)
        style.configure('TFrame', background="#ffffff", relief="solid", borderwidth=1)
        style.configure('TButton', background="#4caf50", foreground="black", font=('Arial', 12, 'bold'), relief="flat")
        style.map('TButton', background=[('active', '#45a049')])
        style.configure('TLabel', background="#ffffff", font=('Arial', 14, 'bold'))

        upload_frame = ttk.Frame(window, padding=(20, 20, 20, 10))
        upload_frame.pack(fill='x')

        upload_label = ttk.Label(upload_frame, text="Upload Excel File:")
        upload_label.grid(row=0, column=0, padx=10, pady=10)

        self.file_path_var = tk.StringVar()
        upload_entry = ttk.Entry(upload_frame, textvariable=self.file_path_var, width=50)
        upload_entry.grid(row=0, column=1, padx=10, pady=10)

        upload_button = ttk.Button(upload_frame, text="Browse", command=self.browse_file)
        upload_button.grid(row=0, column=2, padx=10, pady=10)

        dropdown_frame = ttk.Frame(window, padding=(20, 10, 20, 20))
        dropdown_frame.pack(fill='both', expand=True)

        self.dropdown_vars = {} 
        self.dropdowns = []     

        columns = [
            ("Patient Name", "full_name"),
            ("Medicare ID", "med_id"),
            ("DOB", "dob"),
            ("Age", "age"),
            ("Gender", "gender"),
            ("Address", "address"),
            ("Phone", "phone"),
            ("Alternative Number", "alt_number"),
            ("Month Year", "month_year"),
            ("Dr Name", "dr_name"),
            ("Dr NPI", "dr_npi"),
            ("Client", "client")
        ]

        num_columns = 2  

        for i, (label_text, db_column) in enumerate(columns):
            col = i % num_columns  
            row = i // num_columns 

            label = ttk.Label(dropdown_frame, text=label_text)
            label.grid(row=row, column=col * 2, padx=10, pady=10, sticky='w')

            self.dropdown_vars[db_column] = tk.StringVar()
            dropdown = ttk.Combobox(dropdown_frame, textvariable=self.dropdown_vars[db_column], state='disabled', width=30)
            dropdown.grid(row=row, column=col * 2 + 1, padx=10, pady=10)
            self.dropdowns.append(dropdown)

        import_button = ttk.Button(dropdown_frame, text="Import Data", command=lambda: self.import_data_5(window))
        import_button.grid(row=(len(columns) + 1) // num_columns, column=1, padx=10, pady=10)

    # def browse_file(self):
    #     file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls")])
    #     if file_path:
    #         self.file_path_var.set(file_path)
    #         self.load_dropdowns(file_path)

    # def load_dropdowns(self, file_path):
    #     try:
    #         df = pd.read_excel(file_path)
    #         headers = df.columns.tolist()

    #         for dropdown in self.dropdowns:
    #             dropdown['values'] = ['NULL'] + headers
    #             dropdown.config(state='readonly')

    #     except Exception as e:
    #         print(f"Error loading file: {e}")
    #         for dropdown in self.dropdowns:
    #             dropdown.config(state='disabled')
    
    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls"), ("CSV files", "*.csv")])
        if file_path:
            self.file_path_var.set(file_path)
            self.load_dropdowns(file_path)

    def load_dropdowns(self, file_path):
        try:
            # Determine file type and read data accordingly
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            else:
                df = pd.read_excel(file_path)
            
            headers = df.columns.tolist()

            # Update dropdowns
            for dropdown in self.dropdowns:
                dropdown['values'] = ['NULL'] + headers
                dropdown.config(state='readonly')

        except Exception as e:
            print(f"Error loading file: {e}")
            for dropdown in self.dropdowns:
                dropdown.config(state='disabled')

    def format_date(self, date):
        try:
            if date:
                if isinstance(date, datetime):
                    parsed_date = date
                else:
                    formats_to_try = [
                        '%m/%d/%Y', '%m-%d-%Y', '%Y-%m-%d',  
                        '%d/%m/%Y', '%d-%m-%Y', '%Y-%d-%m',  
                        '%Y/%m/%d', '%Y-%m-%d',              
                        '%m/%d/%y', '%m-%d-%y', '%y-%m-%d',  
                        '%d/%m/%y', '%d-%m-%y', '%y-%d-%m',  
                        '%Y/%m/%d %H:%M:%S', '%Y-%m-%d %H:%M:%S', 
                        '%m/%d/%Y %H:%M:%S', '%m-%d-%Y %H:%M:%S', 
                        '%d/%m/%Y %H:%M:%S', '%d-%m-%Y %H:%M:%S',
                    ]
                    
                    parsed_date = None
                    for fmt in formats_to_try:
                        try:
                            parsed_date = datetime.strptime(date, fmt)
                            break  # Exit loop if successfully parsed
                        except ValueError:
                            continue  # Continue to next format if current one fails
                    
                    if not parsed_date:
                        return None  # Return None if all formats fail
                    
            else:
                return None
        except ValueError:
            return None
    
        formatted_date = parsed_date.strftime('%Y-%m-%d')
        return formatted_date

    def clean_string(self, text):
        if isinstance(text, str):
            cleaned_text = re.sub(r'[^\w\s-]', '', text)  
            return cleaned_text.strip()
        else:
            return None
        
    def clean_numbers(self,text):
        if isinstance(text, str):
            cleaned_text = re.sub(r'\D', '', text)
            return cleaned_text
        else:
            return None
        
    def import_data(self, window):
        try:
            file_path = self.file_path_var.get()
            selected_columns = [self.dropdown_vars[db_col].get() for db_col in self.dropdown_vars if self.dropdown_vars[db_col].get()]
            
            if file_path and selected_columns:
                if file_path.endswith('.csv'):
                    df = pd.read_csv(file_path, usecols=selected_columns)
                else:
                    df = pd.read_excel(file_path, usecols=selected_columns)
                
                connection = mysql.connector.connect(host='localhost', database='search_engine_new', user='root', password='')
                cursor = connection.cursor()
                row_count = 0
                skipped_count= 0
                for index, row in df.iterrows():
                    if selected_columns[0] == "NULL":
                        first_name = None
                    else:
                        first_name = self.clean_string(row[selected_columns[0]])
                    if selected_columns[1] == "NULL":
                        last_name = None
                    else:
                        last_name = self.clean_string(row[selected_columns[1]])
                    if selected_columns[2] == "NULL":
                        dob = None
                    else:
                        dob = self.format_date(row[selected_columns[2]])
                    if selected_columns[3] == "NULL":
                        address = None
                    else:
                        address = row[selected_columns[3]]
                    if selected_columns[4] == "NULL":
                        city = None
                    else:
                        city = row[selected_columns[4]]
                    if selected_columns[5]== "NULL":
                        state = None
                    else:
                        state = row[selected_columns[5]]
                    if selected_columns[6] == "NULL":
                        zip_code = None
                    else:
                        zip_code = row[selected_columns[6]]
                    if selected_columns[7] == "NULL":
                        medicare_number = None
                    else:
                        medicare_number = self.clean_string(row[selected_columns[7]])
                        
                    # Handle NaN values
                    if pd.isnull(first_name):
                        first_name = None
                    if pd.isnull(last_name):
                        last_name = None
                    if pd.isnull(dob):
                        dob = None
                    if pd.isnull(city):
                        city = None
                    if pd.isnull(address):
                        address = None
                    if pd.isnull(state):
                        state = None
                    if pd.isnull(zip_code):
                        zip_code = None
                    if pd.isnull(medicare_number):
                        medicare_number = None
                    
                
                    query = "INSERT INTO raw (first_name, last_name, dob, address, city, state, zip, medicare_number) " \
                            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                            
                    values = (
                        first_name,
                        last_name,
                        dob,
                        address,
                        city,
                        state,
                        zip_code,
                        medicare_number
                    )
                    try:
                        cursor.execute(query, values)
                        connection.commit()
                        row_count += 1
                    except mysql.connector.IntegrityError as e:
                        skipped_count += 1
                    except Exception as e:
                        skipped_count += 1

                cursor.close()
                connection.close()
                messagebox.showinfo("Success", f"Data imported successfully!\nRows inserted: {row_count}\nRows skipped: {skipped_count}")
                window.after(0, window.destroy)
            else:
                messagebox.showerror("Error", "Please select a file and columns to import.")

        except Exception as e:
            print(f"")

    def import_data_1(self, window):
        try:
            file_path = self.file_path_var.get()
            selected_columns = [self.dropdown_vars[db_col].get() for db_col in self.dropdown_vars if self.dropdown_vars[db_col].get()]

            if file_path and selected_columns:
                if file_path.endswith('.csv'):
                    df = pd.read_csv(file_path, usecols=selected_columns)
                else:
                    df = pd.read_excel(file_path, usecols=selected_columns)

                connection = mysql.connector.connect(
                    host='localhost',
                    database='search_engine_new',
                    user='root',
                    password=''
                )
                cursor = connection.cursor()
                row_count = 0
                skipped_count = 0

                for index, row in df.iterrows():
                    if selected_columns[0]== 'NULL':
                        full_name = None
                    else:
                        full_name = row[selected_columns[0]]
                    if selected_columns[1] == "NULL":
                        dob = None
                    else:
                        dob = None
                        if row[selected_columns[1]] == '' or row[selected_columns[1]] is None:
                            dob = None
                        else:
                            dob = self.format_date_1(row[selected_columns[1]])
                    if selected_columns[2] == "NULL":
                        state = None
                    else:
                        state = row[selected_columns[2]]
                    if selected_columns[3] == "NULL":
                        medicare_number = None
                    else:
                        medicare_number = self.clean_string(row[selected_columns[3]])

                    # Split full name into first name and last name
                    if pd.notnull(full_name):
                        names = full_name.split()
                        first_name = names[0]
                        last_name = ' '.join(names[1:]) if len(names) > 1 else None
                    else:
                        first_name = None
                        last_name = None
                    
                    # Handle NaN values
                    if pd.isnull(full_name):
                        full_name = None
                    if pd.isnull(last_name):
                        last_name = None
                    if pd.isnull(dob):
                        dob = None
                    if pd.isnull(state):
                        state = None
                    if pd.isnull(medicare_number):
                        medicare_number = None

                    query = (
                        "INSERT INTO raw (first_name, last_name, dob, address, city, state, zip, medicare_number) "
                        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                    )
                    values = (
                        self.clean_string(first_name),
                        self.clean_string(last_name),
                        dob,
                        None,  # address
                        None,  # city
                        state,
                        None,  # zip
                        medicare_number
                    )

                    try:
                        cursor.execute(query, values)
                        connection.commit()
                        row_count += 1
                    except mysql.connector.IntegrityError:
                        skipped_count += 1
                    except Exception:
                        skipped_count += 1

                cursor.close()
                connection.close()
                messagebox.showinfo("Success", f"Data imported successfully!\nRows inserted: {row_count}\nRows skipped: {skipped_count}")
                window.after(0, window.destroy)
            else:
                messagebox.showerror("Error", "Please select a file and columns to import.")

        except Exception as e:
            print(f"")
            
    def import_data_2(self, window):
        try:
            file_path = self.file_path_var.get()
            selected_columns = [self.dropdown_vars[db_col].get() for db_col in self.dropdown_vars if self.dropdown_vars[db_col].get()]

            if file_path and selected_columns:
                if file_path.endswith('.csv'):
                    df = pd.read_csv(file_path, usecols=selected_columns)
                else:
                    df = pd.read_excel(file_path, usecols=selected_columns)

                connection = mysql.connector.connect(
                    host='localhost',
                    database='search_engine_new',
                    user='root',
                    password=''
                )
                cursor = connection.cursor()
                row_count = 0
                skipped_count = 0

                for index, row in df.iterrows():
                    if selected_columns[0]=='NULL':
                        full_name = None
                    else:    
                        full_name = row[selected_columns[0]]
                    if selected_columns[1]=='NULL':
                        medicare_number = None
                    else:
                        medicare_number = self.clean_string(row[selected_columns[1]])
                    if selected_columns[2]=='NULL':
                        payer = None
                    else:
                        payer = row[selected_columns[2]]
                    if selected_columns[3]=='NULL':
                        provider_name = None
                    else:
                        provider_name = row[selected_columns[3]]
                    if selected_columns[4]=='NULL':
                        insights_message = None
                    else:
                        insights_message = row[selected_columns[4]]
                    if selected_columns[5]=='NULL':
                        col_1 = None
                    else:
                        col_1 = row[selected_columns[5]]
                    if selected_columns[6]=='NULL':
                        col_2 = None
                    else:
                        col_2 = row[selected_columns[6]]

                    # Split full name into first name and last name
                    if pd.notnull(full_name):
                        names = full_name.split(',')
                        if len(names) == 2:
                            last_name = names[0].strip()
                            first_name = names[1].strip()
                        else:
                            names = full_name.split()
                            first_name = names[0]
                            last_name = ' '.join(names[1:]) if len(names) > 1 else None
                    else:
                        first_name = None
                        last_name = None
                    
                    # Handle NaN values
                    if pd.isnull(full_name):
                        full_name = None
                    if pd.isnull(medicare_number):
                        medicare_number = None
                    if pd.isnull(payer):
                        payer = None
                    if pd.isnull(provider_name):
                        provider_name = None
                    if pd.isnull(insights_message):
                        insights_message = None
                    if pd.isnull(col_1):
                        col_1 = None
                    if pd.isnull(col_2):
                        col_2 = None

                    query = (
                        "INSERT INTO raw (first_name, last_name, medicare_number, payer, provider_name, insights_message,col_1,col_2) "
                        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                    )
                    values = (
                        self.clean_string(first_name),
                        self.clean_string(last_name),
                        medicare_number,
                        payer,
                        provider_name,
                        insights_message,
                        col_1,
                        col_2,
                    )

                    try:
                        cursor.execute(query, values)
                        connection.commit()
                        row_count += 1
                    except mysql.connector.IntegrityError:
                        skipped_count += 1
                    except Exception:
                        skipped_count += 1

                cursor.close()
                connection.close()
                messagebox.showinfo("Success", f"Data imported successfully!\nRows inserted: {row_count}\nRows skipped: {skipped_count}")
                window.after(0, window.destroy)
            else:
                messagebox.showerror("Error", "Please select a file and columns to import.")

        except Exception as e:
            print(f"")
            
    def import_data_3(self, window):
        try:
            file_path = self.file_path_var.get()
            selected_columns = [self.dropdown_vars[db_col].get() for db_col in self.dropdown_vars if self.dropdown_vars[db_col].get()]

            if file_path and selected_columns:
                if file_path.endswith('.csv'):
                    df = pd.read_csv(file_path, usecols=selected_columns)
                else:
                    df = pd.read_excel(file_path, usecols=selected_columns)

                connection = mysql.connector.connect(
                    host='localhost',
                    database='search_engine_new',
                    user='root',
                    password=''
                )
                cursor = connection.cursor()
                row_count = 0
                update_count = 0
                update_count_checked = 0
                skipped_count = 0
                skipped_count_same_id = 0
                skipped_count_raw = 0

                for index, row in df.iterrows():
                    if selected_columns[0] == "NULL":
                        full_name = None
                    else:
                        full_name = row[selected_columns[0]]
                    if selected_columns[1] == "NULL":
                        dob = None
                    else:
                        dob = None
                        if row[selected_columns[2]] == '' or row[selected_columns[1]] is None:
                            dob = None
                        else:
                            dob = self.format_date_1(row[selected_columns[1]])
                    if selected_columns[2] == "NULL":
                        gender = None
                    else:
                        gender = row[selected_columns[2]]
                    if selected_columns[3] == "NULL":
                        address = None
                    else:
                        address = row[selected_columns[3]]
                    if selected_columns[4] == "NULL":
                        city = None
                    else:
                        city = row[selected_columns[4]]
                    if selected_columns[5] == "NULL":
                        state = None
                    else:
                        state = row[selected_columns[5]]
                    if selected_columns[6] == "NULL":
                        zip_code = None
                    else:
                        zip_code = row[selected_columns[6]]
                    if selected_columns[7] == "NULL":
                        active_date = None
                    else:
                        active_date = row[selected_columns[7]]
                    if selected_columns[8] == "NULL":
                        ins_name = None
                    else:
                        ins_name = row[selected_columns[8]]
                    if selected_columns[9] == "NULL":
                        ins_type = None
                    else:
                        ins_type = row[selected_columns[9]]
                    if selected_columns[10] == "NULL":
                        msp = None
                    else:
                        msp = row[selected_columns[10]]
                    try:
                        modify = selected_columns[11]
                    except IndexError:
                        modify = 0
                        
                    if pd.notnull(full_name):
                        names = full_name.split(',')
                        if len(names) == 2:
                            last_name = names[0].strip()
                            first_name_parts = names[1].strip().split()
                            if len(first_name_parts) >= 2:
                                first_name = ' '.join(first_name_parts[:-1])
                                medicare_number = first_name_parts[-1]
                                medicare_number = medicare_number.replace('(', '').replace(')', '')
                            else:
                                first_name = names[1].strip()
                                medicare_number = None
                        else:
                            names = full_name.split()
                            first_name = names[0]
                            last_name = ' '.join(names[1:]) if len(names) > 1 else None
                            medicare_number = None
                    else:
                        first_name = None
                        last_name = None
                        medicare_number = None

                    if first_name:
                        first_name = ' '.join([name for name in first_name.split() if len(name) > 1 or name.islower()])

                    if pd.notnull(zip_code) and '-' in str(zip_code):
                        zip_code = str(zip_code).split('-')[0]
                     
                    # Handle NaN values
                    if pd.isnull(first_name):
                        first_name = None
                    if pd.isnull(last_name):
                        last_name = None
                    if pd.isnull(dob):
                        dob = None
                    if pd.isnull(city):
                        city = None
                    if pd.isnull(address):
                        address = None
                    if pd.isnull(state):
                        state = None
                    if pd.isnull(zip_code):
                        zip_code = None
                    if pd.isnull(medicare_number):
                        medicare_number = None
                    if pd.isnull(ins_type):
                        ins_type = None
                    if pd.isnull(ins_name):
                        ins_name = None
                    if pd.isnull(msp):
                        msp = None
                    if(modify==1):
                        query_check = "SELECT COUNT(*) FROM checked WHERE medicare_number = %s"
                        cursor.execute(query_check, (medicare_number,))
                        result = cursor.fetchone()
                            
                        if result and result[0] > 0:
                            delete_query = "DELETE FROM checked WHERE medicare_number = %s"
                            cursor.execute(delete_query, (medicare_number,))
                            update_count = cursor.rowcount
                            update_count_checked += update_count
                            
                    # Check if medicare_number already exists in raw table
                    query_check = "SELECT COUNT(*) FROM raw WHERE medicare_number = %s"
                    cursor.execute(query_check, (medicare_number,))
                    result = cursor.fetchone()
                    
                    if result and result[0] > 0:
                        delete_query = "DELETE FROM raw WHERE medicare_number = %s"
                        cursor.execute(delete_query, (medicare_number,))
                        deleted_count = cursor.rowcount
                        skipped_count_raw += deleted_count
                        # continue  # Skip insertion if medicare_number already exists in raw table
                    query = (
                        "INSERT INTO checked (first_name, last_name, medicare_number, dob, gender, address, city, state, zip, ins_name, ins_type,active_date,msp) "
                        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    )
                    values = (
                        self.clean_string(first_name),
                        self.clean_string(last_name),
                        medicare_number,
                        dob,
                        gender,
                        address,
                        city,
                        state,
                        zip_code,
                        ins_name,
                        ins_type,
                        self.format_date_1(active_date),
                        msp
                        
                    )

                    try:
                        cursor.execute(query, values)
                        connection.commit()
                        row_count += 1
                    except mysql.connector.IntegrityError:
                        skipped_count_same_id += 1
                    except Exception:
                        skipped_count += 1

                cursor.close()
                connection.close()
                messagebox.showinfo("Success", f"Data imported successfully!\nRows inserted: {row_count}\nRows skipped: {skipped_count}\nRows Deleted (Raw Check): {skipped_count_raw}\nRows Updated : {update_count_checked}\nRows Already Exist : {skipped_count_same_id}")
                window.after(0, window.destroy)
            else:
                messagebox.showerror("Error", "Please select a file and columns to import.")

        except Exception as e:
            print(f"")
            
    def extract_first_last_name(self,full_name):
        first_name = None
        last_name = None
        
        if pd.notnull(full_name):
            # Split by comma to handle cases like "Last Name, First Name(s)"
            names = full_name.split(',')
            if len(names) == 2:
                last_name = names[0].strip()
                first_name = names[1].strip()
            else:
                # Split by spaces to handle cases like "First Name Middle Initials Last Name"
                names = full_name.split()
                first_name = names[0]
                # Identify parts that belong to the last name
                last_name_parts = []
                for part in names[1:]:
                    if len(part) <= 2 and part.isalpha():
                        continue  # Skip initials or abbreviations
                    last_name_parts.append(part)
                last_name = ' '.join(last_name_parts)

        return first_name, last_name
            
    def import_data_4(self, window):
        try:
            file_path = self.file_path_var.get()
            selected_columns = [self.dropdown_vars[db_col].get() for db_col in self.dropdown_vars if self.dropdown_vars[db_col].get()]

            if file_path and selected_columns:
                if file_path.endswith('.csv'):
                    df = pd.read_csv(file_path, usecols=selected_columns)
                else:
                    df = pd.read_excel(file_path, usecols=selected_columns)

                connection = mysql.connector.connect(
                    host='localhost',
                    database='search_engine_new',
                    user='root',
                    password=''
                )
                cursor = connection.cursor()
                row_count = 0
                update_count = 0
                update_count_checked = 0
                skipped_count = 0
                skipped_count_same_id = 0
                skipped_count_raw = 0

                for index, row in df.iterrows():
                    if selected_columns[0] == "NULL":
                        full_name = None
                    else:
                        full_name = row[selected_columns[0]]
                    if selected_columns[1] == "NULL":
                        medicare_number = None
                    else:
                        medicare_number = (row[selected_columns[1]])
                    if selected_columns[2] == "NULL":
                        dob = None
                    else:
                        dob = None
                        if row[selected_columns[2]] == '' or row[selected_columns[2]] is None:
                            dob = None
                        else:
                            dob = self.format_date_1(row[selected_columns[2]])
                    if selected_columns[3] == "NULL":
                        gender_code = None
                    else:
                        gender_code = row[selected_columns[3]]
                    if selected_columns[4] == "NULL":
                        address = None
                    else:
                        address = row[selected_columns[4]]
                    if selected_columns[5] == "NULL":
                        payer = None
                    else:
                        payer = row[selected_columns[5]]
                    if selected_columns[6] == "NULL":
                        plan = None
                    else:
                        plan = row[selected_columns[6]]
                    if selected_columns[7] == "NULL":
                        ins_name = None
                    else:
                        ins_name = row[selected_columns[7]]
                    if selected_columns[8] == "NULL":
                        ins_type = None
                    else:
                        ins_type = row[selected_columns[8]]
                    if selected_columns[9] == "NULL":
                        msp = None
                    else:
                        msp = row[selected_columns[9]]
                    try:
                        modify = selected_columns[10]
                    except IndexError:
                        modify = 0

                    

                    
                    gender = 'Male' if gender_code == 'M' else 'Female' if gender_code == 'F' else None
                     
                    first_name, last_name = self.extract_first_last_name(full_name)
                    if first_name:
                        first_name = ' '.join([name for name in first_name.split() if len(name) > 1 or name.islower()])
                    # Handle NaN values
                    if pd.isnull(first_name):
                        first_name = None
                    if pd.isnull(last_name):
                        last_name = None
                    if pd.isnull(dob):
                        dob = None
                    if pd.isnull(address):
                        address = None
                    if pd.isnull(plan):
                        plan = None
                    if pd.isnull(medicare_number):
                        medicare_number = None
                    if pd.isnull(ins_type):
                        ins_type = None
                    if pd.isnull(ins_name):
                        ins_name = None
                    if pd.isnull(gender):
                        gender = None
                    if pd.isnull(payer):
                        payer = None    
                    if pd.isnull(msp):
                        msp = None    
                    
                    
                    if(modify==1):
                            query_check = "SELECT COUNT(*) FROM checked WHERE medicare_number = %s"
                            cursor.execute(query_check, (medicare_number,))
                            result = cursor.fetchone()
                            
                            if result and result[0] > 0:
                                delete_query = "DELETE FROM checked WHERE medicare_number = %s"
                                cursor.execute(delete_query, (medicare_number,))
                                update_count = cursor.rowcount
                                update_count_checked += update_count
                                # continue 
                            
                    query_check = "SELECT COUNT(*) FROM raw WHERE medicare_number = %s"
                    cursor.execute(query_check, (medicare_number,))
                    result = cursor.fetchone()
                    
                    if result and result[0] > 0:
                        delete_query = "DELETE FROM raw WHERE medicare_number = %s"
                        cursor.execute(delete_query, (medicare_number,))
                        deleted_count = cursor.rowcount
                        skipped_count_raw += deleted_count
                        continue  
                          
                    query = (
                        "INSERT INTO checked (first_name, last_name, medicare_number, dob, gender, address, payer, plan, ins_name, ins_type,msp) "
                        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    )
                    values = (
                        self.clean_string(first_name),
                        self.clean_string(last_name),
                        medicare_number,
                        dob,
                        gender,
                        address,
                        payer,
                        plan,
                        ins_name,
                        ins_type,
                        msp
                    )

                    try:
                        cursor.execute(query, values)
                        connection.commit()
                        row_count += 1
                    except mysql.connector.IntegrityError as ie:
                        print(f"IntegrityError occurred while inserting data: {ie}")
                        # skipped_count += 1
                        skipped_count_same_id +=1
                    except Exception as e:
                        print(f"Error occurred while inserting data: {e}")
                        skipped_count += 1


                cursor.close()
                connection.close()
                messagebox.showinfo("Success", f"Data imported successfully!\nRows inserted: {row_count}\nRows skipped: {skipped_count}\nRows Deleted (Raw Check): {skipped_count_raw}\nRows Updated : {update_count_checked}\nRows Already Exist : {skipped_count_same_id}")
                window.after(0, window.destroy)
            else:
                messagebox.showerror("Error", "Please select a file and columns to import.")

        except Exception as e:
            print(f"")

    def import_data_5(self, window):
        try:
            file_path = self.file_path_var.get()
            selected_columns = [self.dropdown_vars[db_col].get() for db_col in self.dropdown_vars if self.dropdown_vars[db_col].get()]

            if file_path and selected_columns:
                if file_path.endswith('.csv'):
                    df = pd.read_csv(file_path, usecols=selected_columns)
                else:
                    df = pd.read_excel(file_path, usecols=selected_columns)

                connection = mysql.connector.connect(
                    host='localhost',
                    database='search_engine_new',
                    user='root',
                    password=''
                )
                cursor = connection.cursor()
                row_count = 0
                skipped_count_raw = 0
                skipped_count_checked = 0

                for index, row in df.iterrows():
                    if selected_columns[0] == "NULL":
                        full_name =None
                    else:
                        full_name = row[selected_columns[0]]
                    if selected_columns[1] == "NULL":
                        medicare_number =None
                    else:
                        medicare_number = row[selected_columns[1]]
                    if selected_columns[2] == "NULL":
                        dob =None
                    else:
                        dob = None
                        if row[selected_columns[2]] == '' or row[selected_columns[2]] is None:
                            dob = None
                        else:
                            dob = self.format_date_1(row[selected_columns[2]])
                            
                    if selected_columns[3] == "NULL":
                        age =None
                    else:
                        age = row[selected_columns[3]]
                    if selected_columns[4] == "NULL":
                        gender =None
                    else:
                        gender = row[selected_columns[4]]
                    if selected_columns[5] == "NULL":
                        address =None
                    else:
                        address = row[selected_columns[5]]
                    if selected_columns[6] == "NULL":
                        phone =None
                    else:
                        phone = self.clean_numbers(row[selected_columns[6]])
                    if selected_columns[7] == "NULL":
                        alternate_number_landline =None
                    else:
                        alternate_number_landline = self.clean_numbers(row[selected_columns[7]])
                    if selected_columns[8] == "NULL":
                        month_year =None
                    else:
                        month_year =row[selected_columns[8]]
                    if selected_columns[9] == "NULL":
                        dr_name =None
                    else:
                        dr_name = row[selected_columns[9]]
                    if selected_columns[10] == "NULL":
                        dr_npi =None
                    else:
                        dr_npi = row[selected_columns[10]]
                    if selected_columns[11] == "NULL":
                        client =None
                    else:
                        client = row[selected_columns[11]]
                    

                    first_name, last_name = self.extract_first_last_name(full_name)
                    if first_name:
                        first_name = ' '.join([name for name in first_name.split() if len(name) > 1 or name.islower()])
                    # Handle NaN values
                    if pd.isnull(first_name):
                        first_name = None
                    if pd.isnull(last_name):
                        last_name = None
                    if pd.isnull(dob):
                        dob = None
                    if pd.isnull(address):
                        address = None
                    if pd.isnull(client):
                        client = None
                    if pd.isnull(dr_npi):
                        dr_npi = None
                    if pd.isnull(medicare_number):
                        medicare_number = None
                    if pd.isnull(dr_name):
                        dr_name = None
                    if pd.isnull(month_year):
                        month_year = None
                    if pd.isnull(alternate_number_landline):
                        alternate_number_landline = None
                    if pd.isnull(phone):
                        phone = None
                    if pd.isnull(gender):
                        gender = None
                    # Check if medicare_number already exists in raw or checked table
                    query_check_raw = "SELECT COUNT(*) FROM raw WHERE medicare_number = %s"
                    cursor.execute(query_check_raw, (medicare_number,))
                    result_raw = cursor.fetchone()

                    query_check_checked = "SELECT COUNT(*) FROM checked WHERE medicare_number = %s"
                    cursor.execute(query_check_checked, (medicare_number,))
                    result_checked = cursor.fetchone()

                    if result_raw and result_raw[0] > 0:
                        skipped_count_raw += 1
                        # continue

                    if result_checked and result_checked[0] > 0:
                        skipped_count_checked += 1
                        # continue
                    # print(medicare_number)
                    # Prepare INSERT query
                    query = (
                        "INSERT INTO complete (full_name, first_name, last_name, medicare_number, dob, gender, address, phone, age, alternate_number_landline, dr_name, dr_npi,client,month_year) "
                        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    )
                    values = (
                        self.clean_string(full_name),
                        self.clean_string(first_name),
                        self.clean_string(last_name),
                        medicare_number,
                        dob,
                        gender,
                        address,
                        phone,
                        age,
                        alternate_number_landline,
                        self.clean_string(dr_name),
                        dr_npi,
                        client,
                        month_year
                    )

                    try:
                        cursor.execute(query, values)
                        connection.commit()
                        row_count += 1
                    except mysql.connector.Error as err:
                        print(f"Error occurred while inserting data: {err}")
                        connection.rollback()
                    except Exception as e:
                        print(f"Unknown error occurred while inserting data: {e}")

                cursor.close()
                connection.close()
                messagebox.showinfo("Success", f"Data imported successfully!\nRows inserted: {row_count}\nRows skipped (Raw Check): {skipped_count_raw}\nRows skipped (Checked Check): {skipped_count_checked}")
                window.after(0, window.destroy)
            else:
                messagebox.showerror("Error", "Please select a file and columns to import.")

        except Exception as e:
            print(f"")
    
    def import_data_d5(self, window):
            try:
                file_path = self.file_path_var.get()
                selected_columns = [self.dropdown_vars[db_col].get() for db_col in self.dropdown_vars if self.dropdown_vars[db_col].get()]

                if file_path and selected_columns:
                    df = pd.read_excel(file_path)

                    connection = mysql.connector.connect(
                        host='localhost',
                        database='search_engine_new',
                        user='root',
                        password=''
                    )
                    cursor = connection.cursor()
                    row_count = 0
                    skipped_count = 0
                    skipped_count_raw = 0
                    skipped_count_checked = 0

                    for index, row in df.iterrows():
                        full_name = row[selected_columns[0]]
                        medicare_number = (row[selected_columns[1]])
                        dob = None
                        if row[selected_columns[2]] == '' or row[selected_columns[2]] is None:
                            dob = None
                        else:
                            dob = self.format_date_1(row[selected_columns[2]])
                        age = row[selected_columns[3]]
                        gender = row[selected_columns[4]]
                        address = row[selected_columns[5]]
                        month_year = row[selected_columns[6]]
                        dr_name = row[selected_columns[7]]
                        phone = row[selected_columns[8]]
                        alternative_no = row[selected_columns[9]]
                        dr_npi = row[selected_columns[10]]
                       
                        # Handle NaN values
                        if pd.isnull(full_name):
                            full_name = None
                        if pd.isnull(medicare_number):
                            medicare_number = None
                        if pd.isnull(dob):
                            dob = None
                        if pd.isnull(gender):
                            gender = None
                        if pd.isnull(address):
                            address = None
  

                        first_name, last_name = self.extract_first_last_name(full_name)
                        if first_name:
                            first_name = ' '.join([name for name in first_name.split() if len(name) > 1 or name.islower()])
                            
                        query_check = "SELECT COUNT(*) FROM raw WHERE medicare_number = %s"
                        cursor.execute(query_check, (medicare_number,))
                        result = cursor.fetchone()
                        
                        if result and result[0] > 0:
                            skipped_count_raw += 1
                            continue 
                        
                        query_check = "SELECT COUNT(*) FROM checked WHERE medicare_number = %s"
                        cursor.execute(query_check, (medicare_number,))
                        result = cursor.fetchone()
                        
                        if result and result[0] > 0:
                            skipped_count_checked += 1
                            continue  
                             
                        query = (
                            "INSERT INTO checked (full_name,first_name, last_name, medicare_number, dob, gender, address, phone, age, 	alternate_number_landline, dr_aame,	dr_npi) "
                            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                        )
                        values = (
                            self.clean_string(first_name),
                            self.clean_string(last_name),
                            self.clean_string(medicare_number),
                            dob,
                            gender,
                            address,
                            payer,
                            plan,
                            ins_name,
                            ins_type
                        )

                        try:
                            cursor.execute(query, values)
                            connection.commit()
                            row_count += 1
                        except mysql.connector.IntegrityError as ie:
                            print(f"IntegrityError occurred while inserting data: {ie}")
                            skipped_count += 1
                        except Exception as e:
                            print(f"Error occurred while inserting data: {e}")
                            skipped_count += 1


                    cursor.close()
                    connection.close()
                    messagebox.showinfo("Success", f"Data imported successfully!\nRows inserted: {row_count}\nRows skipped: {skipped_count}\nRows skipped (Raw Check): {skipped_count_raw}\nRows skipped (Checked Check): {skipped_count_checked}")
                    window.after(0, window.destroy)
                else:
                    messagebox.showerror("Error", "Please select a file and columns to import.")

            except Exception as e:
                print(f"")

    def import_data_old(self):
        try:
            file_path = self.file_path_var.get()
            selected_columns = [self.dropdown_vars[db_col].get() for db_col in self.dropdown_vars if self.dropdown_vars[db_col].get()]
            
            if file_path and selected_columns:
                df = pd.read_excel(file_path)
                
                # Clean and format data
                for col in selected_columns:
                    if col in df.columns:
                        if col == 'dob':  # Example formatting for date column
                            df[col] = df[col].apply(self.format_date)
                        else:
                            df[col] = df[col].apply(self.clean_string)
                
                # Example: Connecting to MySQL and inserting data
                connection = mysql.connector.connect(host='localhost', database='search_engine_new', user='root', password='')
                cursor = connection.cursor()

                for index, row in df.iterrows():
                    query = "INSERT INTO raw ({}) VALUES ({})".format(','.join(selected_columns), ','.join(['%s']*len(selected_columns)))
                    cursor.execute(query, tuple(row[col] for col in selected_columns))
                    connection.commit()

                cursor.close()
                connection.close()
                print("Data imported successfully!")
            else:
                print("Please select a file and columns to import.")

        except Exception as e:
            print(f"Error importing data: {e}")
            
    def format_date__old(self, date):
        try:
            if pd.notnull(date):
                if isinstance(date, datetime):
                    parsed_date = date
                else:
                    parsed_date = datetime.strptime(date, '%m/%d/%Y')
                formatted_date = parsed_date.strftime('%Y-%m-%d')
                return formatted_date
            else:
                return None
        except ValueError:
            return None
    def format_date_1(self, date):
        try:
            if date:
                if pd.isna(date):
                    return None
                if isinstance(date, datetime):
                    try:
                        return date.strftime('%Y-%m-%d')
                    except Exception as e:
                        return None
                    
                elif isinstance(date, (int, float)):  # Handle float or int case (timestamp)
                    parsed_date = datetime.fromtimestamp(date)
                else:
                    # Define multiple date formats to try parsing
                    formats_to_try = [
                        '%m/%d/%Y', '%m-%d-%Y', '%Y-%m-%d',  # Standard formats
                        '%d/%m/%Y', '%d-%m-%Y', '%Y-%d-%m',  # European formats
                        '%Y/%m/%d', '%Y-%m-%d',              # ISO formats
                        '%m/%d/%y', '%m-%d-%y', '%y-%m-%d',  # Short year formats
                        '%d/%m/%y', '%d-%m-%y', '%y-%d-%m',  # Short year European formats
                        '%Y/%m/%d %H:%M:%S', '%Y-%m-%d %H:%M:%S',  # ISO datetime formats
                        '%m/%d/%Y %H:%M:%S', '%m-%d-%Y %H:%M:%S',  # Datetime formats with time
                        '%d/%m/%Y %H:%M:%S', '%d-%m-%Y %H:%M:%S',  # European datetime formats
                    ]
                    
                    parsed_date = None
                    for fmt in formats_to_try:
                        try:
                            parsed_date = datetime.strptime(str(date), fmt)
                            break  # Exit loop if successfully parsed
                        except ValueError:
                            continue  # Continue to next format if current one fails
                    
                    if parsed_date is None:
                        return None  # Return None if all formats fail
            else:
                return None
        
        except Exception as e:
            print(f"Error in format_date_1: {e}")
            return None
        
        formatted_date = parsed_date.strftime('%Y-%m-%d')
        return formatted_date
        
if __name__ == "__main__":
    app = DBMSApp()
    app.mainloop()

