from PyQt5.QtWidgets import QLCDNumber, QGraphicsOpacityEffect
from PyQt5.QtCore import QTimer, pyqtSignal, QPropertyAnimation


class ActionCounter(QLCDNumber):
    time_reached = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        # Initialize the counter and the timer
        self.times = list()
        self.current_time_index = 0
        self.remaining_time = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_counter)
        self.display("--:--")  # Initial display

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

        # Initialize the opacity effect and the animation
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setDuration(1000)  # 2 seconds
        self.animation.setStartValue(1)  # Fully opaque
        self.animation.setEndValue(0)  # Fully transparent
        self.animation.stateChanged.connect(self.animate)


    def start(self, times):
        self.times = times
        self.remaining_time = self.times[self.current_time_index]
        self.timer.start(1000)  # Update the counter every second

    def stop(self):
        self.timer.stop()
        self.current_time_index = 0
        self.remaining_time = 0
        self.display("--:--")

    def update_counter(self):
        self.remaining_time -= 1  # Decrement the remaining time
        if self.animation.state() != QPropertyAnimation.Running:
            self.display_time()

        # Check if the time has reached zero
        if self.remaining_time == 0:
            if self.animation.state() == QPropertyAnimation.Running:    # If another animation is already running, stop it
                self.animation.stop()
            self.animation.start()  # Start the animation
            self.time_reached.emit()  # Emit the time_reached signal #TODO: How fast can I connect it? Or better use other way?

            # Move to the next time, if there is one
            self.current_time_index += 1
            if self.current_time_index < len(self.times):
                self.remaining_time = self.times[self.current_time_index]
            else:
                self.stop()  # Stop the timer

    def display_time(self):
        minutes, seconds = divmod(self.remaining_time, 60)
        self.display(f"{minutes:02d}:{seconds:02d}")  # Update the display

    def animate(self, state):
        if state == QPropertyAnimation.Stopped:
            self.end_animation()
        elif state == QPropertyAnimation.Running:
            self.start_animation()

    def start_animation(self):
        self.display("00:00")
        self.setStyleSheet("""
            background-color: white;
            color: green;
            border: 1px solid green;
            border-radius: 10px;
        """)

    def end_animation(self):
        self.opacity_effect.setOpacity(1)
        self.display_time()
        self.setStyleSheet("""
            background-color: white;
            color: black;
            border: 1px solid black;
            border-radius: 10px;
        """)