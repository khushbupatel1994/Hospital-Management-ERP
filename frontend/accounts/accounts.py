"""
===========================================================
Cloud Secure Hospital Management & Accounting ERP System
Module  : Accounts Controller
Version : 2.0
===========================================================
"""

from tkinter import messagebox
from tkcalendar import DateEntry
from frontend.accounts.accounts_ui import AccountsUI
from frontend.accounts.accounts_service import AccountsService
from frontend.accounts.accounts_crud import AccountsCRUD
from datetime import date

class Accounts(AccountsUI):

    def __init__(self, root):

        super().__init__(root)

        self.service = AccountsService()

        self.crud = AccountsCRUD()

        self.bind_events()

        self.load_transactions()

        self.transaction_id.configure(state="normal")

        self.transaction_id.insert(
            0,
            self.crud.generate_transaction_id()
        )

        self.transaction_id.configure(state="disabled")

        self.selected_transaction_id = None

    # ==========================================
    # Bind Events
    # ==========================================

    def bind_events(self):

        self.add_btn.configure(
            command=self.add_transaction
        )

        self.update_btn.configure(
            command=self.update_transaction
        )

        self.delete_btn.configure(
            command=self.delete_transaction
        )

        self.search_btn.configure(
            command=self.search_transaction
        )

        self.search_entry.bind(
            "<KeyRelease>",
            lambda event: self.search_transaction()
        )

        self.clear_btn.configure(
            command=self.clear_form
        )

        self.accounts_table.bind(
            "<<TreeviewSelect>>",
            self.load_selected_transaction
        )

    # ==========================================
    # Add Transaction
    # ==========================================

    def add_transaction(self):

        transaction_type = self.transaction_type.get()

        category = self.category.get()

        amount = self.amount.get().strip()

        payment_mode = self.payment_mode.get()

        transaction_date = self.transaction_date.get().strip()

        description = self.description.get(
            "1.0",
            "end"
        ).strip()

        remarks = self.remarks.get(
            "1.0",
            "end"
        ).strip()

        if not self.service.validate_transaction(

            transaction_type,

            category,

            amount,

            payment_mode,

            transaction_date

        ):

            return

        self.transaction_id.configure(state="normal")

        transaction_id = self.transaction_id.get()

        self.transaction_id.configure(state="disabled")

        success = self.crud.add_transaction(

            transaction_id,

            transaction_type,

            category,

            float(amount),

            payment_mode,

            transaction_date,

            description,

            remarks

        )

        if success:

            messagebox.showinfo(
                "Success",
                "Transaction added successfully."
            )

            self.load_transactions()

            self.clear_form()

        else:

            messagebox.showerror(
                "Error",
                "Unable to add transaction."
            )

    # ==========================================
    # Clear Form
    # ==========================================

    def clear_form(self):

        self.transaction_id.configure(state="normal")

        self.transaction_id.delete(0, "end")

        self.transaction_id.insert(
            0,
            self.crud.generate_transaction_id()
        )

        self.transaction_id.configure(state="disabled")

        self.transaction_type.set("Income")

        self.category.set("Consultation")

        self.amount.delete(0, "end")

        self.payment_mode.set("Cash")

    
        self.transaction_date.set_date(date.today())

        self.description.delete(
            "1.0",
            "end"
        )

        self.remarks.delete(
            "1.0",
            "end"
        )

        self.selected_transaction_id = None

    # ==========================================
    # Load Transactions
    # ==========================================

    def load_transactions(self):

        for item in self.accounts_table.get_children():

            self.accounts_table.delete(item)

        rows = self.crud.load_transactions()

        for row in rows:

            self.accounts_table.insert(

                "",

                "end",

                values=row

            )

    # ==========================================
    # Load Selected Transaction
    # ==========================================

    def load_selected_transaction(self, event=None):

        selected = self.accounts_table.focus()

        if not selected:
            return

        values = self.accounts_table.item(
            selected,
            "values"
        )

        transaction = self.crud.get_transaction_by_id(
            int(values[0])
        )

        if not transaction:
            return

        self.selected_transaction_id = transaction[0]

        self.transaction_id.configure(state="normal")

        self.transaction_id.delete(0, "end")

        self.transaction_id.insert(
            0,
            transaction[1]
        )

        self.transaction_id.configure(state="disabled")

        self.transaction_type.set(
            transaction[2]
        )

        self.category.set(
            transaction[3]
        )

        self.amount.delete(0, "end")
        self.amount.insert(
            0,
            transaction[4]
        )

        self.payment_mode.set(
            transaction[5]
        )

        self.transaction_date.set_date(transaction[6])

        self.description.delete(
            "1.0",
            "end"
        )
        self.description.insert(
            "1.0",
            transaction[7]
        )

        self.remarks.delete(
            "1.0",
            "end"
        )
        self.remarks.insert(
            "1.0",
            transaction[8]
        )

        # ==========================================
        # Update Transaction
        # ==========================================

    def update_transaction(self):
        if self.selected_transaction_id is None:
            messagebox.showwarning(
                "Warning",
                "Please select a transaction."
            )
            return

        transaction_type = self.transaction_type.get()

        category = self.category.get()

        amount = self.amount.get().strip()

        payment_mode = self.payment_mode.get()

        transaction_date = self.transaction_date.get().strip()

        description = self.description.get(
            "1.0",
            "end"
        ).strip()

        remarks = self.remarks.get(
            "1.0",
            "end"
        ).strip()

        if not self.service.validate_transaction(

            transaction_type,

            category,

            amount,

            payment_mode,

            transaction_date

        ):

            return

        success = self.crud.update_transaction(

            self.selected_transaction_id,

            transaction_type,

            category,

            float(amount),

            payment_mode,

            transaction_date,

            description,

            remarks

        )

        if success:

            messagebox.showinfo(
                "Success",
                "Transaction updated successfully."
            )

            self.load_transactions()

            self.clear_form()

        else:

            messagebox.showerror(
                "Error",
                "Unable to update transaction."
            )


    # ==========================================
    # Delete Transaction
    # ==========================================

    def delete_transaction(self):

        selected = self.accounts_table.focus()

        if not selected:

            messagebox.showwarning(
                "Warning",
                "Please select a transaction."
            )

            return

        values = self.accounts_table.item(
            selected,
            "values"
        )

        transaction_db_id = int(values[0])

        transaction = self.crud.get_transaction_by_id(
            transaction_db_id
        )

        if not transaction:

            messagebox.showerror(
                "Error",
                "Transaction not found."
            )

            return

        if messagebox.askyesno(
            "Confirm",
            "Delete this transaction?"
        ):

            if self.crud.delete_transaction(
                transaction_db_id
            ):

                messagebox.showinfo(
                    "Success",
                    "Transaction deleted successfully."
                )

                self.load_transactions()

                self.clear_form()


    # ==========================================
    # Search Transaction
    # ==========================================

    def search_transaction(self):

        keyword = self.search_entry.get().strip()

        for item in self.accounts_table.get_children():

            self.accounts_table.delete(item)

        rows = self.crud.search_transaction(
            keyword
        )

        for row in rows:

            self.accounts_table.insert(

                "",

                "end",

                values=row

            )
