import tkinter as tk
from tkinter import ttk, filedialog
import pandas as pd
import mysql.connector
from datetime import datetime
import re
from tkinter import Tk, ttk, StringVar, messagebox

class DBMSApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("DBMS")
        self.configure(bg="#e0e0e0")
        self.geometry("800x400")
        
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

    def custom_function1(self, window):
        window.title("Raw Checker 1")
        window.geometry("700x550")
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
        window.geometry("700x380")
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
            ("Insights Message", "insights_message")
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
        window.geometry("700x380")
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
        ]

        for i, (label_text, db_column) in enumerate(columns):
            label = ttk.Label(dropdown_frame, text=label_text)
            label.grid(row=i, column=0, padx=10, pady=10, sticky='w')

            self.dropdown_vars[db_column] = tk.StringVar()
            dropdown = ttk.Combobox(dropdown_frame, textvariable=self.dropdown_vars[db_column], state='disabled', width=30)
            dropdown.grid(row=i, column=1, padx=10, pady=10)
            self.dropdowns.append(dropdown)

        import_button = ttk.Button(dropdown_frame, text="Import Data", command=self.import_data)
        import_button.grid(row=len(columns), column=1, padx=10, pady=10)

    def custom_function5(self, window):
        window.title("Checked Checker 2")
        window.geometry("700x380")
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
            ("Plan", "plan"),
            ("Payer", "payer"),
            ("Insights Message", "insight_message"),
            ("Provider Name", "provider_message"),
            ("Medicare Number(MBI)", "medicare_number")
        ]

        for i, (label_text, db_column) in enumerate(columns):
            label = ttk.Label(dropdown_frame, text=label_text)
            label.grid(row=i, column=0, padx=10, pady=10, sticky='w')

            self.dropdown_vars[db_column] = tk.StringVar()
            dropdown = ttk.Combobox(dropdown_frame, textvariable=self.dropdown_vars[db_column], state='disabled', width=30)
            dropdown.grid(row=i, column=1, padx=10, pady=10)
            self.dropdowns.append(dropdown)

        import_button = ttk.Button(dropdown_frame, text="Import Data", command=self.import_data)
        import_button.grid(row=len(columns), column=1, padx=10, pady=10)

    def custom_function6(self, window):
        label = ttk.Label(window, text="Custom Function 6", style='TLabel')
        label.pack(expand=True)

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls")])
        if file_path:
            self.file_path_var.set(file_path)
            self.load_dropdowns(file_path)

    def load_dropdowns(self, file_path):
        try:
            df = pd.read_excel(file_path)
            headers = df.columns.tolist()

            for dropdown in self.dropdowns:
                dropdown['values'] = headers
                dropdown.config(state='readonly')

        except Exception as e:
            print(f"Error loading file: {e}")
            for dropdown in self.dropdowns:
                dropdown.config(state='disabled')

    def format_date(self, date):
        try:
            if pd.notnull(date):
                parsed_date = datetime.strptime(date, '%m/%d/%Y')
                formatted_date = parsed_date.strftime('%Y-%m-%d')  
                return formatted_date
            else:
                return None
        except ValueError:
            return None

    def clean_string(self, text):
        if isinstance(text, str):
            cleaned_text = re.sub(r'[^\w\s-]', '', text)  
            return cleaned_text.strip()
        else:
            return None
        
    def import_data(self, window):
        try:
            file_path = self.file_path_var.get()
            selected_columns = [self.dropdown_vars[db_col].get() for db_col in self.dropdown_vars if self.dropdown_vars[db_col].get()]
            
            if file_path and selected_columns:
                df = pd.read_excel(file_path)
                
                connection = mysql.connector.connect(host='localhost', database='search_engine_new', user='root', password='')
                cursor = connection.cursor()
                row_count = 0
                skipped_count= 0
                for index, row in df.iterrows():
                    query = "INSERT INTO raw (first_name, last_name, dob, address, city, state, zip, medicare_number) " \
                            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                            
                    values = (
                        self.clean_string(row[selected_columns[0]]),
                        self.clean_string(row[selected_columns[1]]),
                        self.format_date(row[selected_columns[2]]),
                        row[selected_columns[3]],
                        row[selected_columns[4]],
                        row[selected_columns[5]],
                        row[selected_columns[6]],
                        self.clean_string(row[selected_columns[7]])
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
            print(f"Error importing data: {e}")

    def import_data_1(self, window):
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

                for index, row in df.iterrows():
                    full_name = row[selected_columns[0]]
                    dob = self.format_date_1(row[selected_columns[1]])
                    state = row[selected_columns[2]]
                    medicare_number = self.clean_string(row[selected_columns[3]])

                    if pd.notnull(full_name):
                        names = full_name.split()
                        first_name = names[0]
                        last_name = ' '.join(names[1:]) if len(names) > 1 else None
                    else:
                        first_name = None
                        last_name = None

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
            messagebox.showerror("Error", f"Error importing data: {e}")
            print(e)
            
    def import_data_2(self, window):
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

                for index, row in df.iterrows():
                    full_name = row[selected_columns[0]]
                    medicare_number = self.clean_string(row[selected_columns[1]])
                    payer = row[selected_columns[2]]
                    provider_name = row[selected_columns[3]]
                    insights_message = row[selected_columns[4]]

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

                    query = (
                        "INSERT INTO raw (first_name, last_name, medicare_number, payer, provider_name, insights_message) "
                        "VALUES (%s, %s, %s, %s, %s, %s)"
                    )
                    values = (
                        self.clean_string(first_name),
                        self.clean_string(last_name),
                        medicare_number,
                        payer,
                        provider_name,
                        insights_message
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
            messagebox.showerror("Error", f"Error importing data: {e}")
            print(e)



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
            
    def format_date_1(self, date):
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
if __name__ == "__main__":
    app = DBMSApp()
    app.mainloop()
