from PyQt6.QtWidgets import QWidget, QVBoxLayout, QCheckBox

from my_gui import Account, WidgetWithCheck
from my_gui import RecurringPayments, Transaction, Loan, Budget, Saving

def create_hash(labels: list) -> dict:
    """Creates a simple hash, so that if the order
    of the columns change, then the program won't break."""
    hash_labels = dict()

    for i,label in enumerate(labels):
        hash_labels[label] = i

    return hash_labels

def create_using_function_with_check(window,email,create: callable, read: callable, command) -> list:
    """Given an email, a create function and a read function, this function will read
    the data from the database and return a list of widgets created with the data."""
    widgets = list()
    data, labels = read(email, command)

    # Create a hash so that we don't rely on indexing but column names
    hash_labels = create_hash(labels)

    # Create the user's accounts
    for d in data:
        widget = create(window, d, hash_labels)

        # Attach a primary key (first column name that ends with _ID) to the widget if present
        pk = None
        for col_name, idx in hash_labels.items():
            if col_name.endswith("_ID") and idx < len(d):
                pk = d[idx]
                break
        if pk is not None:
            # store pk on the created widget for later deletion/update operations
            try:
                widget._pk = pk
            except Exception:
                pass

        master_widget = WidgetWithCheck(widget,QCheckBox())
        
        widgets.append(master_widget)

    return widgets

def create_account(window, d, hash_labels):
    """Builds and returns an account widget."""
    return Account(window,d[hash_labels["PURPOSE_NAME"]],
                                 d[hash_labels["CURRENCY_NAME"]],
                                 d[hash_labels["BALANCE"]])

def create_recurring_payment(window, d, hash_labels):
    """Builds and returns a recurring_payment widget."""
    return RecurringPayments(window,d[hash_labels["COMPANY_NAME"]],
                                    d[hash_labels["PRICE"]],
                                    d[hash_labels["SUB_CAT"]],
                                    d[hash_labels["DUE_DATE"]],
                                    d[hash_labels["FREQ"]],
                                    d[hash_labels["NAME"]],
                                    d[hash_labels["USER_NAME"]])

def create_transaction(window, d, hash_labels):
    """Builds and returns a transaction widget."""
    return Transaction(window,d[hash_labels["TRANSACTION_TIME"]],
                                    d[hash_labels["SUB_CAT"]],
                                    d[hash_labels["AMOUNT"]],
                                    d[hash_labels["TYPE"]],
                                    d[hash_labels["DESCRIPTION"]],
                                    d[hash_labels["NAME"]])

def create_loan(window, d, hash_labels):
    """Builds and returns a loan widget."""
    return Loan(window,d[hash_labels["INTEREST"]],
                                    d[hash_labels["VALUE"]],
                                    d[hash_labels["NAME"]])

def create_budget(window, d, hash_labels):
    """Builds and returns a budget widget."""
    return Budget(window,d[hash_labels["BALANCE"]],
                                    d[hash_labels["NAME"]],
                                    d[hash_labels["PERIOD_BEGIN"]],
                                    d[hash_labels["PERIOD_END"]],
                                    d[hash_labels["CATEGORYNAME"]])

def create_saving(window, d, hash_labels):
    """Builds and returns a saving widget."""
    return Saving(window,d[hash_labels["YIELD"]],
                                    d[hash_labels["BUDGET"]],
                                    d[hash_labels["CURRENCY_NAME"]],
                                    d[hash_labels["SAVING_GOAL_NAME"]]
                                    )

def create_layout_from_list(window, email, create: callable, read: callable, command):
    """Gets the data associated to the email, then it creates a container
    for the data, then returns it."""
    # Here's the change, if it does not works roll back to create_using_function()
    widgets = create_using_function_with_check(window, email, create, read, command)

    container = QWidget()
    layout = QVBoxLayout(container)

    for widget in widgets:
        layout.addWidget(widget)

    layout.addStretch()

    return container