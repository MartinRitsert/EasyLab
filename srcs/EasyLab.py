import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import QTimer
import random

class ExperimentApp(QWidget):
    def __init__(self):
        super().__init__()

        self.hash_label = QLabel("Hash:")
        self.experiment_type_label = QLabel("Experiment Type:")
        self.times_table = QTableWidget()
        self.start_button = QPushButton("Start Experiment")
        self.export_button = QPushButton("Export Data")
        self.end_button = QPushButton("End Experiment")

        self.setup_ui()
        self.generate_times()

    def setup_ui(self):
        layout = QVBoxLayout()

        layout.addWidget(self.hash_label)
        layout.addWidget(self.experiment_type_label)
        layout.addWidget(self.times_table)
        layout.addWidget(self.start_button)
        layout.addWidget(self.export_button)
        layout.addWidget(self.end_button)

        self.setLayout(layout)

        self.start_button.clicked.connect(self.start_experiment)
        self.export_button.clicked.connect(self.export_data)
        self.end_button.clicked.connect(self.end_experiment)

        self.setWindowTitle("Experiment Program")
        self.setGeometry(100, 100, 600, 400)

    def generate_times(self):
        # Add your existing time generation code here and populate the times_table
        pass

    def start_experiment(self):
        # Add code to start the experiment, display countdown, etc.
        pass

    def export_data(self):
        # Add code to export data to a Word file
        pass

    def end_experiment(self):
        # Add code to end the experiment, remind user to export data, etc.
        pass

if __name__ == '__main__':
    # Create the application
    app = QApplication(sys.argv)
    experiment_app = ExperimentApp()

    # Get screen resolution
    screen = app.primaryScreen()
    rect = screen.availableGeometry()
    screenWidth = rect.width()
    screenHeight = rect.height()

    # Window size
    winWidth = int(screenWidth // 1.4)
    winHeight = int(screenHeight // 1.6)

    # Calculate window position
    x = (screenWidth - winWidth) // 2
    y = (screenHeight - winHeight) // 2

    # Set window size and position
    experiment_app.setGeometry(x, y, winWidth, winHeight)
    experiment_app.setWindowTitle("EasyLab")
    experiment_app.show()

    # Run the application
    experiment_app.show()
    sys.exit(app.exec_())
