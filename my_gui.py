"""
Here are the widges created that go into the scrollable area of a Window.
"""

from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QLineEdit, QCheckBox, QLabel, QWidget, QFormLayout, QSpacerItem
from PyQt6.QtCore import Qt

class Page(QWidget):
    """A page displays input boxes and labels, to read the text from the input boxes
        give the key of the box. You can call the avalaible_inputs() for the keys"""
    
    def __init__(self, window):
        """Initialize a Page for collecting input."""

        super().__init__(window)
        self.input_boxes = {}
        self.labels = {}
        self.setLayout(QFormLayout())

    def add_title(self, title: str, size=25):
        """Gives a title for the page!"""
        assert size > 0
        label = QLabel(title)
        label.setStyleSheet(f"font-size: {size}px;")
        self.layout().addRow(label)

    def add_empty_line_horizontal(self):
        """Adds an empty horizontal line"""

        self.layout().addItem(QSpacerItem(20,40,QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum))

    def add_input_boxes(self,**boxes) -> None:
        """The boxes must be dict of pairs of string:QLineEdit."""

        for box in boxes.values():
            if type(box) != QLineEdit:
                raise Exception("The dict must contain a string:QLineEdit pair!")
            
        for label,box in boxes.items():
            self.input_boxes[label] = box
            self.layout().addRow(label,box)

    def add_label(self, name, label):
        self.labels[name] = label
        self.layout().addRow(label)

    def label_already_exists(self, name):
        return name in self.labels.keys() 

    def text_from_box(self,label):
        """Given the label of the input box, the text from that box is returned."""

        if label not in self.input_boxes.keys():
            raise Exception("No such label exists")
        
        return self.input_boxes[label].text()

class Account(QWidget):
    """Shows basic information about the account when choosing which account to enter."""
    def __init__(self, window, purpose, currency, balance):
        """Create a widget that hold information about accounts."""
        super().__init__(window)
        self.purpose = purpose
        self.currency = currency
        self.balance = balance
        self.setLayout(QFormLayout())
        self.display_account()
        self.data = [purpose, currency, balance]
        self.delete_param = [currency]

    def display_account(self):
        self.layout().addItem(QSpacerItem(20,40,QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum))
        l = QLabel(text=str(self.balance) + self.currency)
        l.setStyleSheet("font-size: 40px")
        self.layout().addWidget(l)
        self.layout().addItem(QSpacerItem(20,40,QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum))
        l = QLabel(text=self.purpose)
        l.setStyleSheet("font-size: 25px")
        self.layout().addWidget(l)

    def get_data(self):
        return self.data

    def get_delete_params(self):
        return self.delete_param

class RecurringPayments(QWidget):
    """A widget that holds the data of a recurring payment."""
    def __init__(self, window, company, price, subcategory,
                 due_date, frequency, currency, name):
        """Using the email only it will get all the needed data
        and it will create the widget needed to store the data."""
        super().__init__(window)

        self.layout_ = QHBoxLayout()
        self.data = [company, price, currency, subcategory, due_date, frequency]

        self.create_interface()
        self.delete_params = [company, price, currency]

    def create_interface(self):
        """Based on the data it will create the widget's contence."""
        for d in self.data:
            l = QLabel(text=str(d))
            l.setStyleSheet("font-size: 20px")
            self.layout_.addWidget(l)

        self.setLayout(self.layout_)

    def get_data(self):
        return self.data

    def get_delete_params(self):
        return self.delete_params

class Transaction(QWidget):
    """A class that represent a transaction in a database."""
    def __init__(self, window, transaction_time, sub_cat, type, amount, description, code):
        """Creates a transaction widget that holds the data of a transaction."""
        super().__init__(window)

        self.essential = QWidget()
        self.layout_ = QHBoxLayout(self.essential)

        self.great_layout = QVBoxLayout(self)
        
        self.data = [transaction_time, sub_cat, type, amount, description, code]
        self.description_index = self.data.index(description)
        self.create_interface()
        self.delete_params = [transaction_time,type,code]
    
    def create_interface(self):
        """Based on the data it will create the widget's contence."""
        for i, d in enumerate(self.data):
            if i == self.description_index:
                continue
            l = QLabel(text=str(d))
            l.setStyleSheet("font-size: 20px")
            self.layout_.addWidget(l)

        des = QLabel(text=self.data[self.description_index])
        des.setStyleSheet("font-size: 20px")

        self.great_layout.addWidget(self.essential)
        self.great_layout.addWidget(des)
        self.setLayout(self.great_layout)

    def get_data(self):
        return self.data

    def get_delete_params(self):
        return self.delete_params

