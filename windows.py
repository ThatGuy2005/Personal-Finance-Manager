"""
A Window is the main widget of the app. It is in the center and it has a scrollable area and buttons.
In the scrollabel area are the widgets with check, these are needed for operations.
"""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QTableWidgetItem, QVBoxLayout, QTableWidget
from PyQt6.QtWidgets import QComboBox, QLineEdit, QPushButton, QLabel, QScrollArea, QWidget, QTextEdit

import server_communication as sc

from my_gui import WidgetWithCheck

class Window(QWidget):
    """A class that is designed for A scrollable area and push_buttons."""

    def __init__(self,parent):
        """By default it creates one scrollable area."""

        super().__init__(parent)

        self.scrollable = QScrollArea()

        self.scrollable.setWidgetResizable(True)

        self.scrollable.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

        self.scrollable.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

        self.holds_widgets = QWidget()

        self.holds_widgets_layout = QVBoxLayout(self.holds_widgets)

        #self.scrollabel.setWidget(self.holds_widgets)

        self.great_layout = QHBoxLayout(self)

        self.scroll_labels = list()

        #self.great_layout.addWidget(self.scrollabel)

    def add_widget(self,widget: QPushButton):
        """Adds a push button to the window."""

        self.holds_widgets_layout.addWidget(widget)

    def add_widget_to_scroll(self,widget_container):
        """Adds a container of widgets to the scroll area"""
        self.widgets_in_scrollable = widget_container
        self.scrollable.setWidget(widget_container)

        self.great_layout.addWidget(self.scrollable)

    def show_widgets(self):
        """If you call this before add_widget_to_scroll then
        the buttons will be on the left."""

        self.great_layout.addWidget(self.holds_widgets) 

    def save_labels(self, labels):
        self.scroll_labels = labels

    def get_scroll_labels(self):
        return self.scroll_labels
    
    def delete_checked(self):
        container = self.scrollable.widget()
        if container is None:
            return [] 

        data_to_delete = list()
        for widget in container.findChildren(WidgetWithCheck):
            if widget.checked():
                print("Get_delete_param:", widget.get_delete_params())
                data_to_delete.append(widget.get_delete_params())

        return data_to_delete

class BaseInsertWindow(QWidget):
    """Base setup for popup submission windows."""
    def __init__(self, parent, title):
        super().__init__(parent, Qt.WindowType.Window)
        self.setWindowTitle(title)
        self.resize(380, 450)
        self.layout_ = QVBoxLayout(self)
        self.fields = {}

    def add_field(self, key, label_text):
        from windows import LineEdit
        field = LineEdit(label=label_text)
        self.layout_.addWidget(field)
        self.fields[key] = field

    def add_dropdown(self, key, label_text, options):
        """Options should be a list of tuples: (hidden_id, display_text)"""
        self.layout_.addWidget(QLabel(label_text))
        dropdown = QComboBox()
        for hidden_id, display_text in options:
            dropdown.addItem(display_text, userData=hidden_id)
        self.layout_.addWidget(dropdown)
        self.fields[key] = dropdown

class UpdateBalanceWindow(BaseInsertWindow):
    def __init__(self, parent, submit_callback):
        super().__init__(parent, "Update Saving Balance")
        self.add_field("BALANCE", "New Balance:")
        btn = QPushButton("Save Balance")
        btn.clicked.connect(lambda: submit_callback(self.fields))
        self.layout_.addWidget(btn)

class InsertSavingWindow(BaseInsertWindow):
    def __init__(self, parent, account_options, submit_callback, goal_options):
        super().__init__(parent, "Add Saving Plan")
        
        self.add_field("BUDGET", "Target Budget:")
        self.add_field("YIELD", "Expected Yield (%):")
        self.add_dropdown("ACCOUNT_ID", "Select Account:", account_options)
        self.add_dropdown("SAVING_GOAL_ID", "Select Goal:", goal_options)
        
        btn = QPushButton("Save Saving Plan")
        btn.clicked.connect(lambda: submit_callback(self.fields))
        self.layout_.addWidget(btn)

