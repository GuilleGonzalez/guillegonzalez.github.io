# This file is just a class needed for the following. 
# 1. Run "kjv.py" & "esv.py". 
# 2. Run "sections_and_html.py" with "VERSION" set to "KJV" & "ESV" one time each respectively.
class BibleStats(): 
    include_metrics = True
    include_reading_times = True

    reading_speeds = range(150, 251, 50) # Start WPM, End WPM+1, Increment
    def wpm(word_count: int, speed):
        time = word_count / speed
        hrs, mins, secs = int(time // 60), int(time % 60), int(float(time * 60) % 60)
        return f'{hrs}hr {mins}m' if hrs > 0 else f'{mins}m {secs}s'
    