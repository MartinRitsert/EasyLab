import sys
import os
import random
import string

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QLineEdit, QGridLayout, \
    QSizePolicy, QComboBox, QMessageBox, QFrame
from PyQt5.QtCore import Qt, QTimer, QTime, pyqtSignal
from PyQt5.QtGui import QGuiApplication, QFont
from PyQt5.QtMultimedia import QSound

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
        self.experiment_dropdown_index = 0

        # Initialize inhaler type label and dropdown
        self.inhaler_label = QLabel("Inhaler Type:")
        self.inhaler_dropdown = QComboBox()
        self.inhaler_dropdown.addItem("pMDI")
        self.inhaler_dropdown.addItem("Turbohaler")
        self.inhaler_dropdown.addItem("Diskus")

        # Initialize clock
        self.clock = DigitalClock()

        # Initialize time counters and upcoming action label
        self.action_label = QLabel("Next Action:")
        self.upcoming_action_label = QLabel("")
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

        # Initialize dict that contains schedule of experiment
        self.schedule = dict()  # Example: (150: ("Hold", 25))
        
        # Initialize the key and value pair in the schedule
        self.next_action_time_point = None
        self.next_action = ""
        self.next_action_duration = None

        # Initialize a QTimer used for countdown inside upcoming_action_label
        self.action_timer = QTimer(self)
        self.action_timer_remaining = None
        self.action_timer.timeout.connect(self.update_upcoming_action_label)

        # Initialize a SingleShot Timer used for showing the the next action inside upcoming_action_label
        self.action_singleshot_timer = QTimer(self)
        self.action_singleshot_timer.setSingleShot(True)
        self.action_singleshot_timer.timeout.connect(self.stop_action)

        # Keep track of message boxes
        self.message_box = None

        # Load standard stylesheet
        current_file_path = os.path.abspath(__file__)
        current_directory = os.path.dirname(current_file_path)
        with open(os.path.join(current_directory, "style.qss"), "r") as file:
            self.stylesheet = file.read()

        # Load sound files
        current_file_path = os.path.abspath(__file__)
        current_directory = os.path.dirname(current_file_path)
        self.silence_sound = os.path.join(current_directory, "../assets/sounds/silence.wav")
        self.cheering_sound = os.path.join(current_directory, "../assets/sounds/cheering.wav")  

        # Setup the UI
        self.setup_ui()


    def setup_ui(self):
        #* Setup the window
        # Get screen resolution
        screen = QGuiApplication.primaryScreen().geometry()
        screenWidth = screen.width()
        screenHeight = screen.height()

        # Window size
        winWidth = int(screenWidth // 2.23)
        winHeight = int(screenHeight // 1.45)

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
        hash_layout.setSpacing(7)  # Set the spacing between the widgets
        self.hash_label.setFixedWidth(130)    # Set the width for all labels to align them
        self.hash_line_edit.setMaxLength(10)    # Set the maximum number of characters
        metrics = self.hash_line_edit.fontMetrics()    # Get the font metrics
        width = metrics.boundingRect("Z" * 13).width()    # Calculate the width of 10 characters
        self.hash_line_edit.setFixedWidth(width)    # Set the width of the line edit
        self.hash_line_edit.setStyleSheet(self.stylesheet)
        metrics = self.hash_edit_button.fontMetrics()    # Get the font metrics
        width = metrics.boundingRect("Confirm Hash").width()    # Calculate the width of the button
        width += 40    # Add some extra width
        self.hash_edit_button.setFixedWidth(width)    # Set the width of the button
        self.hash_edit_button.setStyleSheet(self.stylesheet)
        self.hash_gen_button.setFixedWidth(width)    # Set the width of the button
        self.hash_gen_button.setStyleSheet(self.stylesheet)

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
        self.experiment_dropdown.setStyleSheet(self.stylesheet)
        experiment_layout.addWidget(self.experiment_dropdown)
        experiment_layout.addStretch()
        top_layout.addLayout(experiment_layout, 1, 0)

        # Setup inhaler type label and dropdown
        inhaler_layout = QHBoxLayout()
        self.inhaler_label.setFixedWidth(130)    # Set the width for all labels to align them
        inhaler_layout.addWidget(self.inhaler_label)
        self.inhaler_dropdown.setStyleSheet(self.stylesheet)
        inhaler_layout.addWidget(self.inhaler_dropdown)
        inhaler_layout.addStretch()
        top_layout.addLayout(inhaler_layout, 2, 0)

        # Setup the clock
        top_layout.addWidget(self.clock, 0, 2, 3, 1)

        # Add the top layout to the main layout
        layout.addLayout(top_layout)

        # Add space between the labels and the counters
        layout.addStretch()

        # Setup counter labels
        counter_labels_layout = QHBoxLayout()
        self.action_label.setAlignment(Qt.AlignCenter)
        self.action_label.setFixedSize(710, 30)
        self.action_label.setStyleSheet("""
            background-color: white;
            font: bold 14pt;
            color: black;
            border: 1px solid black;
            border-radius: 10px;
        """)
        counter_labels_layout.addWidget(self.action_label)
        # counter_labels_layout.setAlignment(self.action_label, Qt.AlignCenter)
        counter_labels_layout.addStretch()
        self.elapsed_label.setAlignment(Qt.AlignCenter)
        self.elapsed_label.setFixedSize(300, 30)
        self.elapsed_label.setStyleSheet("""
            background-color: white;
            font: bold 14pt;
            color: black;
            border: 1px solid black;
            border-radius: 10px;
        """)
        counter_labels_layout.addWidget(self.elapsed_label)
        # counter_labels_layout.setAlignment(self.elapsed_label, Qt.AlignRight)
        layout.addLayout(counter_labels_layout)

        # Setup counters and upcoming action label
        counter_layout = QHBoxLayout()
        counter_layout.setSpacing(10)
        self.upcoming_action_label.setAlignment(Qt.AlignCenter)
        self.upcoming_action_label.setFixedSize(400, 100)
        self.upcoming_action_label.setStyleSheet("""
            background-color: white;
            font: bold 42pt;
            color: lightgray;
            border: 1px solid black;
            border-radius: 10px;
        """)
        counter_layout.addWidget(self.upcoming_action_label)
        counter_layout.addWidget(self.action_counter)
        # counter_layout.setAlignment(self.action_counter, Qt.AlignRight)
        counter_layout.addStretch()
        counter_layout.addWidget(self.elapsed_counter)
        # counter_layout.setAlignment(self.elapsed_counter, Qt.AlignRight)
        layout.addLayout(counter_layout)
        layout.addStretch()

        # Setup table1 labels and line edits
        t1_frame = QFrame()     # Create a frame for table1
        t1_frame.setStyleSheet("""
            border: 1px solid black;
            border-radius: 10px;
        """)

        t1_frame_layout = QVBoxLayout(t1_frame)
        self.table1_label.setStyleSheet("""
            font: bold 16pt;
            border: none;
        """)
        t1_frame_layout.addWidget(self.table1_label)

        t1_layout = QGridLayout()
        for label in [self.t1_col1_label, self.t1_col2_label]:
            label.setStyleSheet("""
                font: bold 14pt;
                border: none;
            """)
        t1_layout.addWidget(self.t1_col1_label, 0, 0)
        t1_layout.addWidget(self.t1_col2_label, 0, 1)

        t_stylesheet = ("""
            border: 1px solid gray;
            border-radius: 6px;
            padding-left: 2px;
        """)
        for col1_line_edit, col2_line_edit in zip(self.t1_col1_line_edits, self.t1_col2_line_edits):
            col1_line_edit.setStyleSheet(t_stylesheet)
            col2_line_edit.setStyleSheet(t_stylesheet)
            t1_layout.addWidget(col1_line_edit)
            t1_layout.addWidget(col2_line_edit)
        t1_frame_layout.addLayout(t1_layout)
        layout.addWidget(t1_frame)
        layout.addStretch()

        # Setup table2 labels and line edits
        t2_frame = QFrame()     # Create a frame for table2
        t2_frame.setStyleSheet("""
            border: 1px solid black;
            border-radius: 10px;
        """)

        t2_frame_layout = QVBoxLayout(t2_frame)
        self.table2_label.setStyleSheet("""
            font: bold 16pt;
            border: none;
        """)
        t2_frame_layout.addWidget(self.table2_label)

        t2_layout = QGridLayout()
        for label in [self.t2_col1_label, self.t2_col2_label]:
            label.setStyleSheet("""
                font: bold 14pt;
                border: none;
            """)
        t2_layout.addWidget(self.t2_col1_label, 0, 0)
        t2_layout.addWidget(self.t2_col2_label, 0, 1)

        for col1_line_edit, col2_line_edit in zip(self.t2_col1_line_edits, self.t2_col2_line_edits):
            col1_line_edit.setStyleSheet(t_stylesheet)
            col2_line_edit.setStyleSheet(t_stylesheet)
            t2_layout.addWidget(col1_line_edit)
            t2_layout.addWidget(col2_line_edit)
        t2_frame_layout.addLayout(t2_layout)
        layout.addWidget(t2_frame)
        layout.addStretch()

        # Setup randomization and export buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        self.rand_button.setFixedHeight(30)
        self.rand_button.setStyleSheet(self.stylesheet)
        self.rand_button.setFont(QFont("Arial", 14))
        self.export_button.setFixedHeight(30)
        self.export_button.setStyleSheet(self.stylesheet)
        self.export_button.setFont(QFont("Arial", 14))
        button_layout.addWidget(self.rand_button)
        button_layout.addWidget(self.export_button)
        layout.addLayout(button_layout)

        # Setup start_stop button
        self.start_stop_button.setFixedHeight(30)
        self.start_stop_button.setStyleSheet(self.stylesheet)
        self.start_stop_button.setFont(QFont("Arial", 14))
        layout.addWidget(self.start_stop_button)

        # Set the layout for the window
        self.setLayout(layout)

        # Connect signals and slots
        self.hash_edit_button.clicked.connect(self.edit_hash)
        self.hash_gen_button.clicked.connect(self.generate_hash)
        self.experiment_dropdown.currentIndexChanged.connect(self.on_experiment_changed)
        self.action_counter.time_reached.connect(self.start_action)
        self.action_counter.style_changed.connect(self.change_action_style)
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
        # Prevent changing experiment type during an active experiment
        if self.start_stop_button.text() == "Stop Experiment":
            QMessageBox.warning(self, "Experiment Running", "Cannot change the experiment type during an active experiment. \
                                Please stop the experiment before changing the experiment type.")
            # Manually set the dropdown back to the previous index
            self.experiment_dropdown.blockSignals(True)
            self.experiment_dropdown.setCurrentIndex(self.experiment_dropdown_index)
            self.experiment_dropdown.blockSignals(False)
            return

        # Ask for confirmation of deleting current times
        if self.t1_col1_line_edits[0].text():
            reply = QMessageBox.warning(self, "Delete Data", 'This will delete all "time points and clock times" data. Are you sure that you want to continue?', \
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.No:
                # Manually set the dropdown back to the previous index
                self.experiment_dropdown.blockSignals(True)
                self.experiment_dropdown.setCurrentIndex(self.experiment_dropdown_index)
                self.experiment_dropdown.blockSignals(False)
                return
        
        # Save the current index
        self.experiment_dropdown_index = index

        # Delete current times, clock times before changing the experiment type
        self.delete_time_points()
        self.delete_clock_times()
        self.delete_schedule()

        # Reset elapsed counter
        self.elapsed_counter.reset()

        # Change table1 label
        if index == 0:
            self.table1_label.setText("Table 1 - Inhaler Usage Times")
        elif index == 1:
            self.table1_label.setText("Table 1 - Inhaler Dumping Times")

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

    def generate_times_e1(self):
        # Note: all times in seconds
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
        self.delete_schedule()

        # Reset elapsed counter
        self.elapsed_counter.reset()

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
        # Note: all times in seconds
        #! Assumption 1: The times must be so that they begin and end inside the same 10 minute intervall
            #! Assumption 1.1: Between end of dumping and end of current intervall, there must be at least 1 second 
            #! Assumption 1.2: Between end of holding and end of current intervall, there must be at least 1 second
        #! Assumption 2: The times must be so that actions do not overlap
            #! Assumption 2.1: Between end of dumping and start of next action, there must be at least 1 second
            #! Assumption 2.2: Between end of holding and start of next action, there must be at least 1 second
        #! Assumption 3: The holding duration must be at least 30 seconds
        #? Question1: Are the assumptions okay?
        #? Question2: Holding duration [30, 70] okay?
        #? Question3: Dumping duration [60, 119] okay?

        # Ask for confirmation of deleting current times
        if self.t1_col1_line_edits[0].text():
            reply = QMessageBox.warning(self, "Delete Data", 'This will delete all "time points and clock times" data. Are you sure that you want to continue?', \
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.No:
                return
        
        # Delete current times before generating new times
        self.delete_time_points()
        self.delete_clock_times()
        self.delete_schedule()

        # Reset elapsed counter
        self.elapsed_counter.reset()

        # Iterate over all six 10-minute intervals
        for i in range(0, 60*60, 10*60):

            # Start randomizing usage time point, hold time point and hold duration
            dump_time_point = i + random.randint(0, (10*60)-61)    # Assumption 1.1
            dump_duration = random.randint(60, 119)
            hold_time_point = i + random.randint(0, (10*60)-2)  # Assumption 1.2 && Assumption 3
            hold_duration = random.randint(30, 70)

            # Initialize approved to false
            approved = False

            # Recalculate times until they are approved
            while not approved:
                # Assumption 1.1
                if (dump_time_point + dump_duration) >= (i + (10*60)):
                    dump_time_point = i + random.randint(0, (10*60)-61)
                    dump_duration = random.randint(60, 119)
                    hold_time_point = i + random.randint(0, (10*60)-2)
                    hold_duration = random.randint(30, 70)
                    continue
                # Assumption 1.2
                if (hold_time_point + hold_duration) >= (i + (10*60)):
                    dump_time_point = i + random.randint(0, (10*60)-61)
                    dump_duration = random.randint(60, 119)
                    hold_time_point = i + random.randint(0, (10*60)-2)
                    hold_duration = random.randint(30, 70)
                    continue
                # Assumption 2
                elif dump_time_point == hold_time_point or dump_time_point == (hold_time_point + hold_duration) \
                    or (dump_time_point + dump_duration) == hold_time_point or (dump_time_point + dump_duration) == (hold_time_point + hold_duration):
                    dump_time_point = i + random.randint(0, (10*60)-61)
                    dump_duration = random.randint(60, 119)
                    hold_time_point = i + random.randint(0, (10*60)-2)
                    hold_duration = random.randint(30, 70)
                    continue
                # Assumption 2.1
                elif dump_time_point < hold_time_point and (dump_time_point + dump_duration + 1) > hold_time_point:
                    dump_time_point = i + random.randint(0, (10*60)-61)
                    dump_duration = random.randint(60, 119)
                    hold_time_point = i + random.randint(0, (10*60)-2)
                    hold_duration = random.randint(30, 70)
                    continue
                # Assumption 2.2 && Assumption 3
                elif hold_time_point < dump_time_point and (hold_time_point + hold_duration + 1) > dump_time_point:
                    dump_time_point = i + random.randint(0, (10*60)-61)
                    dump_duration = random.randint(60, 119)
                    hold_time_point = i + random.randint(0, (10*60)-2)
                    hold_duration = random.randint(30, 70)
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

    def delete_schedule(self):
        # Clear schedule dict and corresponding variables
        self.schedule.clear()
        self.next_action_time_point = None
        self.next_action = ""
        self.next_action_duration = None

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
            self.delete_schedule() # Delete current schedule
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
        # Check experiment type and setup schedule dict:
        if self.experiment_dropdown.currentText() == "Experiment 1: Inhaler Usage":
            # 1. Add entries from usage_time_points
            for time_point in self.usage_time_points:
                self.schedule[time_point] = ("Inhale", 10)
            # 2. Add entries from hold_time_points
            for i, time_point in enumerate(self.hold_time_points):
                self.schedule[time_point] = ("Hold", self.hold_durations[i])
        elif self.experiment_dropdown.currentText() == "Experiment 2: Inhaler Dumping":
            # 1. Add entries from dump_time_points
            for i, time_point in enumerate(self.dump_time_points):
                self.schedule[time_point] = ("Dump", self.dump_durations[i])
            # 2. Add entries from hold_time_points
            for i, time_point in enumerate(self.hold_time_points):
                self.schedule[time_point] = ("Hold", self.hold_durations[i])
        else:
            print("Error: Unknown experiment type")
            return
        self.schedule = dict(sorted(self.schedule.items()))    # 3. Sort the schedule dict

        # Extract time_points before poping values from schedule
        time_points = list(self.schedule.keys())

        # Display the first action
        self.display_upcoming_action()

        # Change the button text
        self.start_stop_button.setText("Stop Experiment")

        # Display intital counter values
        self.elapsed_counter.display("00:00")  # Initial display
        minutes, seconds = divmod(self.next_action_time_point, 60)
        self.action_counter.display(f"{minutes:02d}:{seconds:02d}")  # Initial display

        # Start the timers
        current_time = QTime.currentTime()
        time_until_next_second = 1000 - current_time.msec()    # Ensure that the counters are displayed exactly on every second-change
        QTimer.singleShot(time_until_next_second, lambda: self.synced_start(time_points))    # Start counters

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
        self.action_timer.stop()
        self.action_singleshot_timer.stop()

        # Clear the upcoming action label
        self.upcoming_action_label.setText("")

        # Reset styles
        self.upcoming_action_label.setStyleSheet("""
            background-color: white;
            font: bold 42pt;
            color: lightgray;
            border: 1px solid black;
            border-radius: 10px;
        """)

        # Play cheering sound
        if not self.schedule:
            QSound.play(self.cheering_sound)

        # Display a message
        #? If wished, make the tables writeable now
        QMessageBox.information(self, "Experiment Stopped", "The experiment has been stopped. Don't forget to export the data if you haven't already done so.")

    def synced_start(self, time_points):
        self.clock.restart()    # Sync the clock
        self.elapsed_counter.start()
        self.action_counter.start(time_points)

    def display_upcoming_action(self):
        # When schedule is empty (all actions are done), clear the upcoming action label
        if not self.schedule:
            self.upcoming_action_label.setText("All done!")
            return

        # Pop first action from schedule
        time_point = next(iter(self.schedule))
        (action, duration) = self.schedule.pop(time_point)
        self.next_action_time_point = time_point
        self.next_action = action
        self.next_action_duration = duration

        # Case 1: Next action = Inhale
        if action == "Inhale":
            self.upcoming_action_label.setText("Inhale")
        # Case 2: Next action = Hold
        elif action == "Hold":
            self.upcoming_action_label.setText(f"Hold ({duration} s)")
        # Case 3: Next action = Dump
        elif action == "Dump":
            self.upcoming_action_label.setText(f"Dump ({duration} s)")
   
    def start_action(self):
        # Apply the new style
        self.upcoming_action_label.setStyleSheet("""
            background-color: white;
            font: bold 42pt;
            color: green;
            border: 3px solid green;
            border-radius: 10px;
        """)

        # Start timer until end of action
        if self.next_action in ["Hold", "Dump"]:
            self.action_timer.start(1000)
            self.action_timer_remaining = self.next_action_duration

        # Start timer until end of action (+1 s to be not abrupt and not interfere with action_counter)
        self.action_singleshot_timer.start((self.next_action_duration + 1) * 1000)

    def stop_action(self):
        # Apply the default style
        self.upcoming_action_label.setStyleSheet("""
            background-color: white;
            font: bold 42pt;
            color: lightgray;
            border: 1px solid black;
            border-radius: 10px;
        """)

        # Display the next action
        self.display_upcoming_action()

        #TODO:(Gray out lines in table1 and table2)

    def update_upcoming_action_label(self):
        self.action_timer_remaining -= 1
        if self.next_action == "Hold":
            self.upcoming_action_label.setText(f"Hold ({self.action_timer_remaining} s)")
        elif self.next_action == "Dump":
            self.upcoming_action_label.setText(f"Dump ({self.action_timer_remaining} s)")

        # Stop the timer when it reaches 0
        if self.action_timer_remaining == 0:
            self.action_timer.stop()

    def change_action_style(self, color):
        if color == "black":
            pass
        elif color == "orange":
            pass
        elif color == "red":
            pass
        elif color == "green":
            pass
        else:
            pass
    
    def closeEvent(self, event):
        reply = QMessageBox.question(self, "Exit", "Exiting the application will stop active experiments and will delete all 'time points and clock times' data. Are you sure you want to exit the application?", \
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

def main():
    # Create the application
    app = QApplication(sys.argv)

    # Create the main window
    experiment_app = EasyLab()

    # Define what happens when app is exiting
    app.aboutToQuit.connect(experiment_app.closeEvent)

    # Exit the application
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()