class InsertBudgetWindow(BaseInsertWindow):
    def __init__(self, parent, account_options, submit_callback, category_options):
        super().__init__(parent, "Create Budget")
        
        self.add_field("BALANCE", "Initial Balance:")
        self.add_field("PERIOD_BEGIN", "Start Date (YYYY-MM-DD):")
        self.add_field("PERIOD_END", "End Date (YYYY-MM-DD):")
        self.add_dropdown("ACCOUNT_ID", "Select Account:", account_options)
        self.add_dropdown("CATEGORY_ID", "Select Category:", category_options)
        
        btn = QPushButton("Save Budget")
        btn.clicked.connect(lambda: submit_callback(self.fields))
        self.layout_.addWidget(btn)


class InsertTransactionWindow(BaseInsertWindow):
    def __init__(self, parent, account_options, submit_callback, subcategory_options,
                 direction_options):
        super().__init__(parent, "Record New Transaction")
        
        self.add_field("AMOUNT", "Amount:")
        self.add_dropdown("SUBCATEGORY_ID", "Select Category:", subcategory_options)
        self.add_field("TRANSACTION_DATE", "Date (YYYY-MM-DD hh:mm:ss):")
        self.add_dropdown("ACCOUNT_ID", "Select Account:", account_options)
        self.add_dropdown("DIRECTION_ID","Select Direction:", direction_options)
        self.add_field("DESCRIPTION","Give a Description:")
        
        btn = QPushButton("Save Transaction")
        btn.clicked.connect(lambda: submit_callback(self.fields))
        self.layout_.addWidget(btn)

class WindowManager():
    """A class that holds windows and does operations on them.
    It holds a dict with a string and a window."""
    def __init__(self):
        """Creates an empty dict."""
        self.current_windows = dict()
        self.built_windows = dict()

    def add_window(self, name, window: Window):
        """Adds a window to the manager. It does nothing if the key already exists."""
        if name in self.current_windows.keys():
            print(f"This window already exists with the classifier:{name}.")
        else:
            self.current_windows[name] = window

    def hide_windows_except(self,keys:list):
        """Hides all windows except the specified ones."""
        for k, window in self.current_windows.items():
            if k in keys or window.isHidden():
                continue
            else:
                window.hide()

    def window_is_built(self,key):
        self.built_windows[key] = True

    def is_built(self, key):
        if key in self.built_windows.keys():
            return True
        else:
            return False
        
    def show_window(self, key):
        self.current_windows[key].show()

    def get_window(self, name):
        return self.current_windows[name]
    
    def update_scroll(self, window_name, widget_container):
        self.current_windows[window_name].add_widget_to_scroll(widget_container)

class LineEdit(QWidget):
    """Holds a label and a line edit object."""
    def __init__(self, parent=None, label=None):
        super().__init__(parent)

        self.label = QLabel(text=label)
        self.line_edit = QLineEdit()
        self.layout_ = QHBoxLayout()
        self.layout_.addWidget(self.label)
        self.layout_.addWidget(self.line_edit)

        self.setLayout(self.layout_)

    def text(self):
        return self.line_edit.text()

class InsertAccountWindow(BaseInsertWindow):
    def __init__(self, parent, currency_options, purpose_options, submit_callback):
        super().__init__(parent, "Add Account")
        
        self.add_field("BALANCE", "Initial Balance:")
        self.add_dropdown("CURRENCY_ID", "Select Currency:", currency_options)
        self.add_dropdown("PURPOSE_ID", "Select Purpose:",purpose_options)
        
        btn = QPushButton("Save Account")
        btn.clicked.connect(lambda: submit_callback(self.fields))
        self.layout_.addWidget(btn)

class InsertRecurringPayment(BaseInsertWindow):
    def __init__(self, parent, subcategory_options, account_options,
                 frequency_options, submit_callback):
            super().__init__(parent, "Add Recurring Payment")
            
            self.add_field("COMPANY_NAME", "Company:")
            self.add_field("PRICE", "Price:")
            self.add_dropdown("SUBCATEGORY_ID", "Select Subcategory:", subcategory_options)
            self.add_field("DUE_DATE", "Due date (YYYY-MM-DD):")
            self.add_dropdown("ACCOUNT_ID", "Account:", account_options)
            self.add_dropdown("FREQUENCY_ID", "Frequency:", frequency_options)
            
            btn = QPushButton("Save Recurring Payment")
            btn.clicked.connect(lambda: submit_callback(self.fields))
            self.layout_.addWidget(btn)

