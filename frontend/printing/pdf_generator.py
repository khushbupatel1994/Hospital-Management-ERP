"""
===========================================================
Cloud Secure Hospital Management & Accounting ERP System
Module  : PDF Generator
Version : 3.0
===========================================================
"""

import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Table,
    TableStyle,
    Spacer
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm

from frontend.printing.invoice_template import InvoiceTemplate


class PDFGenerator:

    def __init__(self):

        self.styles = getSampleStyleSheet()

        self.template = InvoiceTemplate()

    # ==========================================
    # Generate Billing Invoice
    # ==========================================
    def billing_invoice(
        self,
        filename,
        invoice_no,
        patient,
        doctor,
        bill_date,
        amount,
        services=None
    ):

        pdf = SimpleDocTemplate(

            filename,

            pagesize=A4

        )

        story = []

        # Hospital Header

        story.append(
            self.template.hospital_header()
        )

        story.append(
            self.template.spacer()
        )

        # Invoice Title

        story.append(
            self.template.title(
                "Billing Invoice"
            )
        )

        story.append(
            self.template.spacer()
        )

        # ==========================================
        # Billing Information
        # ==========================================

        bill_data = [
            ["Invoice No", invoice_no],
            ["Patient Name", patient],
            ["Doctor Name", doctor],
            ["Bill Date", bill_date],
            ["Total Amount", f"₹ {amount}"]
        ]

        bill_table = Table(
            bill_data,
            colWidths=[50 * mm, 120 * mm]
        )

        bill_table.setStyle(
            TableStyle(
                [
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                    ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#E8F4FD")),
                    ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                    ("TOPPADDING", (0, 0), (-1, -1), 8),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE")
                ]
            )
        )

        story.append(bill_table)
        story.append(Spacer(1, 15))

        # ==========================================
        # Services Table
        # ==========================================

        service_data = [
            ["Service", "Qty", "Rate", "Amount"]
        ]

        if services:
            service_data.extend(services)
        else:
            service_data.extend([
                ["Consultation", "1", "₹500", "₹500"],
                ["Blood Test", "1", "₹350", "₹350"],
                ["Medicines", "2", "₹200", "₹400"]
            ])

        service_table = Table(
            service_data,
            colWidths=[80 * mm, 20 * mm, 35 * mm, 35 * mm]
        )

        service_table.setStyle(
            TableStyle(
                [
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#007ACC")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8)
                ]
            )
        )

        story.append(service_table)
        story.append(Spacer(1, 20))

        total_data = [
            ["Grand Total", f"₹ {amount}"]
        ]

        total_table = Table(
            total_data,
            colWidths=[135 * mm, 35 * mm]
        )

        total_table.setStyle(
            TableStyle(
                [
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                    ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#E8F4FD")),
                    ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
                    ("ALIGN", (1, 0), (1, 0), "RIGHT")
                ]
            )
        )

        story.append(total_table)
        story.append(Spacer(1, 20))

        story.append(
            Paragraph(
                "<br/><br/><b>Authorized Signature</b>",
                self.styles["Heading3"]
            )
        )

        story.append(
            Paragraph(
                f"""
                Generated On : {datetime.now().strftime("%d-%m-%Y %I:%M %p")}<br/><br/>
                Thank you for choosing Cloud Secure Hospital.<br/>
                We wish you a speedy recovery.<br/>
                This is a computer-generated invoice and does not require a signature.
                """,
                self.styles["Normal"]
            )
        )

        pdf.build(story)

        return os.path.abspath(filename)