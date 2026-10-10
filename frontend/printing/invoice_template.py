"""
===========================================================
Cloud Secure Hospital Management & Accounting ERP System
Module  : Invoice Template
Version : 3.0
===========================================================
"""
import os

from reportlab.platypus import Image
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import (
    Table,
    TableStyle,
    Paragraph,
    Spacer
)
from reportlab.lib.styles import getSampleStyleSheet


class InvoiceTemplate:

    def __init__(self):

        self.styles = getSampleStyleSheet()

    # ==========================================
    # Hospital Header
    # ==========================================

   

    def hospital_header(self):

       logo_path = os.path.join(
          "assets",
           "logo",
           "hospital_logo.png"
        )

       if os.path.exists(logo_path):

             logo = Image(
                    logo_path,
                    width=35 * mm,
                    height=35 * mm
                     )

       else:

            logo = Paragraph(
               "<b>No Logo</b>",
               self.styles["Normal"]
           )

       hospital_info = Paragraph(

            "<b><font size=18>Cloud Secure Hospital</font></b><br/>"
            "Hospital Management & Accounting ERP<br/>"
            "Address : Mateswri scosity, Aanand<br/>"
            "Phone : +91-7046278573<br/>"
            "Email : info@cloudsecurehospital.com",

        self.styles["BodyText"]

        )

       table = Table(

        [

            [logo, hospital_info]

        ],

        colWidths=[40 * mm, 140 * mm]

    )

       table.setStyle(

          TableStyle(

            [

                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),

                ("LINEBELOW", (0, 0), (-1, -1), 1, colors.grey)

            ]

        )

    )

       return table

    # ==========================================
    # Title
    # ==========================================

    def title(self, text):

        return Paragraph(

            f"<b>{text}</b>",

            self.styles["Title"]

        )

    # ==========================================
    # Spacer
    # ==========================================

    def spacer(self):

        return Spacer(1, 8)