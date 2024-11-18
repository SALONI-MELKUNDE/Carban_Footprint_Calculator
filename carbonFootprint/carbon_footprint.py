import sys
from ctypes import windll

import pymysql
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QComboBox, QPushButton, QTabWidget, \
    QVBoxLayout, QHBoxLayout, QGridLayout, QGroupBox, QStyledItemDelegate, QTableWidget, QTableWidgetItem, QRadioButton, \
    QMessageBox
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtCore import Qt
# from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# from matplotlib.figure import Figure
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
import tempfile
import os
import MySQLdb as mdb

#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
HOST = "sql.freedb.tech"
USERNAME = "freedb_saloni"
PASSWORD = "Xyk$b8T!MNGQh&T"
DATABASE = "freedb_mydbcf"


class IconDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super(IconDelegate, self).__init__(parent)
        # Load tick and cross icons
        self.tick_icon = QIcon("tick.png")  # Path to tick icon image
        self.cross_icon = QIcon("cross.png")  # Path to cross icon image

    def paint(self, painter, option, index):
        # Get the value from the second column for comparison
        table = index.model().parent()  # Get the QTableWidget
        value = table.item(index.row(), 1).text()  # Second column value

        # Choose the icon based on the condition
        icon = self.cross_icon if value == "Warning" else self.tick_icon

        # Draw the icon in the third column
        icon.paint(painter, option.rect)


