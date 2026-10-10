"""
===========================================================
Cloud Secure Hospital Management & Accounting ERP System
Module  : Dashboard Charts
Version : 3.0
===========================================================
"""

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class DashboardCharts:

    def __init__(self):

        pass

    # ==========================================
    # Revenue Chart
    # ==========================================

    def revenue_chart(

        self,

        parent

    ):

        figure = Figure(

            figsize=(5, 3),

            dpi=100

        )

        ax = figure.add_subplot(111)

        months = [

            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun"

        ]

        revenue = [

            15000,
            18000,
            22000,
            26000,
            31000,
            36000

        ]

        ax.plot(

            months,

            revenue,

            marker="o",

            linewidth=2

        )

        ax.set_title(

            "Monthly Revenue"

        )

        ax.set_ylabel(

            "Amount"

        )

        canvas = FigureCanvasTkAgg(

            figure,

            parent

        )

        canvas.draw()

        canvas.get_tk_widget().pack(

            fill="both",

            expand=True

        )

    # ==========================================
    # Patient Statistics
    # ==========================================

    def patient_chart(

        self,

        parent

    ):

        figure = Figure(

            figsize=(5,3),

            dpi=100

        )

        ax = figure.add_subplot(111)

        labels = [

            "OPD",

            "IPD",

            "Emergency",

            "Lab"

        ]

        values = [

            120,

            60,

            25,

            80

        ]

        ax.bar(

            labels,

            values

        )

        ax.set_title(

            "Patient Statistics"

        )

        canvas = FigureCanvasTkAgg(

            figure,

            parent

        )

        canvas.draw()

        canvas.get_tk_widget().pack(

            fill="both",

            expand=True

        )