class Loan(QWidget):
    """A class that represent a loan in a database."""
    def __init__(self, window, interest, value, code):
        """Creates a transaction widget that holds the data of a transaction."""
        super().__init__(window)

        self.essential = QWidget()
        self.layout_ = QHBoxLayout()
        
        self.data = [value, code, str(interest)+"%"]
        self.create_interface()
        self.delete_params = [value, interest, code]
    
    def create_interface(self):
        """Based on the data it will create the widget's contence."""
        for d in self.data:
            l = QLabel(text=str(d))
            l.setStyleSheet("font-size: 20px")
            self.layout_.addWidget(l)

        self.setLayout(self.layout_)

    def get_data(self):
        return self.data

    def get_delete_params(self):
        return self.delete_params

class Budget(QWidget):
    """A class that represent a budget in a database."""
    def __init__(self, window, balance, period_begin, period_end, name, code):
        """Creates a transaction widget that holds the data of a transaction."""
        super().__init__(window)

        self.essential = QWidget()
        self.layout_ = QHBoxLayout()
        
        self.data = [balance, period_begin, period_end, name, code]
        self.create_interface()
        self.delete_params= [balance, period_begin, period_end, name]
        print("Delete params:", self.delete_params)
    
    def create_interface(self):
        """Based on the data it will create the widget's contence."""
        for d in self.data:
            l = QLabel(text=str(d))
            l.setStyleSheet("font-size: 20px")
            self.layout_.addWidget(l)

        self.setLayout(self.layout_)

    def get_data(self):
        return self.data

    def get_delete_params(self):
        return self.delete_params

class Saving(QWidget):
    """A class that represent a saving in a database."""
    def __init__(self, window, yield_, budget, code, name):
        """Creates a transaction widget that holds the data of a transaction."""
        super().__init__(window)

        self.essential = QWidget()
        self.layout_ = QHBoxLayout()
        
        self.data = [budget, code, str(yield_)+"%", name]
        self.create_interface()

        self.delete_params = [budget, yield_, code]
    
    def create_interface(self):
        """Based on the data it will create the widget's contence."""
        for d in self.data:
            l = QLabel(text=str(d))
            l.setStyleSheet("font-size: 20px")
            self.layout_.addWidget(l)

        self.setLayout(self.layout_)

    def get_data(self):
        return self.data

    def get_delete_params(self):
        return self.delete_params

class WidgetWithCheck(QWidget):
    """A widget that holds a widget with a checkbox for them to be selected."""
    def __init__(self,widget:QWidget, check: QCheckBox, parent=None):
        """Creates the horizontal layout with the widget and the checkbox"""
        super().__init__(parent)
        layout_ = QHBoxLayout()

        self.check = check
        self.widget = widget

        layout_.addWidget(widget)
        layout_.addWidget(check)

        self.setLayout(layout_)

    def checked(self):
        return self.check.checkState() == Qt.CheckState.Checked
    
    def get_data(self):
        """Return data for this checked widget.
        If the inner widget exposes get_data() return that value,
        and if a primary key (_pk) was attached by the creator,
        return a list with the pk prepended: [pk, ...inner...] (or [pk] if no inner).
        This keeps both delete-by-pk and update-by-values workflows working."""
        inner = None
        if hasattr(self.widget, 'get_data') and callable(self.widget.get_data):
            try:
                inner = self.widget.get_data()
            except Exception:
                inner = None
            if hasattr(self.widget, "_pk"):
                pk = getattr(self.widget, "_pk")
                if pk is None:
                    return inner
                # If inner is a list/tuple, prepend pk
                if isinstance(inner, (list, tuple)):
                    return [pk] + list(inner)
                # If inner exists but is scalar, return [pk, inner]
                if inner is not None:
                    return [pk, inner]
                # No inner data, just return pk
                return pk
            return inner

    def get_delete_params(self):
        return self.widget.get_delete_params() 