class CarbonFootprintCalculator(QMainWindow):
    def __init__(self, username, role):
        super().__init__()
        self.setWindowTitle("Carbon Footprint Calculator")
        self.setGeometry(100, 100, 400, 400)
        # self.setFixedWidth(600)
        self.username = username
        self.role = role
        self.init_ui()
        self.carbonCalculator = {}
        self.carbonCalculator.setdefault("Details", {})
        self.carbonCalculator.setdefault("Energy", {})
        self.carbonCalculator.setdefault("Waste", {})
        self.carbonCalculator.setdefault("Travel", {})
        self.carbonCalculator.setdefault("Results", {})

        # self.log_App = login_UI()
        # self.log_App = UI_Form()
        # self.log_App.show()

    def check_employee_count(self):
    
        try:
            # Get the input from the staff headcount field
            staff_count = int(self.tab1_staff_input.text())  # Convert to integer
            if staff_count < 250:
                # Show a suggestion for small business
                QMessageBox.information(self, "Suggestion", "Based on the number of employees, it is recommended to choose 'Small Enterprises'.")
                self.sbusiness_rbtn.setChecked(True)  # Automatically select the Small Business radio button
            else:
                # Show a suggestion for big business
                QMessageBox.information(self, "Suggestion", "Based on the number of employees, it is recommended to choose 'Large Enterprises'.")
                self.bbusiness_rbtn.setChecked(True)  # Automatically select the Big Business radio button
        except ValueError:
            # Handle invalid or empty input
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid number for the staff headcount.")

    def generate_feedback(self):

        #Generate feedback based on the total carbon footprint compared to the European average.
    
        try:
            total_cf = self.carbonCalculator["Results"].get("Total", 0)
            avg_cf = self.carbonCalculator["Details"].get("avg_europe", 0)

            if total_cf < avg_cf:
                # Positive Feedback
                feedback_text = (
                    "<b>Good/Positive Result:</b><br>"
                    "Fantastic work! Your carbon footprint is below the European average.<br>"
                    "Keep up these sustainable habits, and consider additional ways to further reduce your impact.<br><br>"
                    "<b>Energy:</b> You're doing great! Consider adding renewable energy options, like solar panels, to take it a step further.<br>"
                    "<b>Waste:</b> Keep up the progress! Composting organic waste and promoting recycling can make an even bigger difference.<br>"
                    "<b>Travel:</b> Excellent choices! Continue carpooling or using public transport whenever possible to maintain a low travel footprint."
                )
            else:
                # Negative Feedback
                feedback_text = (
                    "<b>Bad/Negative Result:</b><br>"
                    "Your carbon footprint is above the European average, but small changes can help!<br>"
                    "Try adopting sustainable practices in energy, waste, and travel to lower your impact.<br><br>"
                    "<b>Energy:</b><br>"
                    "- Switch to energy-efficient appliances and consider renewable options like solar panels.<br>"
                    "- Improve home insulation to cut down on heating and cooling needs.<br>"
                    "- Unplug devices when not in use to save energy.<br><br>"
                    "<b>Waste:</b><br>"
                    "- Try composting organic waste and using reusable bags to reduce single-use plastics.<br>"
                    "- Join a recycling program to ensure proper waste processing.<br>"
                    "- Donate items you no longer need instead of discarding them.<br><br>"
                    "<b>Travel:</b><br>"
                    "- Carpool or use public transport whenever possible.<br>"
                    "- Walk or bike short distances to reduce emissions.<br>"
                    "- Opt for virtual meetings to minimize travel when you can."
                )

            # Update the feedback label in Tab 8
            self.tab8_feedback_label.setText(feedback_text)

        except Exception as e:
            print(f"Error generating feedback: {e}")

    
    
    
    
    def generate_pdf(self):
        graph_spacing = 300  # Space between each graph
        graph_width = 500    # Width of the graph in the PDF
        graph_height = 250   # Height of the graph in the PDF

        try:
            # File  path to save the PDF
            file_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save PDF", "", "PDF Files (*.pdf)")
            if not file_path:
                return  # User canceled saving

            # Create a PDF canvas
            c = canvas.Canvas(file_path, pagesize=letter)

            # Add Title
            c.setFont("Helvetica-Bold", 20)
            c.drawString(50, 750, "Carbon Footprint Report")

            # Add User Details
            c.setFont("Helvetica", 12)
            y_position = 720
            for key, value in self.carbonCalculator["Details"].items():
                c.drawString(50, y_position, f"{key}: {value}")
                y_position -= 20

            # Add Results
            c.setFont("Helvetica-Bold", 14)
            c.drawString(50, y_position - 10, "Results:")
            y_position -= 30
            for key, value in self.carbonCalculator["Results"].items():
                c.drawString(50, y_position, f"{key}: {value:.2f} KgCO2")
                y_position -= 20

            # Add Feedback
            c.setFont("Helvetica-Bold", 14)
            c.drawString(50, y_position - 10, "Feedback:")
            y_position -= 30
            feedback_text = self.tab8_feedback_label.text()
            c.setFont("Helvetica", 12)
            for line in feedback_text.split("<br>"):  # Handle HTML line breaks
                c.drawString(50, y_position, line.strip().replace("<b>", "").replace("</b>", ""))
                y_position -= 20

            # Leave enough space for graphs
            y_position -= 50
            graph_spacing = 300  # Adjust spacing for graphs
            graph_width = 500
            graph_height = 300

            # Add Graphs
            graph_spacing = 300  # Space between each graph
            graph_width = 500    # Width of the graph in the PDF
            graph_height = 250   # Height of the graph in the PDF

            try:
                # Draw Total CF Graph
                if hasattr(self, 'total_cf_graph_path') and os.path.exists(self.total_cf_graph_path):
                    if y_position - (graph_height + graph_spacing) < 50:
                        c.showPage()
                        y_position = 750
                c.drawImage(self.total_cf_graph_path, 50, y_position - graph_height, width=graph_width, height=graph_height)
                y_position -= (graph_height + graph_spacing)

                # Draw Sub Graph
                if hasattr(self, 'sub_graph_path') and os.path.exists(self.sub_graph_path):
                    if y_position - (graph_height + graph_spacing) < 50:
                        c.showPage()
                        y_position = 750
                    c.drawImage(self.sub_graph_path, 50, y_position - graph_height, width=graph_width, height=graph_height)
                    y_position -= (graph_height + graph_spacing)

                # Draw Comparison Graph
                if hasattr(self, 'comparison_graph_path') and os.path.exists(self.comparison_graph_path):
                    if y_position - (graph_height + graph_spacing) < 50:
                        c.showPage()
                        y_position = 750
                    c.drawImage(self.comparison_graph_path, 50, y_position - graph_height, width=graph_width, height=graph_height)
                    y_position -= (graph_height + graph_spacing)
            except Exception as e:
                print(f"Error adding graphs to PDF: {e}")


            # Finalize and save the PDF
            c.save()
            QtWidgets.QMessageBox.information(self, "Success", f"PDF saved successfully at: {file_path}")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Error generating PDF: {e}")

           



    def init_ui(self):
        try:
            validator = QtGui.QDoubleValidator()  # Create validator.
            validator.setRange(0, 9999.0, 1)

            # self.setStyleSheet()
            # Create the main widget and layout
            self.central_widget = QWidget()
            self.setCentralWidget(self.central_widget)
            self.layout = QVBoxLayout(self.central_widget)

            self.my_font = QtGui.QFont()
            self.my_font.setBold(True)

            # Create the tab widget and add tabs
            self.tabs = QTabWidget()
            
            self.tabs.setStyleSheet("""
                QTabWidget::pane {
                    border: 1px solid #004d40; /* Border around the tab widget */
                    background: #e0f7fa; /* Light background for the pane */
                }

                QTabBar::tab {
                    background: #00796b; /* Default background color for tabs */
                    color: white; /* Default text color for tab labels */
                    font-weight: bold; /* Bold text for better visibility */
                    border: 1px solid #004d40; /* Border around each tab */
                    border-bottom: none; /* Prevent overlap with content pane */
                    padding: 8px 20px; /* Adjust padding for proper alignment */
                    margin: 2px; /* Space between tabs */
                    min-width: 100px; /* Minimum width for each tab */
                    border-top-left-radius: 10px; /* Rounded corners for tabs */
                    border-top-right-radius: 10px;
                }

                QTabBar::tab:selected {
                    background: #004d40; /* Background for the selected tab */
                    color: #e0f7fa; /* Text color for the selected tab */
                }

                QTabBar::tab:hover {
                    background: #005b4f; /* Hover effect for tabs */
                }
            """)
 

            self.tab1 = QWidget()
            self.tab2 = QWidget()
            self.tab3 = QWidget()
            self.tab4 = QWidget()
            self.tab5 = QWidget()
            self.tab6 = QWidget()
            self.tab7 = QWidget()
            self.tab8 = QWidget()
            self.tabs.addTab(self.tab1, "Welcome")
            self.tabs.addTab(self.tab2, "Energy")
            self.tabs.addTab(self.tab3, "Waste")
            self.tabs.addTab(self.tab4, "Travel/Transport")
            self.tabs.addTab(self.tab5, "Results")
            self.tabs.addTab(self.tab6, "Visualization")
            self.tabs.addTab(self.tab7, "Comparison")
            self.tabs.addTab(self.tab8, "Feedback")


            # Add widgets to the first tab
            self.tab1_layout = QGridLayout(self.tab1)
            
            self.tab1.setObjectName("tab1")
            
            image_path = os.path.abspath("images/carbon_footprint_background.png")

            self.tab1.setStyleSheet(f"""
                QWidget#tab1 {{                    
                    background-image: url('images/image.png');
                    background = QLabel()
                    pixmap = QPixmap("images/carbonfootprint_login.png")
                    scaled_pixmap = pixmap.scaled(400, 400)
                    background.setPixmap(scaled_pixmap)
                    background.setScaledContents(True)
                    background-repeat: no-repeat;
                    background-position: center;
                
                }}
            
        
        
                QLabel {{ 
                    color: #ffffff;
                    font-size: 13pt;
                    font-weight: bold;
                    background-color: rgba(0, 0, 0, 1);
                    padding: 8px;
                    border-radius: 8px;
                }}

                QLineEdit {{
                    background-color: rgba(255, 255, 255, 1);
                    color: #004d40;
                    font-size: 12pt;
                    padding: 8px;
                    border: 2px solid #00796b; 
                    border-radius: 8px;
                }}

                QPushButton {{
                    background-color: rgba(0, 51, 102, 1);
                    color: #ffffff;
                    font-size: 12pt;
                    font-weight: bold;
                    padding: 10px 20px;
                    border: none;                
                    border-radius: 8px;
                }}

                QPushButton:hover {{
                    background-color: rgba(0, 137, 123, 0.9); /* Slightly lighter green on hover */    
                }}                    
            """)


            background = QLabel()
            # Load the image using QPixmap
            pixmap = QPixmap("images/carbonfootprint_login.png")
            scaled_pixmap = pixmap.scaled(400, 400)

            # Set the pixmap to the label
            background.setPixmap(scaled_pixmap)
            background.setScaledContents(True)
            background.setToolTip(
                "Welcome to the Carbon Footprint Calculator!\n\nThis tool helps you understand and reduce your carbon footprint. "
                "Every small action counts toward a healthier planet.\nCalculate your emissions, get insights, and track your impact with tables & charts  for a sustainable future. ")
            

            self.tab1_staff_label = QLabel("Staff Headcount:")
            self.tab1_staff_input = QLineEdit()
            self.tab1_staff_input.setPlaceholderText("Enter number of staff")
            self.tab1_staff_input.setValidator(QtGui.QIntValidator())  # Ensures only integer input

            self.individual_rbtn = QRadioButton("Individual")
            self.individual_rbtn.setFont(QFont("Arial", 18, QFont.Bold))
            self.individual_rbtn.setStyleSheet("""
                color: #000000;  /* Bright white */
            """)
            self.individual_rbtn.setChecked(True)
            self.sbusiness_rbtn = QRadioButton("Small Enterprises")
            self.sbusiness_rbtn.setFont(QFont("Arial", 18, QFont.Bold))
            self.sbusiness_rbtn.setStyleSheet("""
                color: #000000;  /* Bright white */
            """)
            self.bbusiness_rbtn = QRadioButton("Large Enterprises")
            self.bbusiness_rbtn.setFont(QFont("Arial", 18, QFont.Bold))
            self.bbusiness_rbtn.setStyleSheet("""
                color: #000000;  /* Bright white */
            """)
            self.tab1_name_label = QLabel("Name:")
            self.tab1_name_input = QLineEdit()
            self.tab1_name_input.setPlaceholderText("Enter your name")
            self.tab1_year_label = QLabel("Year:")
            self.tab1_year_input = QComboBox()
            self.tab1_year_input.addItems(["2020","2021", "2022", "2023", "2024",])
            self.tab1_year_input.setCurrentIndex(4)
            self.tab1_next_button = QPushButton("Next")
            self.tab1_next_button.clicked.connect(lambda: self.switchTab(1))
            self.tab1_staff_input = QLineEdit()
            self.tab1_staff_input.editingFinished.connect(self.check_employee_count)

            


            self.tab1_layout.addWidget(background, 0, 0, 1, 8)
            self.tab1_layout.addWidget(self.tab1_staff_label, 1, 0, 1, 1)
            self.tab1_layout.addWidget(self.tab1_staff_input, 1, 1, 1, 7)
            self.tab1_layout.addWidget(self.individual_rbtn, 2, 3, 1, 1)
            self.tab1_layout.addWidget(self.sbusiness_rbtn, 2, 4, 1, 1)
            self.tab1_layout.addWidget(self.bbusiness_rbtn, 2, 5, 1, 1)
            self.tab1_layout.addWidget(self.tab1_name_label, 3, 0, 1, 1)
            self.tab1_layout.addWidget(self.tab1_name_input, 3, 1, 1, 7)
            self.tab1_layout.addWidget(self.tab1_year_label, 4, 0, 1, 1)
            self.tab1_layout.addWidget(self.tab1_year_input, 4, 1, 1, 7)
            self.tab1_layout.addWidget(self.tab1_next_button, 5, 6, 1, 2)


            self.tab1_staff_input.editingFinished.connect(lambda: self.carbonCalculator_func("Details"))
            self.tab1_name_input.editingFinished.connect(lambda: self.carbonCalculator_func("Details"))
            self.tab1_year_input.currentIndexChanged.connect(lambda: self.carbonCalculator_func("Details"))
            

            # Add widgets to the second tab
            self.tab2_layout = QGridLayout(self.tab2)
            
            self.tab2.setObjectName("tab2")
            
            image_path = os.path.abspath("images/carbon_footprint_background.png")

            self.tab2.setStyleSheet(f"""
                QWidget#tab2 {{                    
                    background-image: url('images/carbon_footprint_background.png');
                    background = QLabel()
                    pixmap = QPixmap("images/carbon_footprint_background.png")
                    scaled_pixmap = pixmap.scaled(400, 400)
                    background.setPixmap(scaled_pixmap)
                    background.setScaledContents(True)
                    background-repeat: no-repeat;
                    background-position: center;
                    
                }}
            
        
        
                QLabel {{ 
                    color: #ffffff;
                    font-size: 13pt;
                    font-weight: bold;
                    background-color: rgba(0, 0, 0, 1);
                    padding: 8px;
                    border-radius: 8px;
                }}

                QLineEdit {{
                    background-color: rgba(255, 255, 255, 1);
                    color: #004d40;
                    font-size: 12pt;
                    padding: 8px;
                    border: 2px solid #00796b; 
                    border-radius: 8px;
                }}

                QPushButton {{
                    background-color: rgba(0, 51, 102, 1);
                    color: #ffffff;
                    font-size: 12pt;
                    font-weight: bold;
                    padding: 10px 20px;
                    border: none;                
                    border-radius: 8px;
                }}

                QPushButton:hover {{
                    background-color: rgba(0, 137, 123, 0.9); /* Slightly lighter green on hover */    
                }}                    
            """)


            self.tab2_layout.setAlignment(Qt.AlignCenter)

            self.tab2_input_layout = QGridLayout()
            self.tab2_input_layout.addWidget(QLabel("What is your average monthly electricity bill in euros?"), 0, 0)
            self.tab2_input_layout.addWidget(QLabel("What is your average monthly natural gas bill in euros?"), 1, 0)
            self.tab2_input_layout.addWidget(QLabel("What is your average monthly fuel bill for transportation in euros?"),
                                             2, 0)
            self.tab2_electricity_input = QLineEdit()
            self.tab2_gas_input = QLineEdit()
            self.tab2_fuel_input = QLineEdit()
            self.tab2_electricity_input.setValidator(validator)
            self.tab2_gas_input.setValidator(validator)
            self.tab2_fuel_input.setValidator(validator)
            self.tab2_input_layout.addWidget(self.tab2_electricity_input, 0, 1)
            self.tab2_input_layout.addWidget(self.tab2_gas_input, 1, 1)
            self.tab2_input_layout.addWidget(self.tab2_fuel_input, 2, 1)
            self.tab2_layout.addLayout(self.tab2_input_layout, 0, 0, 1, 0)
            self.tab2_electricity_input.editingFinished.connect(lambda: self.carbonCalculator_func("Energy"))
            self.tab2_gas_input.editingFinished.connect(lambda: self.carbonCalculator_func("Energy"))
            self.tab2_fuel_input.editingFinished.connect(lambda: self.carbonCalculator_func("Energy"))

            self.tab2_previous_button = QPushButton("Previous")
            self.tab2_previous_button.clicked.connect(lambda: self.switchTab(0))
            self.tab2_next_button = QPushButton("Next")
            self.tab2_next_button.clicked.connect(lambda: self.switchTab(2))
            self.tab2_layout.addWidget(self.tab2_previous_button, 5, 0)
            self.tab2_layout.addWidget(self.tab2_next_button, 5, 3)

            # Add widgets to the third tab
            self.tab3_layout = QGridLayout(self.tab3)
            
            self.tab3.setObjectName("tab3")
            
            image_path = os.path.abspath("images/carbon_footprint_background.png")

            self.tab3.setStyleSheet(f"""
                QWidget#tab3 {{                    
                    background-image: url('images/carbon_footprint_background.png');
                    background = QLabel()
                    pixmap = QPixmap("images/carbon_footprint_background.png")
                    scaled_pixmap = pixmap.scaled(400, 400)
                    background.setPixmap(scaled_pixmap)
                    background.setScaledContents(True)
                    background-repeat: no-repeat;
                    background-position: center;
                    
                }}
            
        
        
                QLabel {{ 
                    color: #ffffff;
                    font-size: 13pt;
                    font-weight: bold;
                    background-color: rgba(0, 0, 0, 1);
                    padding: 8px;
                    border-radius: 8px;
                }}

                QLineEdit {{
                    background-color: rgba(255, 255, 255, 1);
                    color: #004d40;
                    font-size: 12pt;
                    padding: 8px;
                    border: 2px solid #00796b; 
                    border-radius: 8px;
                }}

                QPushButton {{
                    background-color: rgba(0, 51, 102, 1);
                    color: #ffffff;
                    font-size: 12pt;
                    font-weight: bold;
                    padding: 10px 20px;
                    border: none;                
                    border-radius: 8px;
                }}

                QPushButton:hover {{
                    background-color: rgba(0, 137, 123, 0.9); /* Slightly lighter green on hover */    
                }}                    
            """)


            self.tab3_layout.setAlignment(Qt.AlignCenter)

            self.tab3_input_layout = QGridLayout()
            self.tab3_input_layout.addWidget(QLabel("How much waste do you generate per month in kilograms?"), 0, 0)
            self.tab3_input_layout.addWidget(QLabel("How much of that waste is recycled or composted(in %)?"), 1, 0)
            self.tab3_waste_generated = QLineEdit()
            self.tab3_waste_recycle = QLineEdit()
            self.tab3_waste_generated.setValidator(validator)
            self.tab3_waste_recycle.setValidator(validator)
            self.tab3_input_layout.addWidget(self.tab3_waste_generated, 0, 1)
            self.tab3_input_layout.addWidget(self.tab3_waste_recycle, 1, 1)
            self.tab3_layout.addLayout(self.tab3_input_layout, 0, 0, 1, 4)
            self.tab3_waste_generated.editingFinished.connect(lambda: self.carbonCalculator_func("Waste"))
            self.tab3_waste_recycle.editingFinished.connect(lambda: self.carbonCalculator_func("Waste"))

            self.tab3_previous_button = QPushButton("Previous")
            self.tab3_previous_button.clicked.connect(lambda: self.switchTab(1))
            self.tab3_next_button = QPushButton("Next")
            self.tab3_next_button.clicked.connect(lambda: self.switchTab(3))
            self.tab3_layout.addWidget(self.tab3_previous_button, 4, 0)
            self.tab3_layout.addWidget(self.tab3_next_button, 4, 3)

            # Add widgets to the fourth tab
            self.tab4_layout = QGridLayout(self.tab4)
            
            self.tab4.setObjectName("tab4")
            
            image_path = os.path.abspath("images/carbon_footprint_background.png")

            self.tab4.setStyleSheet(f"""
                QWidget#tab4 {{                    
                    background-image: url('images/carbon_footprint_background.png');
                    background = QLabel()
                    pixmap = QPixmap("images/carbon_footprint_background.png")
                    scaled_pixmap = pixmap.scaled(400, 400)
                    background.setPixmap(scaled_pixmap)
                    background.setScaledContents(True)
                    background-repeat: no-repeat;
                    background-position: center;
                    
                }}
            
        
        
                QLabel {{ 
                    color: #ffffff;
                    font-size: 13pt;
                    font-weight: bold;
                    background-color: rgba(0, 0, 0, 1);
                    padding: 8px;
                    border-radius: 8px;
                }}

                QLineEdit {{
                    background-color: rgba(255, 255, 255, 1);
                    color: #004d40;
                    font-size: 12pt;
                    padding: 8px;
                    border: 2px solid #00796b; 
                    border-radius: 8px;
                }}

                QPushButton {{
                    background-color: rgba(0, 51, 102, 1);
                    color: #ffffff;
                    font-size: 12pt;
                    font-weight: bold;
                    padding: 10px 20px;
                    border: none;                
                    border-radius: 8px;
                }}

                QPushButton:hover {{
                    background-color: rgba(0, 137, 123, 0.9); /* Slightly lighter green on hover */    
                }}                    
            """)


            self.tab4_layout.setAlignment(Qt.AlignCenter)

            self.tab4_input_layout = QGridLayout()
            self.tab4_input_layout.addWidget(
                QLabel("How many kilometers do your employees travel per year for business purposes?"), 0, 0)
            self.tab4_input_layout.addWidget(
                QLabel("What is the average fuel efficiency of the vehicles used for business travel in litres/100kms?"), 1,
                0)
            self.tab4_distance = QLineEdit()
            self.tab4_fuel_efficiency = QLineEdit()
            self.tab4_distance.setValidator(validator)
            self.tab4_fuel_efficiency.setValidator(validator)
            self.tab4_input_layout.addWidget(self.tab4_distance, 0, 1)
            self.tab4_input_layout.addWidget(self.tab4_fuel_efficiency, 1, 1)
            self.tab4_layout.addLayout(self.tab4_input_layout, 0, 0, 1, 4)
            self.tab4_distance.editingFinished.connect(lambda: self.carbonCalculator_func("Travel"))
            self.tab4_fuel_efficiency.editingFinished.connect(lambda: self.carbonCalculator_func("Travel"))

            self.tab4_previous_button = QPushButton("Previous")
            self.tab4_previous_button.clicked.connect(lambda: self.switchTab(2))
            self.tab4_next_button = QPushButton("Next")
            self.tab4_next_button.clicked.connect(lambda: self.switchTab(4))
            self.tab4_layout.addWidget(self.tab4_previous_button, 4, 0)
            self.tab4_layout.addWidget(self.tab4_next_button, 4, 3)

            # Add widgets to the fifth tab
            self.tab5gb = QGroupBox()
            
            self.tab5.setObjectName("tab5")

            image_path = os.path.abspath("images/carbon_footprint_background.png")

            self.tab5.setStyleSheet(f"""
                QWidget#tab5 {{                    
                    background-image: url('images/carbon_footprint_background.png');
                    background = QLabel()
                    pixmap = QPixmap("images/carbon_footprint_background.png")
                    scaled_pixmap = pixmap.scaled(400, 400)
                    background.setPixmap(scaled_pixmap)
                    background.setScaledContents(True)
                    background-repeat: no-repeat;
                    background-position: center;
                }}
    
                QLabel {{ 
                    color: #ffffff;
                    font-size: 13pt;
                    font-weight: bold;
                    background-color: rgba(0, 0, 0, 1);
                    padding: 8px;
                    border-radius: 8px;
                }}

                QFrame#tableContainer {{
                    background-color: rgba(0, 51, 102, 0.8); /* Dark blue padding color */
                    border-radius: 12px; /* Rounded corners */
                    padding: 10px; /* Space around the table */
                }}

                QTableWidget {{
                    background-color: rgba(255, 255, 255, 0.9); /* Light white background for the table */
                    color: #004d40;
                    font-size: 12pt;
                    border: 2px solid #00796b; 
                    border-radius: 8px;
                    gridline-color: #00796b;
                }}
    
                QTableWidget::item {{
                    background-color: rgba(255, 255, 255, 1); /* Solid white for table items */
                    color: #004d40;
                }}

                QHeaderView::section {{
                    background-color: rgba(42, 161, 131, 1); /* Header background color */
                    color: white;
                    font-weight: bold;
                    padding: 5px;
                }}

                QPushButton {{
                    background-color: rgba(0, 51, 102, 1);
                    color: #ffffff;
                    font-size: 12pt;
                    font-weight: bold;
                    padding: 10px 20px;
                    border: none;                
                    border-radius: 8px;
                }}

                QPushButton:hover {{
                    background-color: rgba(0, 137, 123, 0.9); /* Slightly lighter green on hover */    
                }}                    
            """)

            self.tab5layout = QGridLayout()
            self.tab5gb.setLayout(self.tab5layout)

            self.tab5_layout = QGridLayout(self.tab5)
            # self.tab5_layout.setAlignment(Qt.AlignCenter)

            self.table = QTableWidget(6, 2)  # Set up a table with 2 columns
            self.table.verticalHeader().setVisible(False)
            # Set column headers
            self.table.setHorizontalHeaderLabels(["Operators", "Carbon Footprint (KgCO2)"])
            self.table.horizontalHeader().setFont(self.my_font)
            self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
            self.table.horizontalHeader().setFixedHeight(40)
            self.table.horizontalHeader().setStyleSheet("QHeaderView::section { background-color: #2aa183; color: white; }")

            # Populate the table with sample data
            self.table.setItem(0, 0, QTableWidgetItem("Energy"))
            self.table.setItem(1, 0, QTableWidgetItem("Waste"))
            self.table.setItem(2, 0, QTableWidgetItem("Business Travel"))
            self.table.setItem(3, 0, QTableWidgetItem("Total"))
            self.table.setItem(4, 0, QTableWidgetItem("Europe Average"))
            self.table.setItem(5, 0, QTableWidgetItem("Per Capita CF"))  # Add label for Per Capita CF

            for col in range(self.table.rowCount()):
                if self.table.item(col, 0) is not None:  # Check if the item exists
                    self.table.item(col, 0).setFlags(Qt.ItemIsEnabled)

                if self.table.item(col, 1) is None:  # Ensure the item exists before modifying
                    self.table.setItem(col, 1, QtWidgets.QTableWidgetItem())
                self.table.item(col, 1).setFlags(Qt.ItemIsEnabled)
            self.table.item(5, 0).setFlags(Qt.ItemIsEnabled)
            
            self.tab5layout.addWidget(self.table, 0, 0)

            self.tab5_previous_button = QPushButton("Previous")
            self.tab5_previous_button.clicked.connect(lambda: self.switchTab(3))
            self.tab5_next_button = QPushButton("Next")
            self.tab5_next_button.clicked.connect(lambda: self.switchTab(5))
            self.tab5_calculate_button = QPushButton("Calculate")
            self.tab5_calculate_button.setFixedHeight(50)
            self.tab5_calculate_button.setFont(self.my_font)
            self.tab5_calculate_button.setStyleSheet("""
                QPushButton {
                    background-color: #DC143C; /* Green color */
                    color: white;
                    font-size: 16px;
                    font-weight: bold;
                    padding: 10px 20px;
                    border: none;
                    border-radius: 8px;
                }
                QPushButton:hover {
                    background-color: #FF6347; /* Slightly lighter green */
                }
            """)

            self.tab5_layout.addWidget(self.tab5gb, 0, 0, 1, 3)
            self.tab5_layout.addWidget(self.tab5_previous_button, 1, 0)
            self.tab5_layout.addWidget(self.tab5_calculate_button, 1, 1)
            self.tab5_layout.addWidget(self.tab5_next_button, 1, 2)
            self.tab5_calculate_button.clicked.connect(lambda: self.carbonCalculator_func("Result"))

            # fig = Figure(figsize=(5, 4), dpi=100)
            # ax = fig.add_subplot(111)
            # # ax.plot([1, 2, 3, 4, 5], [10, 20, 30, 40, 50])
            # canvas = FigureCanvas(fig)
            self.web_view = QWebEngineView()
            self.web_view_sub = QWebEngineView()

            # Add widgets to the sixth tab
            self.tab6gb = QGroupBox()

            self.tab6.setObjectName("tab6")

            image_path = os.path.abspath("images/carbon_footprint_background.png")

            self.tab6.setStyleSheet(f"""
                QWidget#tab6 {{                    
                    background-image: url('images/carbon_footprint_background.png');
                    background = QLabel()
                    pixmap = QPixmap("images/carbon_footprint_background.png")
                    scaled_pixmap = pixmap.scaled(400, 400)
                    background.setPixmap(scaled_pixmap)
                    background.setScaledContents(True)
                    background-repeat: no-repeat;
                    background-position: center;
                }}
    
                QLabel {{ 
                    color: #ffffff;
                    font-size: 13pt;
                    font-weight: bold;
                    background-color: rgba(0, 0, 0, 1);
                    padding: 8px;
                    border-radius: 8px;
                }}

                QFrame#tableContainer {{
                    background-color: rgba(0, 51, 102, 0.8); /* Dark blue padding color */
                    border-radius: 12px; /* Rounded corners */
                    padding: 10px; /* Space around the table */
                }}

                QTableWidget {{
                    background-color: rgba(255, 255, 255, 0.9); /* Light white background for the table */
                    color: #004d40;
                    font-size: 12pt;
                    border: 2px solid #00796b; 
                    border-radius: 8px;
                    gridline-color: #00796b;
                }}
    
                QTableWidget::item {{
                    background-color: rgba(255, 255, 255, 1); /* Solid white for table items */
                    color: #004d40;
                }}

                QHeaderView::section {{
                    background-color: rgba(42, 161, 131, 1); /* Header background color */
                    color: white;
                    font-weight: bold;
                    padding: 5px;
                }}

                QPushButton {{
                    background-color: rgba(0, 51, 102, 1);
                    color: #ffffff;
                    font-size: 12pt;
                    font-weight: bold;
                    padding: 10px 20px;
                    border: none;                
                    border-radius: 8px;
                }}

                QPushButton:hover {{
                    background-color: rgba(0, 137, 123, 0.9); /* Slightly lighter green on hover */    
                }}                    
            """)

            self.tab6layout = QGridLayout()
            self.tab6gb.setLayout(self.tab6layout)

            self.tab6_layout = QGridLayout(self.tab6)

            self.tab6layout.addWidget(self.web_view, 0, 0)
            self.tab6layout.addWidget(self.web_view_sub, 1, 0)

            self.tab6_previous_button = QPushButton("Previous")
            self.tab6_previous_button.clicked.connect(lambda: self.switchTab(4))
            self.tab6_next_button = QPushButton("Next")
            self.tab6_next_button.clicked.connect(lambda: self.switchTab(6))
            self.tab6_layout.addWidget(self.tab6gb, 0, 0, 1, 2)
            self.tab6_layout.addWidget(self.tab6_previous_button, 1, 0)
            self.tab6_layout.addWidget(self.tab6_next_button, 1, 1)
            


            # Add widgets to the seventh tab
            self.tab7gb = QGroupBox()
            
            self.tab7.setObjectName("tab7")

            image_path = os.path.abspath("images/carbon_footprint_background.png")

            self.tab7.setStyleSheet(f"""
                QWidget#tab7 {{                    
                    background-image: url('images/carbon_footprint_background.png');
                    background = QLabel()
                    pixmap = QPixmap("images/carbon_footprint_background.png")
                    scaled_pixmap = pixmap.scaled(400, 400)
                    background.setPixmap(scaled_pixmap)
                    background.setScaledContents(True)
                    background-repeat: no-repeat;
                    background-position: center;
                }}
    
                QLabel {{ 
                    color: #ffffff;
                    font-size: 13pt;
                    font-weight: bold;
                    background-color: rgba(0, 0, 0, 1);
                    padding: 8px;
                    border-radius: 8px;
                }}

                QFrame#tableContainer {{
                    background-color: rgba(0, 51, 102, 0.8); /* Dark blue padding color */
                    border-radius: 12px; /* Rounded corners */
                    padding: 10px; /* Space around the table */
                }}

                QTableWidget {{
                    background-color: rgba(255, 255, 255, 0.9); /* Light white background for the table */
                    color: #004d40;
                    font-size: 12pt;
                    border: 2px solid #00796b; 
                    border-radius: 8px;
                    gridline-color: #00796b;
                }}
    
                QTableWidget::item {{
                    background-color: rgba(255, 255, 255, 1); /* Solid white for table items */
                    color: #004d40;
                }}

                QHeaderView::section {{
                    background-color: rgba(42, 161, 131, 1); /* Header background color */
                    color: white;
                    font-weight: bold;
                    padding: 5px;
                }}

                QPushButton {{
                    background-color: rgba(0, 51, 102, 1);
                    color: #ffffff;
                    font-size: 12pt;
                    font-weight: bold;
                    padding: 10px 20px;
                    border: none;                
                    border-radius: 8px;
                }}

                QPushButton:hover {{
                    background-color: rgba(0, 137, 123, 0.9); /* Slightly lighter green on hover */    
                }}                    
            """)


            self.tab7layout = QGridLayout()
            self.tab7gb.setLayout(self.tab7layout)

            self.tab7_layout = QGridLayout(self.tab7)

            self.web_view2 = QWebEngineView()

            self.tab7_compare_button = QPushButton("Compare")
            self.tab7_compare_button.setFixedHeight(50)
            self.tab7_compare_button.setFont(self.my_font)
            self.tab7_compare_button.setStyleSheet("""
                QPushButton {
                    background-color: #DC143C; /* Crimson */
                    color: white;
                    font-size: 16px;
                    font-weight: bold;
                    padding: 10px 20px;
                    border: none;
                    border-radius: 8px;
                }
                QPushButton:hover {
                    background-color: #FF6347; /* Tomato Red */
                }
            """)
            self.tab7_compare_button.clicked.connect(self.visualization_comparison)

            self.tab7layout.addWidget(self.web_view2)

            self.tab7_previous_button = QPushButton("Previous")
            self.tab7_previous_button.clicked.connect(lambda: self.switchTab(5))
            self.tab7_next_button = QPushButton("Next")
            self.tab7_next_button.clicked.connect(lambda: self.switchTab(7))
            self.tab7_layout.addWidget(self.tab7gb, 0, 0, 1, 3)
            self.tab7_layout.addWidget(self.tab7_previous_button, 1, 0)
            self.tab7_layout.addWidget(self.tab7_compare_button, 1, 1)
            self.tab7_layout.addWidget(self.tab7_next_button, 1, 2)


            #Add widgets to the Eighth tab
            self.tab8gb = QGroupBox()

            
            self.tab8gb.setTitle("Remarks:")
            self.tab8gb.setFont(QtGui.QFont("Arial", 19, QtGui.QFont.Bold))
            self.tab8gb.setStyleSheet("""
                QGroupBox {
                    color: #FF0000;
                    font-size: 16pt;
                    font-weight: bold;
                }
            """)
            
            self.tab8.setObjectName("tab8")
            
            image_path = os.path.abspath("images/carbon_footprint_background.png")
            self.tab8.setStyleSheet(f"""
                QWidget#tab8 {{                    
                    background-image: url('images/carbon_footprint_background.png');
                    background = QLabel()
                    pixmap = QPixmap("images/carbon_footprint_background.png")
                    scaled_pixmap = pixmap.scaled(400, 400)
                    background.setPixmap(scaled_pixmap)
                    background.setScaledContents(True)
                    background-repeat: no-repeat;
                    background-position: center;
                    
                }}
                
                                    
                QPushButton {{
                    background-color: rgba(0, 51, 102, 1);
                    color: #ffffff;
                    font-size: 12pt;
                    font-weight: bold;
                    padding: 10px 20px;
                    border: none;                
                    border-radius: 8px;
                }}

                QPushButton:hover {{
                    background-color: rgba(0, 137, 123, 0.9); /* Slightly lighter green on hover */    
                }}                    
            """)



            self.tab8layout = QVBoxLayout()
            self.tab8gb.setLayout(self.tab8layout)

            # Add feedback dynamically here
            self.tab8_feedback_label = QLabel()
            self.tab8_feedback_label.setWordWrap(True)
            self.tab8_feedback_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
            self.tab8_feedback_label.setFont(QtGui.QFont("Arial", 11))
            self.tab8_feedback_label.setStyleSheet("""
                QLabel {
                    background-color: rgba(255, 255, 255, 0.8); 
                    color: #000000;
                    font-size: 13pt;
                    font-weight: bold; /* Make the text bold */
                    padding: 10px; /* Padding to add spacing around text */
                    border-radius: 8px; /* Rounded corners for a polished look */
                }
            """)

            # Add the feedback label to the layout
            self.tab8layout.addWidget(self.tab8_feedback_label)

            # Buttons for navigation in Tab 8
            self.tab8_previous_button = QPushButton("Previous")
            self.tab8_previous_button.clicked.connect(lambda: self.switchTab(6))

            #pdf generater
            self.download_pdf_button = QPushButton("Download PDF")
            self.download_pdf_button.setFixedHeight(50)
            self.download_pdf_button.setFont(QtGui.QFont("Arial", 12, QtGui.QFont.Bold))
            self.download_pdf_button.setStyleSheet("""
                QPushButton {
                    background-color: #DC143C; /* Crimson */
                    color: white;
                    font-size: 16px;
                    font-weight: bold;
                    padding: 10px 20px;
                    border: none;
                    border-radius: 8px;
                }
                QPushButton:hover {
                    background-color: #FF6347; /* Darker green */
                }
            """)
            self.download_pdf_button.clicked.connect(self.generate_pdf)

            self.tab8layout.addWidget(self.download_pdf_button)



            # Main grid layout for the tab
            self.tab8_layout = QGridLayout(self.tab8)
            self.tab8_layout.addWidget(self.tab8gb, 0, 0, 1, 2)
            self.tab8_layout.addWidget(self.tab8_previous_button, 1, 0)
            self.tab8_layout.addWidget(self.download_pdf_button, 1, 1)
            



















            #Add widgets to the ninth tab
            self.tab9 = QWidget()
            self.tab9.setObjectName("tab9")

            image_path = os.path.abspath("images/carbon_footprint_background.png")

            self.tab9.setStyleSheet(f"""
                QWidget#tab9 {{                    
                    background-image: url('images/carbon_footprint_background.png');
                    background = QLabel()
                    pixmap = QPixmap("images/carbon_footprint_background.png")
                    scaled_pixmap = pixmap.scaled(400, 400)
                    background.setPixmap(scaled_pixmap)
                    background.setScaledContents(True)
                    background-repeat: no-repeat;
                    background-position: center;
                }}
    
                QLabel {{ 
                    color: #ffffff;
                    font-size: 13pt;
                    font-weight: bold;
                    background-color: rgba(0, 0, 0, 0.6);
                    padding: 8px;
                    border-radius: 8px;
                }}

                QPushButton {{
                    background-color: rgba(0, 51, 102, 1);
                    color: #ffffff;
                    font-size: 12pt;
                    font-weight: bold;
                    padding: 10px 20px;
                    border: none;                
                    border-radius: 8px;
                }}

                QPushButton:hover {{
                    background-color: rgba(0, 137, 123, 0.9); /* Slightly lighter green on hover */    
                }}
            """)

            
            
            
            if self.role == "Admin":
                self.tabs.addTab(self.tab9, "Admin Viewer")
                self.tab9_layout = QGridLayout(self.tab9)
                self.combo1 = QComboBox()
                self.combo2 = QComboBox()
                generate = QPushButton("Generate")
                generate.setFixedHeight(50)
                generate.setFont(self.my_font)
                generate.setStyleSheet("""
                    QPushButton {
                        background-color: #DC143C; /* Crimson */
                        color: white;
                        font-size: 16px;
                        font-weight: bold;
                        padding: 10px 20px;
                        border: none;
                        border-radius: 8px;
                    }
                    QPushButton:hover {
                        background-color: #FF6347; /* Tomato Red */
                    }
                """)
                generate.clicked.connect(self.admin_gui)
                self.webview_admin = QWebEngineView()
                self.tab9_layout.addWidget(self.combo1, 0, 0)
                self.tab9_layout.addWidget(self.combo2, 0, 1)
                self.tab9_layout.addWidget(generate, 0, 2)
                self.tab9_layout.addWidget(self.webview_admin, 1, 0, 1, 3)

            self.tabs.currentChanged.connect(self.on_tab_change)
            # Add the tab widget to the main layout
            self.layout.addWidget(self.tabs)
        except Exception as e:
            print(e)

    def carbonCalculator_func(self, module: str):
        if module == "Details":
            mod = str
            if self.individual_rbtn.isChecked():
                mod = "Individual"
            elif self.sbusiness_rbtn.isChecked():
                mod = "Small Business Firm"
            elif self.bbusiness_rbtn.isChecked():
                mod = "Big Business Firm"
            self.carbonCalculator["Details"].update(
                {"Username": self.username, "Module": mod, "CompanyName": self.tab1_name_input.text(), "Year": self.tab1_year_input.currentText(), "StaffHeadcount": self.tab1_staff_input.text()}) 
        elif module == "Energy":
            self.carbonCalculator["Energy"].update(
                {"Electricity": self.tab2_electricity_input.text(), "NaturalGas": self.tab2_gas_input.text(),
                 "Fuel": self.tab2_fuel_input.text()})
        elif module == "Waste":
            self.carbonCalculator["Waste"].update(
                {"Waste_generated": self.tab3_waste_generated.text(), "Waste_recycle": self.tab3_waste_recycle.text()})
        elif module == "Travel":
            self.carbonCalculator["Travel"].update(
                {"Distance": self.tab4_distance.text(), "Fuel_Efficiency": self.tab4_fuel_efficiency.text()})
        elif module == "Result":
            self.calculate()
            self.database_update()
            self.generate_feedback()

            # self.visualization([])

    def calculate(self):
        try:
            staff_headcount = int(self.carbonCalculator["Details"].get("StaffHeadcount", 1))  

            energy_result = (float(self.carbonCalculator["Energy"]["Electricity"]) * 12 * 0.0005) + (
                    float(self.carbonCalculator["Energy"]["NaturalGas"]) * 12 * 0.0053) + (
                                    float(self.carbonCalculator["Energy"]["Fuel"]) * 12 * 2.32)
            waste_result = float(self.carbonCalculator["Waste"]["Waste_generated"]) * 12 * (
                    0.57 - (float(self.carbonCalculator["Waste"]["Waste_recycle"]) / 100))
            travel_result = float(self.carbonCalculator["Travel"]["Distance"]) * (
                    1 / float(self.carbonCalculator["Travel"]["Fuel_Efficiency"]) * 2.31)
            total = energy_result+waste_result+travel_result

            per_capita_cf = total / staff_headcount if staff_headcount > 0 else 0
            self.carbonCalculator["Results"].update({"PerCapitaCF": per_capita_cf})

            self.table.setItem(0, 1, QTableWidgetItem("%.2f" % energy_result))
            self.table.setItem(1, 1, QTableWidgetItem("%.2f" % waste_result))
            self.table.setItem(2, 1, QTableWidgetItem("%.2f" % travel_result))
            self.table.setItem(3, 1, QTableWidgetItem("%.2f" % total))
            self.table.setItem(5, 1, QTableWidgetItem("%.2f" % per_capita_cf))

            # table = QTableWidget(0, 2)

            # Add the QTableWidgetItem to the table
            self.table.item(0, 1).setTextAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
            self.table.item(1, 1).setTextAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
            self.table.item(2, 1).setTextAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
            self.table.item(3, 1).setTextAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
            self.table.item(5, 1).setTextAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)


            self.carbonCalculator["Results"].update(
                {"Energy": energy_result, "Waste": waste_result, "Travel": travel_result, "Total": total, "PerCapitaCF": per_capita_cf, "StaffHeadcount": staff_headcount})
        except Exception as e:
            print(f"issue is with: {e}")







    def database_update(self):
        
        self.tab5_calculate_button.blockSignals(True)
        


        try:
            mydb = pymysql.connect(
                host=HOST,
                user=USERNAME,
                password=PASSWORD,
                database=DATABASE
            )
            mycursor = mydb.cursor()

            query = "SELECT * FROM cf_table WHERE User_Type=%s AND Name=%s AND Company_Name=%s AND Year=%s"
            values_check = (
                self.carbonCalculator["Details"].get("Module"),
                self.carbonCalculator["Details"].get("Username"),
                self.carbonCalculator["Details"].get("CompanyName"),
                self.carbonCalculator["Details"].get("Year")
            )
            mycursor.execute(query, values_check)
            result = mycursor.fetchone()
            status = True
            if result:
                sr_no = result[0]
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Question)
                msg_box.setWindowTitle("Confirmation")
                msg_box.setText(
                    "Data already exist for the user with same year, company name and user type\nIf you proceed with yes the data will be overwritten.\nDo you want to proceed?")
                msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                msg_box.setDefaultButton(QMessageBox.No)

                # Show the message box and capture the response
                response = msg_box.exec_()
                # Handle the response
                if response == QMessageBox.Yes:
                    # Perform the update operation
                    avg_query = "SELECT * FROM eu_avgcf_table WHERE Year=%s"
                    mycursor.execute(avg_query, (self.carbonCalculator["Details"].get("Year"),))
                    result_avg = mycursor.fetchone()
                    self.carbonCalculator["Details"]["avg_europe"] = result_avg[2]

                    update_query = """
                            UPDATE cf_table
                            SET Ele_Energy=%s, Nat_Gas_Energy=%s, Fuel_Energy=%s, Total_Energy=%s,
                                Generated_Waste=%s, Recycled_Waste=%s, Total_Waste=%s,
                                Kilometer_Travel=%s, AvgFuelEff_Travel=%s, Total_Travel=%s, Total_CF=%s, Europe_Avg_CF=%s, staff_headcount=%s, per_capita_cf=%s
                            WHERE Sr_No=%s
                            """
                    values_update = (
                        self.carbonCalculator["Energy"].get("Electricity"),
                        self.carbonCalculator["Energy"].get("NaturalGas"),
                        self.carbonCalculator["Energy"].get("Fuel"),
                        self.carbonCalculator["Results"].get("Energy"),
                        self.carbonCalculator["Waste"].get("Waste_generated"),
                        self.carbonCalculator["Waste"].get("Waste_recycle"),
                        self.carbonCalculator["Results"].get("Waste"),
                        self.carbonCalculator["Travel"].get("Distance"),
                        self.carbonCalculator["Travel"].get("Fuel_Efficiency"),
                        self.carbonCalculator["Results"].get("Travel"),
                        self.carbonCalculator["Results"].get("Total"),
                        self.carbonCalculator["Details"].get("avg_europe"),
                        self.carbonCalculator["Details"].get("StaffHeadcount"),
                        self.carbonCalculator["Results"].get("PerCapitaCF"),
                        sr_no
                    )
                    try:
                        mycursor.execute(update_query, values_update)
                        mydb.commit()
                        print("Data has been overwritten successfully.")
                    except mdb.Error as e:
                        print(f"Error updating data: {e}")
                    status = True
                elif response == QMessageBox.No:
                    status = False
                    print("Operation cancelled by the user.")
            else:
                avg_query = "SELECT * FROM eu_avgcf_table WHERE Year=%s"
                mycursor.execute(avg_query, (self.carbonCalculator["Details"].get("Year"),))
                result_avg = mycursor.fetchone()
                self.carbonCalculator["Details"]["avg_europe"] = result_avg[2]

                insert_query = ("INSERT INTO cf_table (User_Type, Name, Company_Name, Year, Country, Ele_Energy, Nat_Gas_Energy, Fuel_Energy, Total_Energy, Generated_Waste, Recycled_Waste, Total_Waste, Kilometer_Travel, AvgFuelEff_Travel, Total_Travel, Total_CF, Europe_Avg_CF, staff_headcount, per_capita_cf) "
                                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
                values_insert = (
                    self.carbonCalculator["Details"].get("Module"),
                    self.carbonCalculator["Details"].get("Username"),
                    self.carbonCalculator["Details"].get("CompanyName"),
                    self.carbonCalculator["Details"].get("Year"),
                    self.carbonCalculator["Details"].get("Country"),
                    self.carbonCalculator["Energy"].get("Electricity"),
                    self.carbonCalculator["Energy"].get("NaturalGas"),
                    self.carbonCalculator["Energy"].get("Fuel"),
                    self.carbonCalculator["Results"].get("Energy"),
                    self.carbonCalculator["Waste"].get("Waste_generated"),
                    self.carbonCalculator["Waste"].get("Waste_recycle"),
                    self.carbonCalculator["Results"].get("Waste"),
                    self.carbonCalculator["Travel"].get("Distance"),
                    self.carbonCalculator["Travel"].get("Fuel_Efficiency"),
                    self.carbonCalculator["Results"].get("Travel"),
                    self.carbonCalculator["Results"].get("Total"),
                    self.carbonCalculator["Details"].get("avg_europe"),
                    self.carbonCalculator["Details"].get("StaffHeadcount"),
                    self.carbonCalculator["Results"].get("PerCapitaCF")  # Add this line
                )
                mycursor.execute(insert_query, values_insert)
                mydb.commit()
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Information)
                msg_box.setWindowTitle("Database Update")
                msg_box.setText("Data recorded successfully")
                msg_box.exec_()
                status = True
                print("Data recorded successfully")

        except mdb.Error as e:
            print(f"Database not connected: {e}")
        finally:
            mycursor.close()
            mydb.close()
            if status:
                self.table.setItem(4, 1, QTableWidgetItem("%.2f" % self.carbonCalculator["Details"].get("avg_europe")))
                self.table.item(4, 1).setTextAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)

                self.visualization([self.carbonCalculator["Results"].get("Total"), self.carbonCalculator["Details"].get("avg_europe")])
                self.visualization_sub([self.carbonCalculator["Results"].get("Energy"), self.carbonCalculator["Results"].get("Waste"),
                     self.carbonCalculator["Results"].get("Travel")])

        self.tab5_calculate_button.blockSignals(False)

    
    
    
    
    
    
    
    def visualization(self, values:list):
        try:
            # Create a bar plot
            categories = ["Total Carbon Footprint\n(KgCO2)", "Europe Avg.Carbon Footprint\n(KgCO2)"]  # Labels for each bar
            # values = [10, 15]  # Heights of each bar

            fig = go.Figure(data=[go.Bar(x=categories, y=values)])
            fig.update_layout(title={
            'text': 'Total Carbon Footprint vs Europe Average Carbon Footprint',
            'x': 0.5,  # Center the title
            'xanchor': 'center'
            }, yaxis_title='KgCO2')

            # Save the plot as a PNG file for PDF
            self.total_cf_graph_path = os.path.join(tempfile.gettempdir(), "total_cf_graph.png")
            fig.write_image(self.total_cf_graph_path, width=1200, height=800, scale=2)  # Higher resolution


            # Save the plot as an HTML file in a temporary location
            temp_html_path = tempfile.mktemp(suffix='.html')
            fig.write_html(temp_html_path)


            self.web_view.setUrl(QUrl.fromLocalFile(temp_html_path))
        except Exception as e:
            print(e)
            pass

    def visualization_sub(self, values_sub:list):
        try:
            # Create a bar plot
            categories = ["Energy", "Waste", "Business Travel"]  # Labels for each bar
            # values = [10, 15]  # Heights of each bar

            fig = go.Figure(data=[go.Bar(x=categories, y=values_sub)])
            fig.update_layout(title={
                'text': 'Energy vs Waste vs Business travel',
                'x': 0.5,  # Center the title
                'xanchor': 'center'
            }, yaxis_title='KgCO2')

            # Save the plot as a PNG file for PDF
            self.sub_graph_path = os.path.join(tempfile.gettempdir(), "sub_graph.png")
            fig.write_image(self.sub_graph_path, width=1200, height=800, scale=2)  # Higher resolution


            # Save the plot as an HTML file in a temporary location
            temp_html_path = tempfile.mktemp(suffix='.html')
            fig.write_html(temp_html_path)

            self.web_view_sub.setUrl(QUrl.fromLocalFile(temp_html_path))
        except Exception as e:
            print(e)
            pass

    def visualization_comparison(self):
        try:
            mydb = pymysql.connect(
                host=HOST,
                user=USERNAME,
                password=PASSWORD,
                database=DATABASE
            )
            mycursor = mydb.cursor()

            query = "SELECT Total_CF, Year FROM cf_table WHERE User_Type=%s AND Name=%s AND Company_Name=%s"
            values_check = (
                self.carbonCalculator["Details"].get("Module"),
                self.carbonCalculator["Details"].get("Username"),
                self.carbonCalculator["Details"].get("CompanyName")
            )
            mycursor.execute(query, values_check)
            result = mycursor.fetchall()
            total_cf_values = [row[0] for row in result]  # Extract values from the result set
            years = [str(row[1]) for row in result]

            fig = go.Figure(data=[go.Bar(x=years, y=total_cf_values)])
            fig.update_layout(title={
            'text': 'Total Carbon Footprints of all available Years',
            'x': 0.5,  # Center the title
            'xanchor': 'center'
            }, yaxis_title='Total Carbon Footprint KgCO2')


            # Save the plot as a PNG file for the PDF
            self.comparison_graph_path = os.path.join(tempfile.gettempdir(), "comparison_graph.png")
            fig.write_image(self.comparison_graph_path, width=1200, height=800, scale=2) 


            # Save the plot as an HTML file in a temporary location
            temp_html_path = tempfile.mktemp(suffix='.html')
            fig.write_html(temp_html_path)
            self.web_view2.setUrl(QUrl.fromLocalFile(temp_html_path))

            
        except mdb.Error as e:
            print(f"Database not connected: {e}")
        finally:
            mycursor.close()
            mydb.close()

    def switchTab(self, index):
        self.tabs.setCurrentIndex(index)

    def on_tab_change(self, index):
        if index == 8:
            try:
                self.combo1.clear()
                self.combo2.clear()
                mydb = pymysql.connect(
                    host=HOST,
                    user=USERNAME,
                    password=PASSWORD,
                    database=DATABASE
                )
                mycursor = mydb.cursor()

                query = "SELECT User_Type, Year FROM cf_table"
                mycursor.execute(query)
                result = mycursor.fetchall()
                usertypes = {row[0] for row in result}  # Extract values from the result set
                years = {str(row[1]) for row in result}
                self.combo1.addItems(list(usertypes))
                self.combo2.addItems(list(years))
            except Exception as e:
                print(e)
            finally:
                mycursor.close()
                mydb.close()

    def admin_gui(self):
        try:
            mydb = pymysql.connect(
                host=HOST,
                user=USERNAME,
                password=PASSWORD,
                database=DATABASE
            )
            mycursor = mydb.cursor()

            query = "SELECT Company_Name, Total_CF FROM cf_table where User_Type=%s AND Year=%s"
            values_check = (
                self.combo1.currentText(),
                self.combo2.currentText()
            )
            mycursor.execute(query, values_check)
            result = mycursor.fetchall()
            companyname = [row[0] for row in result]  # Extract values from the result set
            totalCF = [str(row[1]) for row in result]

            fig = go.Figure(data=[go.Bar(x=companyname, y=totalCF)])
            fig.update_layout(title={
                'text': 'Carbon Footprints comparison of User Types for particular Year',
                'x': 0.5,  # Center the title
                'xanchor': 'center'
            }, yaxis_title='Total Carbon Footprint KgCO2')

            # Save the plot as an HTML file in a temporary location
            temp_html_path = tempfile.mktemp(suffix='.html')
            fig.write_html(temp_html_path)

            self.webview_admin.setUrl(QUrl.fromLocalFile(temp_html_path))
        except mdb.Error as e:
            print(f"Database not connected: {e}")
        finally:
            mycursor.close()
            mydb.close()




if __name__ == "__main__":
  windll.shcore.SetProcessDpiAwareness(0)
  app = QApplication(sys.argv)
  window = CarbonFootprintCalculator("SM", "User")
  window.show()
  sys.exit(app.exec_())