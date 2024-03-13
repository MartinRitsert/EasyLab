import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QLineEdit, QGridLayout, QTimeEdit, \
    QSpacerItem, QSizePolicy
from PyQt5.QtCore import QTimer, QTime
from PyQt5.QtGui import QGuiApplication
import random


class ExperimentApp(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize hash and experiment type labels
        self.hash_label = QLabel("Hash:")
        self.experiment_type_label = QLabel("Experiment Type:")

        # Initialize time counters
        self.elapsed_time_counter = QTimeEdit(QTime(0, 0))
        self.next_action_counter = QTimeEdit(QTime(0, 0))

        # Initialize table labels and text boxes
        self.usage_label = QLabel("Inhaler Usage")
        self.col1_label = QLabel("Time [minutes]")
        self.col2_label = QLabel("Clock time [hh:mm:ss]")
        self.col1_text_boxes = [QLineEdit() for _ in range(6)]
        self.col2_text_boxes = [QLineEdit() for _ in range(6)]

        # Initialize buttons
        self.start_button = QPushButton("Start Experiment")
        self.end_button = QPushButton("End Experiment")
        self.export_button = QPushButton("Export Data")

        self.setup_ui()
        self.generate_times()

    def setup_ui(self):
        #* Setup the window
        # Get screen resolution
        screen = QGuiApplication.primaryScreen().geometry()
        screenWidth = screen.width()
        screenHeight = screen.height()

        # Window size
        winWidth = int(screenWidth // 1.4)
        winHeight = int(screenHeight // 1.6)

        # Calculate window position
        x = (screenWidth - winWidth) // 2
        y = (screenHeight - winHeight) // 2

        # Set window size and position
        self.setGeometry(x, y, winWidth, winHeight)
        self.setWindowTitle("EasyLab")
        self.show()


        #* Setup the widgets
        # Create layouts
        layout = QGridLayout()

        # Setup hash and experiment type labels
        layout.addWidget(self.hash_label, 0, 0)
        layout.addWidget(self.experiment_type_label, 0, 1)

        # Set the counters to read-only so the user can't edit them
        self.elapsed_time_counter.setReadOnly(True)
        self.next_action_counter.setReadOnly(True)

        # Set the counters to display time in mm:ss format
        self.elapsed_time_counter.setDisplayFormat("mm:ss")
        self.next_action_counter.setDisplayFormat("mm:ss")

        # Add the counters to the layout
        layout.addWidget(QLabel("Elapsed Time"), 1, 0)
        layout.addWidget(self.elapsed_time_counter, 1, 1)
        layout.addWidget(QLabel("Next Action in"), 1, 2)
        layout.addWidget(self.next_action_counter, 1, 3)

        # Create a QTimer to update the counters every second
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_counters)

        # Setup table labels and text boxes
        layout.addWidget(self.usage_label, 2, 0)
        layout.addWidget(self.col1_label, 3, 0)
        layout.addWidget(self.col2_label, 3, 1)
        for i, usage_text_box in enumerate(self.col1_text_boxes):
            layout.addWidget(usage_text_box, i+4, 0)
        for i, clock_text_box in enumerate(self.col2_text_boxes):
            layout.addWidget(clock_text_box, i+4, 1)

        # Add space between the table and the buttons
        spacer = QSpacerItem(0, 40, QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addItem(spacer, 10, 0)

        # Setup buttons
        self.start_button.setFixedHeight(50)
        self.end_button.setFixedHeight(50)
        self.export_button.setFixedHeight(50)
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.end_button)
        button_layout.addWidget(self.export_button)
        layout.addLayout(button_layout, 11, 0, 1, 2)

        # Set the layout for the window
        self.setLayout(layout)

        # Connect signals and slots
        self.start_button.clicked.connect(self.start_experiment)
        self.end_button.clicked.connect(self.end_experiment)
        self.export_button.clicked.connect(self.export_data)

    def generate_times(self):
        # Generate lists calculated time & duration values
        usage_time_points = list()
        hold_time_points = list()
        hold_durations = list()

        # Calculate usage time points and hold time points
        for i in range(0, 60, 10):

            # Calculate usage time point
            usage_time_point = i + random.randint(0, 10)
            while(usage_time_point >= i + 10):
                usage_time_point = i + random.randint(0, 10)

            # Calculate hold time point and hold duration
            hold_time_point = usage_time_point
            hold_duration = random.randint(0, 60)
            while hold_time_point == usage_time_point or hold_time_point + (hold_duration / 60) >= i + 10:
                hold_time_point = i + random.randint(0, 10)
                hold_duration = random.randint(0, 60)
            
            # Append the calculated values to the lists
            usage_time_points.append(usage_time_point)
            hold_time_points.append(hold_time_point)
            hold_durations.append(hold_duration)
        
        # Print the calculated values
        for usage_time_point in usage_time_points:
            print(usage_time_point)
        for hold_time_point, hold_duration in zip(hold_time_points, hold_durations):
            print(hold_time_point, "(", hold_duration, "seconds )")

    def start_experiment(self):
        # Start the timer
        self.timer.start(1000)

    def end_experiment(self):
        # Add code to end the experiment, remind user to export data, etc.
        pass

    def export_data(self):
        # Add code to export data to a Word file
        pass

    def update_counters(self):
        # Update the elapsed time counter
        elapsed_time = self.elapsed_time_counter.time().addSecs(1)
        self.elapsed_time_counter.setTime(elapsed_time)

        # Update the next action counter
        next_action = self.next_action_counter.time().addSecs(-1)
        self.next_action_counter.setTime(next_action)

        # Check if the next action counter has reached 0
        if next_action == QTime(0, 0):
            # Add code to display a notification, play a sound, etc.
            pass


def main():
    # Create the application
    app = QApplication(sys.argv)
    experiment_app = ExperimentApp()

    # Exit the application
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()