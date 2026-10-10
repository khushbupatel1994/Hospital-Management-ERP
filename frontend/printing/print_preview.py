"""
===========================================================
Cloud Secure Hospital Management & Accounting ERP System
Module  : Print Preview
Version : 3.0
===========================================================
"""

import os
import platform
import subprocess
from tkinter import messagebox


class PrintPreview:

    # ==========================================
    # Open PDF
    # ==========================================

    def open_pdf(self, pdf_path):

        if not os.path.exists(pdf_path):

            messagebox.showerror(
                "Error",
                "PDF file not found."
            )

            return

        try:

            system = platform.system()

            if system == "Windows":

                os.startfile(pdf_path)

            elif system == "Darwin":

                subprocess.call(["open", pdf_path])

            else:

                subprocess.call(["xdg-open", pdf_path])

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )