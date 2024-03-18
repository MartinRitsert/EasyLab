import sys
import random
import string

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QLineEdit, QGridLayout, \
    QSpacerItem, QSizePolicy, QComboBox, QMessageBox
from PyQt5.QtCore import QTimer, QTime, pyqtSignal
from PyQt5.QtGui import QGuiApplication

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
        #TODO: Implement the action happening on changing the experiment (e.g. reset the line edits, change affected labels, etc.)

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
        self.action_counter = ActionCounter()
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

        # Initialize lists for the times
        # Initialize lists for times points, durations and clock times
        self.usage_time_points = list()
        self.usage_clock_times = list()
        self.dump_time_points = list()
        self.dump_durations = list()
        self.dump_clock_times = list()
        self.hold_time_points = list()
        self.hold_durations = list()
        self.hold_clock_times = list()

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
        counter_layout.addWidget(self.action_counter)
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

        # Setup start_stop button
        self.start_stop_button.setFixedHeight(50)
        layout.addWidget(self.start_stop_button)

        # Set the layout for the window
        self.setLayout(layout)

        # Connect signals and slots
        self.hash_edit_button.clicked.connect(self.edit_hash)
        self.hash_gen_button.clicked.connect(self.generate_hash)
        self.experiment_dropdown.currentIndexChanged.connect(self.on_experiment_changed)
        self.elapsed_counter.time_reached.connect(self.stop_experiment)
        self.rand_button.clicked.connect(self.on_rand_button_clicked)
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
        if self.hash_line_edit.text():
            reply = QMessageBox.warning(self, "Generate New Hash", "Are you sure you want to replace the current hash with a new one?", \
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.No:
                return
        characters = string.ascii_letters + string.digits  # a-z, A-Z, 0-9
        hash = ''.join(random.choice(characters) for _ in range(10))
        self.hash_line_edit.setText(hash)

    def on_experiment_changed(self, index):
        selected_text = self.experiment_dropdown.itemText(index)
        if selected_text == "Option 1":
            # Do something for Option 1
            pass
        elif selected_text == "Option 2":
            # Do something for Option 2
            pass
    def on_rand_button_clicked(self):
        # If experiment is running, return
        if self.start_stop_button.text() == "Stop Experiment":
            QMessageBox.warning(self, "Experiment Running", "Cannot generate new times during an active experiment. \
                                Please stop the experiment before generating new times.")
            return
        if self.experiment_dropdown.currentText() == "Experiment 1: Inhaler Usage":
            self.generate_times_e1()
        elif self.experiment_dropdown.currentText() == "Experiment 2: Inhaler Dumping":
            self.generate_times_e2()
        else:
            QMessageBox.warning(self, "No Experiment Selected", "Please select an experiment type before generating times.")

    def generate_times_e1(self):
        #! Assumption 1: The times must be so that they begin and end inside the same 10 minute intervall
            #! Assumption 1.1: Between start of inhalation and end of current intervall, there must be at least 60 seconds 
                #! Attention: Especially this one means discrimination as no inhalation starts between x9:xx and x9:59 ever!
            #! Assumption 1.2: Between end of holding and end of current intervall, there must be at least 1 second
        #! Assumption 2: The times must be so that actions do not overlap
            #! Assumption 2.1: Between start of inhalation and start of next action, there must be at least 60 seconds
            #! Assumption 2.2: Between end of holding and start of next action, there must be at least 1 second
        #! Assumption 3: The holding duration must be at least 1 second
        #? Question1: Are the assumptions okay?
        #? Question2: Holding duration [0, 60] okay?

        # Ask for confirmation of deleting current times
        if self.t1_col1_line_edits[0].text():
            reply = QMessageBox.warning(self, "Delete Data", 'This will delete all "time points and clock times" data. Are you sure that you want to continue?', \
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.No:
                return
        
        # Delete current times before generating new times
        self.delete_time_points()
        self.delete_clock_times()

        # Note: all times in seconds

        # Iterate over all six 10-minute intervals
        for i in range(0, 60*60, 10*60):

            # Start randomizing usage time point, hold time point and hold duration
            usage_time_point = i + random.randint(0, (10*60)-60)    # Assumption 1.1
            hold_time_point = i + random.randint(0, (10*60)-2)  # Assumption 1.2 && Assumption 3
            hold_duration = random.randint(1, 60)

            # Initialize approved to false
            approved = False

            # Recalculate times until they are approved
            while not approved:
                # Assumption 1.2
                if (hold_time_point + hold_duration) >= (i + (10*60)):
                    usage_time_point = i + random.randint(0, (10*60)-60)
                    hold_time_point = i + random.randint(0, (10*60)-2)
                    hold_duration = random.randint(1, 60)
                    continue
                # Assumption 2
                elif usage_time_point == hold_time_point or usage_time_point == (hold_time_point + hold_duration):
                    usage_time_point = i + random.randint(0, (10*60)-60)
                    hold_time_point = i + random.randint(0, (10*60)-2)
                    hold_duration = random.randint(1, 60)
                    continue
                # Assumption 2.1
                elif usage_time_point < hold_time_point and (usage_time_point + 60) > hold_time_point:
                    usage_time_point = i + random.randint(0, (10*60)-60)
                    hold_time_point = i + random.randint(0, (10*60)-2)
                    hold_duration = random.randint(1, 60)
                    continue
                # Assumption 2.2 && Assumption 3
                elif hold_time_point < usage_time_point and (hold_time_point + hold_duration + 1) > usage_time_point:
                    usage_time_point = i + random.randint(0, (10*60)-60)
                    hold_time_point = i + random.randint(0, (10*60)-2)
                    hold_duration = random.randint(1, 60)
                    continue
                else:
                    approved = True
            
            # Append the calculated values to the lists
            self.usage_time_points.append(usage_time_point)
            self.hold_time_points.append(hold_time_point)
            self.hold_durations.append(hold_duration)
        
        # Fill table1 and table2 line edits
        for index in range(6):
            # Fill table1 line edits
            minutes, seconds = divmod(self.usage_time_points[index], 60)
            self.t1_col1_line_edits[index].setText(f"{minutes:02d}:{seconds:02d}")

            # Fill table2 line edits
            minutes, seconds = divmod(self.hold_time_points[index], 60)
            self.t2_col1_line_edits[index].setText(f"{minutes:02d}:{seconds:02d} ({self.hold_durations[index]} seconds)")

    def generate_times_e2(self):
        #! Assumption 1: The times must be so that they begin and end inside the same 10 minute intervall
            #! Assumption 1.1: Between end of dumping and end of current intervall, there must be at least 1 second 
            #! Assumption 1.2: Between end of holding and end of current intervall, there must be at least 1 second
        #! Assumption 2: The times must be so that actions do not overlap
            #! Assumption 2.1: Between end of dumping and start of next action, there must be at least 1 second
            #! Assumption 2.2: Between end of holding and start of next action, there must be at least 1 second
        #! Assumption 3: The holding duration must be at least 1 second
        #? Question1: Are the assumptions okay?
        #? Question2: Holding duration [0, 60] okay?
        #TODO: Check in MS Teams: holding duration, dumping duration

        # Ask for confirmation of deleting current times
        if self.t1_col1_line_edits[0].text():
            reply = QMessageBox.warning(self, "Delete Data", 'This will delete all "time points and clock times" data. Are you sure that you want to continue?', \
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.No:
                return
        
        # Delete current times before generating new times
        self.delete_time_points()
        self.delete_clock_times()

        # Note: all times in seconds

        # Iterate over all six 10-minute intervals
        for i in range(0, 60*60, 10*60):

            # Start randomizing usage time point, hold time point and hold duration
            dump_time_point = i + random.randint(0, (10*60)-000)    # Assumption 1.1    #!Adjust
            dump_duration = random.randint(1, 60)    #!Adjust
            hold_time_point = i + random.randint(0, (10*60)-2)  # Assumption 1.2 && Assumption 3
            hold_duration = random.randint(1, 60)   #!Adjust

            # Initialize approved to false
            approved = False

            # Recalculate times until they are approved
            while not approved:
                # Assumption 1.1
                if (dump_time_point + dump_duration) >= (i + (10*60)):
                    dump_time_point = i + random.randint(0, (10*60)-60)
                    dump_duration = random.randint(1, 60)    #!Adjust
                    hold_time_point = i + random.randint(0, (10*60)-2)
                    hold_duration = random.randint(1, 60)
                    continue
                # Assumption 1.2
                if (hold_time_point + hold_duration) >= (i + (10*60)):
                    dump_time_point = i + random.randint(0, (10*60)-60)
                    dump_duration = random.randint(1, 60)    #!Adjust
                    hold_time_point = i + random.randint(0, (10*60)-2)
                    hold_duration = random.randint(1, 60)
                    continue
                # Assumption 2
                elif dump_time_point == hold_time_point or dump_time_point == (hold_time_point + hold_duration) \
                    or (dump_time_point + dump_duration) == hold_time_point or (dump_time_point + dump_duration) == (hold_time_point + hold_duration):
                    dump_time_point = i + random.randint(0, (10*60)-60)
                    dump_duration = random.randint(1, 60)    #!Adjust
                    hold_time_point = i + random.randint(0, (10*60)-2)
                    hold_duration = random.randint(1, 60)
                    continue
                # Assumption 2.1
                elif dump_time_point < hold_time_point and (dump_time_point + dump_duration + 1) > hold_time_point:
                    dump_time_point = i + random.randint(0, (10*60)-60)
                    dump_duration = random.randint(1, 60)    #!Adjust
                    hold_time_point = i + random.randint(0, (10*60)-2)
                    hold_duration = random.randint(1, 60)
                    continue
                # Assumption 2.2 && Assumption 3
                elif hold_time_point < dump_time_point and (hold_time_point + hold_duration + 1) > dump_time_point:
                    dump_time_point = i + random.randint(0, (10*60)-60)
                    dump_duration = random.randint(1, 60)    #!Adjust
                    hold_time_point = i + random.randint(0, (10*60)-2)
                    hold_duration = random.randint(1, 60)
                    continue
                else:
                    approved = True
            
            # Append the calculated values to the lists
            self.dump_time_points.append(dump_time_point)
            self.dump_durations.append(dump_duration)
            self.hold_time_points.append(hold_time_point)
            self.hold_durations.append(hold_duration)
        
        # Fill table1 and table2 line edits
        for index in range(6):
            # Fill table1 line edits
            minutes, seconds = divmod(self.dump_time_points[index], 60)
            self.t1_col1_line_edits[index].setText(f"{minutes:02d}:{seconds:02d} ({self.dump_durations[index]} seconds)")

            # Fill table2 line edits
            minutes, seconds = divmod(self.hold_time_points[index], 60)
            self.t2_col1_line_edits[index].setText(f"{minutes:02d}:{seconds:02d} ({self.hold_durations[index]} seconds)")

    def delete_time_points(self):
        # Clear all lists 
        self.usage_time_points.clear()
        self.dump_time_points.clear()
        self.dump_durations.clear()
        self.hold_time_points.clear()
        self.hold_durations.clear()

        # Clear all line edits
        for i in range(6):
            self.t1_col1_line_edits[i].clear()
            self.t2_col1_line_edits[i].clear()

    def delete_clock_times(self):
        # Clear all lists 
        self.usage_clock_times.clear()
        self.dump_clock_times.clear()
        self.hold_clock_times.clear()

        # Clear all line edits
        for i in range(6):
            self.t1_col2_line_edits[i].clear()
            self.t2_col2_line_edits[i].clear()

    def calculate_clock_times(self, current_time):
        if self.experiment_dropdown.currentText() == "Experiment 1: Inhaler Usage":
            # Calculate usage clock times
            for time_point in self.usage_time_points:
                clock_time = current_time.addSecs(time_point)
                self.usage_clock_times.append(clock_time.toString("hh:mm:ss"))

        elif self.experiment_dropdown.currentText() == "Experiment 2: Inhaler Dumping":
            # Calculate dump clock times
            for time_point in self.dump_time_points:
                clock_time = current_time.addSecs(time_point)
                self.dump_clock_times.append(clock_time.toString("hh:mm:ss"))

        # Calculate hold clock times
        for time_point in self.hold_time_points:
            clock_time = current_time.addSecs(time_point)
            self.hold_clock_times.append(clock_time.toString("hh:mm:ss"))

        # Fill table1 and table2 line edits
        for index in range(6):
            if self.experiment_dropdown.currentText() == "Experiment 1: Inhaler Usage":
                self.t1_col2_line_edits[index].setText(self.usage_clock_times[index])
            elif self.experiment_dropdown.currentText() == "Experiment 2: Inhaler Dumping":
                self.t1_col2_line_edits[index].setText(self.dump_clock_times[index])
            self.t2_col2_line_edits[index].setText(self.hold_clock_times[index])
    
    def export_data(self):
        # Add code to export data to a Word file
        pass

    def on_start_stop_button_clicked(self):
        if self.start_stop_button.text() == "Start Experiment":
            # Ensure tables are not empty
            if not self.t1_col1_line_edits[0].text():
                QMessageBox.warning(self, "Missing Times", "Please generate times before starting the experiment.")
                return
            # Ask for confirmation of deleting current times (if they exist)
            elif self.t1_col2_line_edits[0].text():
                reply = QMessageBox.warning(self, "Delete Data", 'This will delete all "clock times" data. Are you sure that you want to continue', \
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if reply == QMessageBox.No:
                    return
            self.delete_clock_times() # Delete current clock times
            self.start_experiment()
        else:
            self.message_box = QMessageBox(self)
            self.message_box.setWindowTitle("Stop Experiment")
            self.message_box.setText("Stopping the experiment will stop all timers. Are you sure that you want to stop the experiment?")
            self.message_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            self.message_box.setDefaultButton(QMessageBox.No)
            reply = self.message_box.exec_()
            if reply == QMessageBox.Yes:
                self.stop_experiment()

    def start_experiment(self):
        # Change the button text
        self.start_stop_button.setText("Stop Experiment")

        # Display intital counter values
        self.elapsed_counter.display("00:00")  # Initial display
        minutes, seconds = divmod(self.usage_time_points[0], 60)
        self.action_counter.display(f"{minutes:02d}:{seconds:02d}")  # Initial display

        # Start the timers
        current_time = QTime.currentTime()
        time_until_next_second = 1000 - current_time.msec()    # Ensure that the counters are displayed exactly on every second-change
        #TODO: Depends on experiment type -> implement this
        QTimer.singleShot(time_until_next_second, self.synced_start)    # Start counters

        # Calculate the clock times
        self.calculate_clock_times(current_time)

    def stop_experiment(self):
        # If any, close the message box
        if self.message_box:
            self.message_box.close()
            self.message_box = None

        # Change the button text
        self.start_stop_button.setText("Start Experiment")

        # Stop the timers
        self.elapsed_counter.stop()
        self.action_counter.stop()

        # Display a message
        #? If wished, make the tables writeable now
        QMessageBox.information(self, "Experiment Stopped", "The experiment has been stopped. You can now export the data.")

    def synced_start(self):
        self.clock.restart()    # Sync the clock
        self.elapsed_counter.start()
        self.action_counter.start(self.usage_time_points)

def main():
    # Create the application
    app = QApplication(sys.argv)
    experiment_app = EasyLab()

    # Exit the application
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()