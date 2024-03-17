import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QLineEdit, QGridLayout, \
    QSpacerItem, QSizePolicy, QComboBox, QMessageBox
from PyQt5.QtCore import QTimer, QTime, pyqtSignal
from PyQt5.QtGui import QGuiApplication
import random

from digital_clock import DigitalClock
from elapsed_counter import ElapsedCounter
from action_counter import ActionCounter

class EasyLab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Initialize hash label, line edit, and buttons
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

        # Initialize clock
        self.clock = DigitalClock()

        # Initialize time counters
        self.action_label = QLabel("Next Action in:")
        self.action_counter = QTimer(self)
        self.elapsed_label = QLabel("Elapsed Time:")
        self.elapsed_counter = ElapsedCounter()

        # Initialize table1 labels and line edits
        self.table1_label = QLabel("Table 1 - Inhaler Usage Times")
        self.t1_col1_label = QLabel("Time [minutes]")
        self.t1_col2_label = QLabel("Clock time [hh:mm:ss]")
        self.t1_col1_line_edits = [QLineEdit() for _ in range(6)]
        self.t1_col2_line_edits = [QLineEdit() for _ in range(6)]
        for line_edit in self.t1_col1_line_edits + self.t1_col2_line_edits:
            line_edit.setReadOnly(True)

        # Initialize table2 labels and line edits
        self.table2_label = QLabel("Table 2 - Inhaler Holding Times")
        self.t2_col1_label = QLabel("Time [minutes]")
        self.t2_col2_label = QLabel("Clock time [hh:mm:ss]")
        self.t2_col1_line_edits = [QLineEdit() for _ in range(6)]
        self.t2_col2_line_edits = [QLineEdit() for _ in range(6)]
        for line_edit in self.t2_col1_line_edits + self.t2_col2_line_edits:
            line_edit.setReadOnly(True)

        # Initialize buttons
        self.rand_button = QPushButton("Randomize Times")
        self.export_button = QPushButton("Export Data")
        self.start_stop_button = QPushButton("Start Experiment")

        # Keep track of message boxes
        self.message_box = None

        # Setup the UI
        self.setup_ui()

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

        # Create a grid layout for the top section
        top_layout = QGridLayout()

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
        top_layout.addLayout(hash_layout, 0, 0)

        # Setup experiment type label and dropdown
        experiment_layout = QHBoxLayout()
        self.experiment_label.setFixedWidth(130)    # Set the width for all labels to align them
        experiment_layout.addWidget(self.experiment_label)
        experiment_layout.addWidget(self.experiment_dropdown)
        experiment_layout.addStretch()
        top_layout.addLayout(experiment_layout, 1, 0)

        # Setup inhaler type label and dropdown
        inhaler_layout = QHBoxLayout()
        self.inhaler_label.setFixedWidth(130)    # Set the width for all labels to align them
        inhaler_layout.addWidget(self.inhaler_label)
        inhaler_layout.addWidget(self.inhaler_dropdown)
        inhaler_layout.addStretch()
        top_layout.addLayout(inhaler_layout, 2, 0)

        # Setup the clock
        top_layout.addWidget(self.clock, 0, 2, 3, 1)

        # Add the top layout to the main layout
        layout.addLayout(top_layout)

        # Add space between the labels and the counters
        layout.addStretch()

        # Set the counters to display time in mm:ss format
        # self.elapsed_counter.

        # Add the counters to the layout
        counter_layout = QHBoxLayout()
        counter_layout.addWidget(self.action_label)
        # counter_layout.addWidget(self.next_action_counter)
        counter_layout.addWidget(self.elapsed_label)
        counter_layout.addWidget(self.elapsed_counter)
        layout.addLayout(counter_layout)
        layout.addStretch()

        # Setup table1 labels and line edits
        layout.addWidget(self.table1_label)
        table1_layout = QGridLayout()
        table1_layout.addWidget(self.t1_col1_label, 0, 0)
        table1_layout.addWidget(self.t1_col2_label, 0, 1)
        for col1_line_edit, col2_line_edit in zip(self.t1_col1_line_edits, self.t1_col2_line_edits):
            table1_layout.addWidget(col1_line_edit)
            table1_layout.addWidget(col2_line_edit)
        layout.addLayout(table1_layout)
        layout.addStretch()

        # Setup table2 labels and line edits
        layout.addWidget(self.table2_label)
        table2_layout = QGridLayout()
        table2_layout.addWidget(self.t2_col1_label, 0, 0)
        table2_layout.addWidget(self.t2_col2_label, 0, 1)
        for col1_line_edit, col2_line_edit in zip(self.t2_col1_line_edits, self.t2_col2_line_edits):
            table2_layout.addWidget(col1_line_edit)
            table2_layout.addWidget(col2_line_edit)
        layout.addLayout(table2_layout)
        layout.addStretch()

        # Setup randomization and export buttons
        button_layout = QHBoxLayout()
        self.rand_button.setFixedHeight(50)
        self.export_button.setFixedHeight(50)
        button_layout.addWidget(self.rand_button)
        button_layout.addWidget(self.export_button)
        layout.addLayout(button_layout)

        # Setup start_stop buttons
        self.start_stop_button.setFixedHeight(50)
        layout.addWidget(self.start_stop_button)

        # Set the layout for the window
        self.setLayout(layout)

        # Connect signals and slots
        self.hash_edit_button.clicked.connect(self.edit_hash)
        self.hash_gen_button.clicked.connect(self.generate_hash)
        self.experiment_dropdown.currentIndexChanged.connect(self.on_experiment_changed)
        self.elapsed_counter.time_reached.connect(self.stop_experiment)
        self.rand_button.clicked.connect(self.generate_times)
        self.export_button.clicked.connect(self.export_data)
        self.start_stop_button.clicked.connect(self.on_start_stop_button_clicked)


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

    def on_experiment_changed(self, index):
        selected_text = self.experiment_dropdown.itemText(index)
        if selected_text == "Option 1":
            # Do something for Option 1
            pass
        elif selected_text == "Option 2":
            # Do something for Option 2
            pass
    
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

    def calculate_clock_times(self):
        # Add code to generate clock times from the usage and hold times
        pass
    
    def export_data(self):
        # Add code to export data to a Word file
        pass

    def on_start_stop_button_clicked(self):
        if self.start_stop_button.text() == "Start Experiment":
            self.start_experiment()
        else:
            self.message_box = QMessageBox(self)
            self.message_box.setWindowTitle("Stop Experiment")
            self.message_box.setText("Stopping the experiment will stop all timers. Are you sure you want to stop the experiment?")
            self.message_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            self.message_box.setDefaultButton(QMessageBox.No)
            reply = self.message_box.exec_()
            if reply == QMessageBox.Yes:
                self.stop_experiment()

    def start_experiment(self):
        # Ensure tables are not empty
        # if not self.t1_col1_line_edits[0].text():
        #     QMessageBox.warning(self, "Missing Times", "Please generate times before starting the experiment.")
        #     return
        
        # Change the button text
        self.start_stop_button.setText("Stop Experiment")

        # Start the timers
        self.elapsed_counter.display("00:00")  # Initial display
        time_until_next_second = 1000 - QTime.currentTime().msec()    # Ensure that the timers are displayed exactly on every second-change
        QTimer.singleShot(time_until_next_second, lambda: (self.elapsed_counter.start()))    # Start the elapsed counter and the cation counter


    def stop_experiment(self):
        # If any, close the message box
        if self.message_box:
            self.message_box.close()
            self.message_box = None

        # Change the button text
        self.start_stop_button.setText("Start Experiment")

        # Stop the timers
        self.elapsed_counter.stop()

        # Display a message
        #? If wished, make the tables writeable now
        QMessageBox.information(self, "Experiment Stopped", "The experiment has been stopped. You can now export the data.")


def main():
    # Create the application
    app = QApplication(sys.argv)
    experiment_app = EasyLab()

    # Exit the application
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()