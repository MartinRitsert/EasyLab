from PyQt5.QtWidgets import QLCDNumber, QGraphicsOpacityEffect
from PyQt5.QtCore import QTimer, pyqtSignal, QPropertyAnimation, QSequentialAnimationGroup


class ActionCounter(QLCDNumber):
    time_reached = pyqtSignal()
    style_changed = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        # Initialize the counter and the timer
        self.time_points = list()
        self.current_time_index = 0
        self.remaining_time = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_counter)
        self.display("--:--")  # Initial display

        # Create stylesheets
        self.default_style = ("""
            background-color: white;
            color: black;
            border: 1px solid black;
            border-radius: 10px;
        """)
        self.orange_style = ("""
            background-color: white;
            color: orange;
            border: 3px solid orange;
            border-radius: 10px;
        """)
        self.red_style = ("""
            background-color: white;
            color: red;
            border: 3px solid red;
            border-radius: 10px;
        """)
        self.green_style = ("""
            background-color: white;
            color: green;
            border: 3px solid green;
            border-radius: 10px;
        """)

        # Set initial display style
        self.setStyleSheet(self.default_style)
        self.setSegmentStyle(QLCDNumber.Flat)
        self.setDigitCount(5)  # Display format: mm:ss
        self.setFixedSize(300, 100)

        # Initialize the opacity effect and the animation
        self.animation_group = QSequentialAnimationGroup()
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.opacity_effect.setOpacity(1)
        self.setGraphicsEffect(self.opacity_effect)

        self.animation1 = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation1.setDuration(1000)
        self.animation1.setStartValue(1)  # Fully opaque
        self.animation1.setEndValue(1)  # Still fully opaque
        self.animation_group.addAnimation(self.animation1)

        self.animation2 = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation2.setDuration(200)
        self.animation2.setStartValue(1)  # Fully opaque
        self.animation2.setEndValue(0)  # Fully transparent
        self.animation_group.addAnimation(self.animation2)

        self.animation_group.stateChanged.connect(self.animate)


    def start(self, time_points):
        self.time_points = time_points
        self.remaining_time = self.time_points[0]
        self.timer.start(1000)  # Update the counter every second

        # Set color for new counter
        if self.remaining_time <= 10:
            self.setStyleSheet(self.red_style)
        elif self.remaining_time <= 30:
            self.setStyleSheet(self.orange_style)
        else:
            self.setStyleSheet(self.default_style)

    def stop(self):
        self.timer.stop()
        self.current_time_index = 0
        self.remaining_time = 0
        self.setStyleSheet(self.default_style)
        self.display("--:--")

    def update_counter(self):
        self.remaining_time -= 1  # Decrement the remaining time

        # Prevent displaying of time and changing color during animation
        if self.animation_group.state() != QPropertyAnimation.Running:
            self.display_time()

            # If required, change counter color
            if self.remaining_time <= 10:
                if self.styleSheet() != self.red_style:
                    self.setStyleSheet(self.red_style)
            elif self.remaining_time <= 30:
                if self.styleSheet() != self.orange_style:
                    self.setStyleSheet(self.orange_style)

        # Check if the time has reached zero
        if self.remaining_time == 0:
            if self.animation_group.state() == QPropertyAnimation.Running:    # If another animation is already running, stop it
                self.animation_group.stop()
            self.animation_group.start()  # Start the animation
            self.time_reached.emit()  # Emit the time_reached signal

            # Move to the next time, if there is one
            self.current_time_index += 1
            if self.current_time_index < len(self.time_points):
                # Need to calculate the difference between two time_points
                self.remaining_time = self.time_points[self.current_time_index] - self.time_points[self.current_time_index - 1]
            else:
                self.animation_group.stop()  # Stop the animation
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
        self.setStyleSheet(self.green_style)

    def end_animation(self):
        self.setStyleSheet(self.default_style)
        self.opacity_effect.setOpacity(1)
        self.display_time()

    def setStyleSheet(self, stylesheet):
        super().setStyleSheet(stylesheet)
        color = None
        if stylesheet == self.default_style:
            color = "black"
        elif stylesheet == self.orange_style:
            color = "orange"
        elif stylesheet == self.red_style:
            color = "red"
        elif stylesheet == self.green_style:
            color = "green"
        if color:
            self.style_changed.emit(color)