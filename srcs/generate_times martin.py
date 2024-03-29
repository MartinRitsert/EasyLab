import random

#TODO Improvements
# Open the file after generation
# Add a well noticeable sound and voice command 30s before the next action is due

# Create a PyQt program for this! It should be able to:
# - Export table automatically at start? Or ask if it should be exported? Or at the end?
# - Export the table to a Word-File (that is exactly the page contained in the study protocol)


usage_time_points = list()
hold_time_points = list()
hold_durations = list()

for i in range(0, 60, 10):

    usage_time_point = i + random.randint(0, 10)
    while(usage_time_point >= i + 10):
        usage_time_point = i + random.randint(0, 10)

    hold_time_point = usage_time_point
    hold_duration = random.randint(0, 60)
    while hold_time_point == usage_time_point or hold_time_point + (hold_duration / 60) >= i + 10:
        hold_time_point = i + random.randint(0, 10)
        hold_duration = random.randint(0, 60)
    
    
    usage_time_points.append(usage_time_point)
    hold_time_points.append(hold_time_point)
    hold_durations.append(hold_duration)
  

for usage_time_point in usage_time_points:
    print(usage_time_point)

for hold_time_point, hold_duration in zip(hold_time_points, hold_durations):
    print(hold_time_point, "(", hold_duration, "seconds )")