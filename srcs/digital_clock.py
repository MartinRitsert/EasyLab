from PyQt5.QtWidgets import QLCDNumber
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt, QTimer, QTime


class DigitalClock(QLCDNumber):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Set the display style
        
        self.showTime()
        self.timer = QTimer(self)
        time_until_next_second = 1000 - QTime.currentTime().msec()
        QTimer.singleShot(time_until_next_second, self.showTime)    # Ensure that the time is displayed exactly on every second-change
        self.timer.start(1000)  # Update the time every second
        self.timer.timeout.connect(self.showTime)
        
        # Set the display style
        self.setStyleSheet("""
            background-color: white;
            color: black;
            border: 1px solid black;
            border-radius: 10px;
            """)
        self.setSegmentStyle(QLCDNumber.Flat)
        self.setDigitCount(8)
        self.setFixedSize(300, 100)


    def showTime(self):
        time = QTime.currentTime()
        text = time.toString('hh:mm:ss')
        self.display(text)
