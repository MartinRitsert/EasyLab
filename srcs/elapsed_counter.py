from PyQt5.QtWidgets import QLCDNumber
from PyQt5.QtCore import QTimer, pyqtSignal


class ElapsedCounter(QLCDNumber):
    time_reached = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        # Set the display style
        self.setStyleSheet("""
            background-color: white;
            color: black;
            border: 1px solid black;
            border-radius: 10px;
        """)
        self.setSegmentStyle(QLCDNumber.Flat)
        self.setDigitCount(5)  # Display format: mm:ss
        self.setFixedSize(300, 100)

        # Initialize the counter and the timer
        self.elapsed_time = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_counter)
        self.display("00:00")  # Initial display


    def start(self):
        self.timer.start(1000)  # Update the counter every second

    def stop(self):
        self.timer.stop()
        self.elapsed_time = 0

    def update_counter(self):
        self.elapsed_time += 1  # Increment the elapsed time
        self.display_time()

    def display_time(self):
        minutes, seconds = divmod(self.elapsed_time, 60)
        self.display(f"{minutes:02d}:{seconds:02d}")  # Update the display

        # Check if the limit has been reached
        if self.elapsed_time >= (60 * 60):  # 60 minutes * 60 seconds/minute
            self.stop()  # Stop the timer
            self.time_reached.emit()  # Emit the time_reached signal