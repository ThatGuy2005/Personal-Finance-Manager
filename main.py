import sys

from PyQt6.QtWidgets import QComboBox
from PyQt6.QtWidgets import QApplication, QMainWindow, QLineEdit
from PyQt6.QtWidgets import QPushButton, QLabel

import argon2

from shapes import Rectangle
from my_gui import Page
from window_settings import Settings
import server_communication as sc
import creating_widgets as cw
from windows import Window, WindowManager, InsertSavingWindow, InsertBudgetWindow, InsertTransactionWindow,InsertRecurringPayment
from windows import UpdateBalanceWindow, InsertAccountWindow, AdminWindow, InsertLoanWindow
import helper_functions as hf

import os
from dotenv import load_dotenv

# Initialize Argon2id hasher with standard parameters
ph = argon2.PasswordHasher(
    time_cost=2,        # Iterations
    memory_cost=19456,  # 19 MiB memory cost
    parallelism=1,      # Threads
    hash_len=32,
    type=argon2.Type.ID
)

load_dotenv()
connection_string = (
    f"Driver={os.getenv('DB_DRIVER')};"
    f"Server={os.getenv('DB_SERVER')};"
    f"Database={os.getenv('DB_NAME')};"
    f"Trusted_Connection={os.getenv('DB_TRUSTED_CONNECTION')};"
    f"TrustServerCertificate={os.getenv('DB_TRUST_SERVER_CERTIFICATE')};"
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # The settings used for the app
        self.setting = Settings()

        # List that manages accounts
        self.accounts = list()

        # The window has the same size as the screen
        self.setGeometry(self.setting.get_screen_size())

        # Some rectangles and design elements
        self.button = QPushButton(self)
        self.rec = Rectangle(self,x=0,y=0,
                             w=self.setting.width//4,h=self.setting.height)
        self.app_name = QLabel(self,text="Welcome to Problem\nManager")

        # Sign in page
        self.sign_up_page = Page(self)

        # Log in page
        self.log_in_page = Page(self)

        # Button for showing and hiding pages
        self.turn_page = QPushButton(self, text="Log In")

        # A warm welcome label
        self.welcome = QLabel(self)
        self.welcome.hide()

        # Put the widgets to the right place
        self.initUI()
        
        self.win_manager = WindowManager()

        # Accounts window
        self.account_window = Window(self)
        self.win_manager.add_window("account_window",self.account_window)

        # Recurring payments window
        self.recurring_payments_window = Window(self)
        self.win_manager.add_window("recurring_payments_window",self.recurring_payments_window)

        # Transactions window
        self.transactions_window = Window(self)
        self.win_manager.add_window("transactions_window",self.transactions_window)

        # Loan window
        self.loans_window = Window(self)
        self.win_manager.add_window("loans_window",self.loans_window)

        # Budget window
        self.budgets_window = Window(self)
        self.win_manager.add_window("budgets_window",self.budgets_window)

        # Saving window
        self.savings_window = Window(self)
        self.win_manager.add_window("savings_window",self.savings_window)

    def initUI(self):

        # Sign up page -------------------------------------------

        self.sign_up_page.setGeometry(self.setting.get_centerx(),
                                      self.setting.get_top() + self.setting.margin,
                                      self.setting.page_width,
                                      self.setting.page_height)
        self.sign_up_page.add_title("Sign Up",25)
        self.sign_up_page.add_empty_line_horizontal()
        self.sign_up_page.add_input_boxes(Name=QLineEdit(self))
        self.sign_up_page.add_input_boxes(Email=QLineEdit(self))
        self.sign_up_page.add_input_boxes(Password=QLineEdit(self))

        # Log in page -------------------------------------------

        self.log_in_page.setGeometry(self.setting.get_centerx(),
                                      self.setting.get_top() + self.setting.margin,
                                      self.setting.page_width,
                                      self.setting.page_height)
        self.log_in_page.add_title("Log In",25)
        self.log_in_page.add_empty_line_horizontal()
        self.log_in_page.add_input_boxes(Name=QLineEdit(self))
        self.log_in_page.add_input_boxes(Email=QLineEdit(self))
        self.log_in_page.add_input_boxes(Password=QLineEdit(self))
        self.log_in_page.hide()

        # General Design ----------------------------------------

        self.app_name.setGeometry(30, 10, 300, 100)
        self.app_name.setStyleSheet("font-size: 25px;")

        self.button.setGeometry(self.setting.get_right()-2*self.setting.button_width, 
                                self.setting.get_bottom()-self.setting.button_height, 
                                self.setting.button_width,
                                self.setting.button_height)
        self.button.setText("Submit")
        self.button.setStyleSheet("font-size: 21px;""font-family: Mono")
        self.button.clicked.connect(self.submit)

        self.rec.setGeometry(0, 0, self.setting.width//4, self.setting.height)

        #--------------------------------------------------------

        self.turn_page.setStyleSheet("font-size: 21px;")

        self.turn_page.setGeometry(self.setting.get_right()-self.setting.button_width,
                                   self.setting.get_bottom()-self.setting.button_height,
                                   self.setting.button_width,
                                   self.setting.button_height)
        
        self.turn_page.clicked.connect(self.turn)
        
    
    def submit(self):
        n = self.log_in_page.text_from_box("Name")
        e = self.log_in_page.text_from_box("Email")
        p = self.log_in_page.text_from_box("Password")

        if not self.sign_up_page.isHidden():
            sc.connect_and_execute("EXEC SignUpUser @NAME=?, @EMAIL=?, @PASSWORD_HASH=?",
                            n, e, ph.hash(p))
        else:
            hash_list = sc.connect_and_execute("EXEC GetHash @EMAIL=?", e)

            if not hash_list or not hash_list[0] or not hash_list[0][0]:
                self.load_login_error()
                return

            if hash_list :
                hash_ = hash_list[0][0]

            try:
                ph.verify(hash_,p)
                self.load_user_page(n, e)
            except argon2.exceptions.VerifyMismatchError:
                self.load_login_error()
            except argon2.exceptions.VerificationError:
                self.load_login_error()
            except Exception:
                self.load_login_error()

    def state(self):
        win = AdminWindow(self.setting,parent=self)
        win.show()


    def turn(self):
        if self.turn_page.text() == "Log In":
            self.turn_page.setText("Sign Up")
            self.sign_up_page.hide()
            self.log_in_page.show()
            
        else:
            self.turn_page.setText("Log In")
            self.sign_up_page.show()
            self.log_in_page.hide()

    def load_user_page(self, name:str, email:str):
        """If the login is successful, then load the user's main page."""
        self.sign_up_page.hide()
        self.log_in_page.hide()
        self.button.hide()
        self.turn_page.hide()
        self.email = email

        role = int(sc.connect_and_execute("EXEC GetRole @EMAIL=?",email)[0][0])

        if role > 1:
            self.state()
            return

        self.welcome.setGeometry(400,50,500,100)
        self.welcome.setStyleSheet("font-size: 40px;")
        self.welcome.setText("Welcome " + name)
        self.welcome.show()

        self.load_accounts()

    def load_login_error(self):
        """Adds a label to the login page with an error message."""
        if not self.log_in_page.label_already_exists("Error"):
            self.log_in_page.add_label(name="Error", 
                                   label=QLabel(text="Invalid credentials!"))

    def load_accounts(self):
        add_btn = QPushButton("Add Account")
        add_btn.clicked.connect(self.open_add_account_view)

        update_btn = QPushButton("Update Balance")
        update_btn.clicked.connect(self.open_update_account_view)

        # Reuses the standard load_window pipeline
        self.load_window(
            "account_window",
            "EXEC GetAccounts @EMAIL=?",
            cw.create_account,
            add_button=add_btn,
            update_button=update_btn
        )   

    def load_recurring_payments(self):

            add_btn = QPushButton("Add Recuring Payment")
            add_btn.clicked.connect(lambda: self.open_add_recurring_payments_view())

            del_btn = QPushButton("Delete Recurring Payment")
            # assumes view includes RECURRING_PAYMENT_ID as a returned column
            cmd = "DELETE FROM RecurringPayments WHERE ACCOUNT_ID=? AND COMPANY_NAME=? AND PRICE=?"
            del_btn.clicked.connect(lambda: self.call_delete_on_window(cmd,"recurring_payments_window"))

            self.load_window("recurring_payments_window",
                         "EXEC GetRecurringPayments @EMAIL=?",
                         cw.create_recurring_payment, add_button=add_btn, delete_button=del_btn)

    def load_budgets(self):
        
            add_btn = QPushButton("Add Budget")
            add_btn.clicked.connect(lambda: self.open_add_budget_view())

            update_btn = QPushButton("Update Budget")
            update_btn.clicked.connect(self.open_update_budget_view)

            del_btn = QPushButton("Delete Budget")
            # assumes view includes BUDGET_ID as a returned column
            cmd = "DELETE FROM Budgets WHERE ACCOUNT_ID=? AND BALANCE=? AND PERIOD_BEGIN=? AND PERIOD_END=?"
            del_btn.clicked.connect(lambda: self.call_delete_on_window(cmd,"budgets_window"))

            self.load_window("budgets_window",
                         "EXEC GetBudgets @EMAIL=?",
                         cw.create_budget, add_button=add_btn, delete_button=del_btn, update_button=update_btn)

    def open_update_budget_view(self):
        selected = self.win_manager.current_windows["budgets_window"].delete_checked()
        if len(selected) != 1:
            return
        self.selected_budget = selected[0]
        # reuse UpdateBalanceWindow which asks for a single BALANCE field
        self.update_budget_popup = UpdateBalanceWindow(self, self.submit_update_budget_balance)
        self.update_budget_popup.show()

    def submit_update_budget_balance(self, fields):
        data = self.gather_form_values(fields)
        selected = self.selected_budget
        if not selected or len(selected) == 0:
            return
        pk = selected[0]
        sc.connect_and_delete(
            "UPDATE Budgets SET BALANCE=? WHERE BUDGET_ID=?",
            data["BALANCE"],
            pk
        )
        self.update_budget_popup.close()
        self.win_manager.built_windows["budgets_window"] = False
        self.load_budgets()

    def load_savings(self):
            # Create your dynamic Add Button context hook
            add_btn = QPushButton("Add Saving")
            
            add_btn.clicked.connect(lambda: self.open_add_saving_view())

            update_btn = QPushButton("Update Balance")
            update_btn.clicked.connect(lambda: self.open_update_saving_balance_view())

            del_btn = QPushButton("Delete Saving")

            cmd = "DELETE FROM SavingPlans WHERE ACCOUNT_ID=? AND BUDGET=? AND YIELD=?"

            del_btn.clicked.connect(lambda: self.call_delete_on_window(cmd,"savings_window"))
            
            self.load_window("savings_window",
                             "EXEC GetSavings @EMAIL=?",
                             cw.create_saving, 
                             add_button=add_btn, delete_button=del_btn, update_button=update_btn)   

    def open_update_saving_balance_view(self):
        selected = self.win_manager.current_windows["savings_window"].delete_checked()
        if len(selected) != 1:
            return
        self.selected_saving = selected[0]
        self.update_popup = UpdateBalanceWindow(self, self.submit_update_saving_balance)
        self.update_popup.show()

    def submit_update_saving_balance(self, fields):
        data = self.gather_form_values(fields)
        selected = self.selected_saving
        if not selected:
            return

        account_id = self._resolve_account_id(selected)
        if account_id is None:
            print("Could not resolve Account ID for the selected saving.")
            return  

        try:
            new_balance = float(data["BALANCE"])
            yield_val = float(selected[0])
            old_budget = float(selected[1])
        except (ValueError, TypeError, IndexError) as e:
            print(f"Error parsing savings values: {e}")
            return

        sc.connect_and_delete(
            "UPDATE SavingPlans SET BUDGET=? WHERE ACCOUNT_ID=? AND YIELD=? AND BUDGET=?",
            new_balance,
            account_id,
            old_budget,
            yield_val
        )

        self.update_popup.close()
        
        self.load_savings()

    def _resolve_account_id(self, item):
        """Fetches Account ID if currency string is present in parameters."""
        res = sc.get_currency_options()
        currencies = set(t[1] for t in res)
    
        # Check if any element in item matches a known currency
        matched = currencies.intersection(set(map(str, item)))
        if not matched:
            return None  # Item doesn't use currency-based account lookup

        currency = list(matched)[0]
        result = sc.connect_and_execute(
            "EXEC GetAccountID @EMAIL=?, @CURRENCY=?", 
            self.email, 
            currency
        )
        if result and result[0][0] is not None:
            return int(result[0][0])
        return None

    def call_delete_on_window(self, command, window_name):
        window = self.win_manager.current_windows.get(window_name)
        if not window:
            return

        to_delete = window.delete_checked()
        if not to_delete:
            return

        for item in to_delete:
            if not item:
                continue

        # Dynamically attach acc_id if needed, filtering out the currency string
        acc_id = self._resolve_account_id(item)
        
        if acc_id is not None:
            # Strip currency string and prepend acc_id
            res = sc.get_currency_options()
            currencies = set(t[1] for t in res)
            clean_params = [acc_id] + [hf.to_float(x) for x in item if str(x) not in currencies]
        else:
            clean_params = item

        print("Clean params:",clean_params)

        try:
            sc.connect_and_delete(command, clean_params)
        except Exception as e:
            print(f"Deletion failed for {clean_params}: {e}")

    def open_add_account_view(self):
        all_currencies = sc.get_currency_options()
        print("Acc currency:",sc.get_account_currencies(self.email))
        used_currency_codes = (t[1] for t in sc.get_account_currencies(self.email))

        # Filter out options matching used currency codes (checking tuple index 1)
        available_currencies = [
            curr for curr in all_currencies if curr[1] not in used_currency_codes
        ]

        if not available_currencies:
            print("No remaining currencies available to create an account.")
            return

        purposes = sc.get_purpose_options()

        self.popup = InsertAccountWindow(self, available_currencies,purposes, self.submit_account_data)
        self.popup.show()

    def submit_account_data(self, fields):
        data = self.gather_form_values(fields)
        
        # Resolve USER_ID for the currently logged-in user
        user_res = sc.connect_and_execute("SELECT USER_ID FROM Users WHERE EMAIL=?", self.email)
        if not user_res or user_res[0][0] is None:
            print("Could not resolve USER_ID for email:", self.email)
            return

        user_id = user_res[0][0]
        purpose_id = data.get("PURPOSE_ID") 

        sql = """
            INSERT INTO Accounts (USER_ID, BALANCE, CURRENCY_ID, PURPOSE_ID) 
            VALUES (?, ?, ?, ?)
        """
        sc.connect_and_insert(
            sql, 
            user_id, 
            float(data["BALANCE"]), 
            data["CURRENCY_ID"], 
            purpose_id
        )

        self.popup.close()
        self.win_manager.built_windows["account_window"] = False
        self.load_accounts()

    def open_update_account_view(self):
        selected = self.win_manager.current_windows["account_window"].delete_checked()
        if not selected or len(selected) != 1:
            print("Please select exactly one account to update.")
            return

        self.selected_account = selected[0]
        self.update_account_popup = UpdateBalanceWindow(self, self.submit_update_account_balance)
        self.update_account_popup.show()

    def submit_update_account_balance(self, fields):
        data = self.gather_form_values(fields)
        selected = self.selected_account
        if not selected:
            return

        # Infer currency from selected widget payload to look up ACCOUNT_ID
        currency_code = str(selected[0]) if isinstance(selected, (list, tuple)) else str(selected)
        
        result = sc.connect_and_execute(
            "EXEC GetAccountID @EMAIL=?, @CURRENCY=?",
            self.email,
            currency_code
        )
        if not result or result[0][0] is None:
            print("Could not resolve Account ID for currency:", currency_code)
            return

        account_id = result[0][0]
        sc.connect_and_delete(
            "UPDATE Accounts SET BALANCE=? WHERE ACCOUNT_ID=?",
            float(data["BALANCE"]),
            account_id
        )

        self.update_account_popup.close()
        self.win_manager.built_windows["account_window"] = False
        self.load_accounts()

    def open_add_saving_view(self):
        accounts = sc.get_account_options(self.email)
        goals = sc.get_goal_options()
        self.popup = InsertSavingWindow(self, accounts, self.submit_saving_data, goals)
        self.popup.show()

    def open_add_recurring_payments_view(self):
        accounts = sc.get_account_options(self.email)
        subcategory = sc.get_subcategories()
        frequency = sc.get_frequencies()

        self.popup = InsertRecurringPayment(self, subcategory, accounts, 
                                            frequency, self.submit_recurring_payment_data)
        self.popup.show()

    def open_add_budget_view(self):
        accounts = sc.get_account_options(self.email)
        categories = sc.get_categories()
        self.popup = InsertBudgetWindow(self, accounts, self.submit_budget_data, categories)
        self.popup.show()

    def open_add_transaction_view(self):
        accounts = sc.get_account_options(self.email)
        subcategories = sc.get_subcategories()
        directions = sc.get_directions()
        self.popup = InsertTransactionWindow(self, accounts, self.submit_transaction_data,subcategories, directions)
        self.popup.show()

    def load_transactions(self):
        
            add_btn = QPushButton("Add Transaction")
            
            add_btn.clicked.connect(lambda: self.open_add_transaction_view())

            del_btn = QPushButton("Delete Transaction")
            cmd = "DELETE FROM Transactions WHERE ACCOUNT_ID=? AND TRANSACTION_TIME=? AND AMOUNT=?"
            del_btn.clicked.connect(lambda: self.call_delete_on_window(cmd,"transactions_window"))
            
            self.load_window("transactions_window",
                         "EXEC GetTransactions @EMAIL=?",
                         cw.create_transaction, add_button=add_btn, delete_button=del_btn) 

    def open_add_loan_view(self):
        accounts = sc.get_account_options(self.email)
        self.popup = InsertLoanWindow(self, accounts, self.submit_loan_data)
        self.popup.show()

    def submit_loan_data(self, fields):
        data = self.gather_form_values(fields)
        sql = "INSERT INTO Loans (INTEREST, VALUE, ACCOUNT_ID) VALUES (?, ?, ?)"
        sc.connect_and_insert(sql, data["INTEREST"], data["VALUE"], data["ACCOUNT_ID"])
        self.popup.close()
        self.win_manager.built_windows["loans_window"] = False
        self.load_loans()

    def load_loans(self):
            add_btn = QPushButton("Add Loan")
            add_btn.clicked.connect(lambda: self.open_add_loan_view())

            update_btn = QPushButton("Update Loan")
            update_btn.clicked.connect(self.open_update_loan_view)

            del_btn = QPushButton("Delete Loan")
            cmd = "DELETE FROM Loans WHERE ACCOUNT_ID=? AND VALUE=? AND INTEREST=?"
            del_btn.clicked.connect(lambda: self.call_delete_on_window(cmd,"loans_window"))

            self.load_window("loans_window",
                         "EXEC GetLoans @EMAIL=?",
                         cw.create_loan, add_button=add_btn, update_button=update_btn, delete_button=del_btn)

    def open_update_loan_view(self):
        selected = self.win_manager.current_windows["loans_window"].delete_checked()
        if len(selected) != 1:
            return
        self.selected_loan = selected[0]
        self.update_loan_popup = UpdateBalanceWindow(self, self.submit_update_loan_value)
        self.update_loan_popup.show()

    def submit_update_loan_value(self, fields):
        """Update a loan value similar to savings update: resolve ACCOUNT_ID via currency and then update by account+interest+value."""
        data = self.gather_form_values(fields)
        selected = self.selected_loan
        if not selected:
            return

        # normalize selected: may be scalar pk or list [pk, interest, value, code/...]
        if isinstance(selected, (list, tuple)):
            # if first element is PK, inner starts at index 1
            shift = 1 if isinstance(selected[0], int) or (isinstance(selected[0], str) and selected[0].isdigit()) else 0
            try:
                interest = selected[0 + shift]
                value = selected[1 + shift]
                currency_name = selected[2 + shift]
            except Exception:
                print("Unexpected selected loan format:", selected)
                return
        else:
            # If selected is scalar pk only, we cannot update by matching account+interest+value;
            # fallback: update by LOAN_ID if possible
            pk = selected
            sc.connect_and_delete(
                "UPDATE Loans SET VALUE=? WHERE LOAN_ID=?",
                data["BALANCE"],
                pk
            )
            self.update_loan_popup.close()
            self.win_manager.built_windows["loans_window"] = False
            self.load_loans()
            return

        # Resolve account id from currency string
        result = sc.connect_and_execute(
            "EXEC GetAccountID @EMAIL=?, @CURRENCY=?",
            self.email,
            str(currency_name)
        )
        if not result or result[0][0] is None:
            print("Could not resolve account id for currency:", currency_name)
            return  

        account_id = result[0][0]

        try:
            sc.connect_and_delete(
                "UPDATE Loans SET VALUE=? WHERE ACCOUNT_ID=? AND INTEREST=? AND VALUE=?",
                data["BALANCE"],
                account_id,
                float(interest),
                float(value)
            )
        except Exception as e:
            print("Loan update failed:", e)
            return

        self.update_loan_popup.close()
        self.win_manager.built_windows["loans_window"] = False
        self.load_loans()

    def load_window(self, window_name, command, create_func, add_button=None, update_button=None,
                    delete_button=None):
        self.win_manager.hide_windows_except([window_name])
        if self.win_manager.is_built(window_name):
             self.container = cw.create_layout_from_list(self,
                                                            self.email,
                                                            create_func,
                                                            sc.read_data,
                                                            command)
             self.win_manager.update_scroll(window_name,self.container)
             self.win_manager.show_window(window_name) 
             return
        
        window = self.win_manager.get_window(window_name)

        self.container = cw.create_layout_from_list(self,
                                                            self.email,
                                                            create_func,
                                                            sc.read_data,
                                                            command)

        window.add_widget_to_scroll(self.container)
        
        window.show_widgets()
        window.show()
        
        window_buttons = self.create_navigation_button(window)
        if add_button is not None:
            window_buttons.append(add_button)
        if update_button is not None:
            window_buttons.append(update_button)
        if delete_button is not None:
            window_buttons.append(delete_button)

        hf.add_widgets_to_window(window, window_buttons)

        window.setGeometry(self.setting.get_centerx() -300,
                                 self.setting.get_centery() -200,
                                 self.setting.scroll_widget_w+self.setting.button_width*3,
                                 self.setting.scroll_widget_h)
        
        self.win_manager.window_is_built(window_name)
    
    def create_navigation_button(self, parent):
        return [hf.create_pushbutton(self,"Loans", self.load_loans),
                    hf.create_pushbutton(self,"Budgets", self.load_budgets),
                    hf.create_pushbutton(self,"Savings", self.load_savings),
                    hf.create_pushbutton(self,"Accounts",self.load_accounts),
                    hf.create_pushbutton(self,"Transactions", self.load_transactions),
                    hf.create_pushbutton(self,"Recurring Payments", self.load_recurring_payments)]
    
    def submit_saving_data(self, fields):
        data = self.gather_form_values(fields)
        sql = "INSERT INTO SavingPlans (YIELD, BUDGET, ACCOUNT_ID, SAVING_GOAL_ID) VALUES (?, ?, ?, ?)"
        sc.connect_and_insert(sql, data["YIELD"],  data["BUDGET"],  data["ACCOUNT_ID"], data["SAVING_GOAL_ID"])
        self.popup.close()
        self.win_manager.built_windows["savings_window"] = False
        self.load_savings()

    def submit_recurring_payment_data(self, fields):
        data = self.gather_form_values(fields)
        sql = "INSERT INTO RecurringPayments (COMPANY_NAME, PRICE, SUBCATEGORY_ID, DUE_DATE, ACCOUNT_ID, FREQUENCY_ID, CURRENCY_ID) VALUES (?, ?, ?, ?, ?, ?, ?)"
        sc.connect_and_insert(sql, data["COMPANY_NAME"], data["PRICE"], data["SUBCATEGORY_ID"], data["DUE_DATE"],
                              data["ACCOUNT_ID"], data["FREQUENCY_ID"], sc.get_account_currency_with_id(data["ACCOUNT_ID"]))
        self.popup.close()
        self.win_manager.built_windows["recurring_payments_window"] = False
        self.load_recurring_payments()

    def submit_budget_data(self, fields):
        data = self.gather_form_values(fields)
        sql = "INSERT INTO Budgets (BALANCE, CATEGORY_ID, PERIOD_BEGIN, ACCOUNT_ID, PERIOD_END) VALUES (?, ?, ?, ?, ?)"
        sc.connect_and_insert(sql, data["BALANCE"], data["CATEGORY_ID"],
                                data["PERIOD_BEGIN"], data["ACCOUNT_ID"], data["PERIOD_END"])
        self.popup.close()
        self.win_manager.built_windows["budgets_window"] = False
        self.load_budgets()

    def submit_transaction_data(self, fields):
        data = self.gather_form_values(fields)
        sql = "INSERT INTO Transactions (TRANSACTION_TIME, SUBCATEGORY_ID, ACCOUNT_ID, AMOUNT, DIRECTION_ID, DESCRIPTION) VALUES (?, ?, ?, ?, ?, ?)"
        sc.connect_and_insert(sql, data["TRANSACTION_DATE"], data["SUBCATEGORY_ID"], 
        data["ACCOUNT_ID"], data["AMOUNT"], data["DIRECTION_ID"], data["DESCRIPTION"])
        self.popup.close()
        self.win_manager.built_windows["transactions_window"] = False
        self.load_transactions()

    def gather_form_values(self, fields):
        """Helper to safely peel UI data out of components."""
        data = {}
        for key, widget in fields.items():
            if isinstance(widget, QComboBox):
                data[key] = widget.currentData()
            else:
                data[key] = widget.text()
        return data

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
