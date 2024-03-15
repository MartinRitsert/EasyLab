import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QLineEdit, QGridLayout, QTimeEdit, \
    QSpacerItem, QSizePolicy, QComboBox
from PyQt5.QtCore import QTimer, QTime
from PyQt5.QtGui import QGuiApplication
import random


class ExperimentApp(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize hash label, line edit, and button
        self.hash_label = QLabel("Hash:")
        self.hash_line_edit = QLineEdit()
        self.hash_line_edit.setReadOnly(True)
        self.hash_edit_button = QPushButton("Edit Hash")
        self.hash_gen_button = QPushButton("Generate Hash")

        # Initialize experiment type label and dropdown
        self.experiment_label = QLabel("Experiment Type:")
        self.experiment_dropdown = QComboBox()
        self.experiment_dropdown.addItem("Experiment 1: Inhaler Usage")
        self.experiment_dropdown.addItem("Experiment 2: Inhaler Dumping")

        # Initialize inhaler type label and dropdown
        self.inhaler_label = QLabel("Inahler Type:")
        self.inhaler_dropdown = QComboBox()
        self.inhaler_dropdown.addItem("pMDI")
        self.inhaler_dropdown.addItem("Turbohaler")
        self.inhaler_dropdown.addItem("Diskus")

        # Initialize time counters
        self.elapsed_time_label = QLabel("Elapsed Time")
        self.elapsed_time_counter = QTimeEdit(QTime(0, 0))
        self.next_action_label = QLabel("Next Action in")
        self.next_action_counter = QTimeEdit(QTime(0, 0))

        # Initialize table labels and line edits
        self.usage_label = QLabel("Inhaler Usage")
        self.col1_label = QLabel("Time [minutes]")
        self.col2_label = QLabel("Clock time [hh:mm:ss]")
        self.col1_line_edits = [QLineEdit() for _ in range(6)]
        self.col2_line_edits = [QLineEdit() for _ in range(6)]

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
        # Create the main layout
        layout = QVBoxLayout()

        # Setup hash label, line edit, and buttons
        hash_layout = QHBoxLayout()
        self.hash_label.setFixedWidth(130)    # Set the width for all labels to align them
        self.hash_line_edit.setMaxLength(10)    # Set the maximum number of characters
        metrics = self.hash_line_edit.fontMetrics()    # Get the font metrics
        width = metrics.boundingRect("Z" * 13).width()    # Calculate the width of 10 characters
        self.hash_line_edit.setFixedWidth(width)    # Set the width of the line edit
        metrics = self.hash_edit_button.fontMetrics()    # Get the font metrics
        width = metrics.boundingRect("Confirm Hash").width()    # Calculate the width of the button
        width += 40    # Add some extra width
        self.hash_edit_button.setFixedWidth(width)    # Set the width of the button

        hash_layout.addWidget(self.hash_label)
        # spacer = QSpacerItem(100, 0, QSizePolicy.Fixed, QSizePolicy.Minimum)
        # hash_layout.addItem(spacer)
        hash_layout.addWidget(self.hash_line_edit)
        hash_layout.addWidget(self.hash_edit_button)
        hash_layout.addWidget(self.hash_gen_button)
        hash_layout.addStretch()
        layout.addLayout(hash_layout)

        # Setup experiment type label and dropdown
        experiment_layout = QHBoxLayout()
        self.experiment_label.setFixedWidth(130)    # Set the width for all labels to align them
        experiment_layout.addWidget(self.experiment_label)
        experiment_layout.addWidget(self.experiment_dropdown)
        experiment_layout.addStretch()
        layout.addLayout(experiment_layout)

        # Setup inhaler type label and dropdown
        inhaler_layout = QHBoxLayout()
        self.inhaler_label.setFixedWidth(130)    # Set the width for all labels to align them
        inhaler_layout.addWidget(self.inhaler_label)
        inhaler_layout.addWidget(self.inhaler_dropdown)
        inhaler_layout.addStretch()
        layout.addLayout(inhaler_layout)

        # Add space between the labels and the counters
        layout.addStretch()

        # Set the counters to read-only so the user can't edit them
        self.elapsed_time_counter.setReadOnly(True)
        self.next_action_counter.setReadOnly(True)

        # Set the counters to display time in mm:ss format
        self.elapsed_time_counter.setDisplayFormat("mm:ss")
        self.next_action_counter.setDisplayFormat("mm:ss")

        # Add the counters to the layout
        counter_layout = QHBoxLayout()
        counter_layout.addWidget(self.elapsed_time_label)
        counter_layout.addWidget(self.elapsed_time_counter)
        counter_layout.addWidget(self.next_action_label)
        counter_layout.addWidget(self.next_action_counter)
        layout.addLayout(counter_layout)
        layout.addStretch()

        # Create a QTimer to update the counters every second
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_counters)

        # Setup table labels and line edits
        layout.addWidget(self.usage_label)
        table_layout = QGridLayout()
        table_layout.addWidget(self.col1_label, 0, 0)
        table_layout.addWidget(self.col2_label, 0, 1)
        for col1_line_edit, col2_line_edit in zip(self.col1_line_edits, self.col2_line_edits):
            table_layout.addWidget(col1_line_edit)
            table_layout.addWidget(col2_line_edit)
        layout.addLayout(table_layout)
        layout.addStretch()

        # Setup start, end and export buttons
        button_layout = QHBoxLayout()
        self.start_button.setFixedHeight(50)
        self.end_button.setFixedHeight(50)
        self.export_button.setFixedHeight(50)
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.end_button)
        button_layout.addWidget(self.export_button)
        layout.addLayout(button_layout)

        # Set the layout for the window
        self.setLayout(layout)

        # Connect signals and slots
        self.hash_edit_button.clicked.connect(self.edit_hash)
        self.hash_gen_button.clicked.connect(self.generate_hash)
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

    def edit_hash(self):
        if self.hash_line_edit.isReadOnly():
            self.hash_edit_button.setText("Confirm Hash")
            self.hash_line_edit.setReadOnly(False)
            self.hash_line_edit.setFocus()
        else:
            self.hash_edit_button.setText("Edit Hash")
            self.hash_line_edit.setReadOnly(True)
    
    def generate_hash(self):
        # Add code to generate a hash
        pass
    
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