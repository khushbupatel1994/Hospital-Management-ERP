"""
===========================================================
Cloud Secure Hospital Management & Accounting ERP System
Module  : Print Service
Version : 3.0
===========================================================
"""

import os
import platform
import subprocess
from tkinter import messagebox


class PrintService:

    # ==========================================
    # Print PDF
    # ==========================================

    def print_pdf(self, pdf_path):

        if not os.path.exists(pdf_path):

            messagebox.showerror(
                "Error",
                "PDF file not found."
            )

            return False

        try:

            system = platform.system()

            if system == "Windows":

                os.startfile(pdf_path, "print")

            elif system == "Darwin":

                subprocess.call(
                    ["lp", pdf_path]
                )

            else:

                subprocess.call(
                    ["lp", pdf_path]
                )

            return True

        except Exception as e:

            messagebox.showerror(
                "Print Error",
                str(e)
            )

            return False