class InsertLoanWindow(BaseInsertWindow):
    def __init__(self, parent, account_options, submit_callback):
        super().__init__(parent, "Add Loan")
        self.add_field("INTEREST", "Interest (%):")
        self.add_field("VALUE", "Value:")
        # reuse account dropdown so loan can be linked to an account
        self.add_dropdown("ACCOUNT_ID", "Account:", account_options)
        btn = QPushButton("Save Loan")
        btn.clicked.connect(lambda: submit_callback(self.fields))
        self.layout_.addWidget(btn)

class AdminWindow(QWidget):
    def __init__(self, settings, parent=None):
        super().__init__(parent)
        self.setting = settings
        self.setWindowTitle("Admin View - Query Console")
        
        # Set geometry using Settings parameters
        w = self.setting.scroll_widget_w + (self.setting.button_width * 3)
        h = self.setting.scroll_widget_h + 150  # Added height for SQL input
        x = self.setting.get_centerx() - (w // 2) + self.setting.button_width
        y = self.setting.get_centery() - (h // 2)
        self.setGeometry(x, y, w, h)

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)

        # SQL Input Area
        main_layout.addWidget(QLabel("Execute SQL Query:"))
        self.query_input = QTextEdit()
        self.query_input.setPlaceholderText("SELECT * FROM Users;")
        self.query_input.setFixedHeight(80)
        main_layout.addWidget(self.query_input)

        # Controls Layout
        control_layout = QHBoxLayout()
        run_btn = QPushButton("Run Query")
        run_btn.setFixedHeight(self.setting.button_height)
        run_btn.clicked.connect(self.execute_query)

        refresh_btn = QPushButton("Refresh Default View")
        refresh_btn.setFixedHeight(self.setting.button_height)
        refresh_btn.clicked.connect(self.load_default_view)

        control_layout.addWidget(run_btn)
        control_layout.addWidget(refresh_btn)
        main_layout.addLayout(control_layout)

        # Status Label for Non-Select Queries / Errors
        self.status_label = QLabel("")
        main_layout.addWidget(self.status_label)

        # Results Table
        self.table = QTableWidget()
        main_layout.addWidget(self.table)

        self.load_default_view()

    def execute_query(self):
        query = self.query_input.toPlainText().strip()
        if not query:
            return

        self.status_label.setText("")

        try:
            # Check if query returns rows (SELECT / EXEC returning sets)
            if query.upper().startswith("SELECT") or query.upper().startswith("EXEC"):
                rows, labels = sc.connect_and_execute_with_labels(query)
                self.populate_table(rows, labels)
                self.status_label.setStyleSheet("color: green;")
                self.status_label.setText(f"Query returned {len(rows)} row(s).")
            else:
                # DML Statements (UPDATE, DELETE, INSERT)
                affected_rows = sc.connect_and_delete(query)  # Ensure function executes non-SELECT queries
                self.table.setRowCount(0)
                self.table.setColumnCount(0)
                self.status_label.setStyleSheet("color: green;")
                self.status_label.setText("Query executed successfully.")

        except Exception as e:
            self.status_label.setStyleSheet("color: red;")
            self.status_label.setText(f"SQL Error: {str(e)}")

    def populate_table(self, rows, labels):
        self.table.clear()
        if not labels:
            self.table.setRowCount(0)
            self.table.setColumnCount(0)
            return

        self.table.setRowCount(len(rows))
        self.table.setColumnCount(len(labels))
        self.table.setHorizontalHeaderLabels(labels)

        for row_index, row_data in enumerate(rows):
            for col_index, value in enumerate(row_data):
                self.table.setItem(row_index, col_index, QTableWidgetItem(str(value)))

    def load_default_view(self):
        self.query_input.setText("SELECT USER_ID, NAME, EMAIL, ROLE_ID FROM Users;")
        self.execute_query()