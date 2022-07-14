import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import flush_Annals_of_the_Association_of_American_Geographers
import flush_Geoforum
import flush_The_Professional_Geographer
import flush_Transaction_of_the_Institute_of_British_Geographers
import flush_The_Geographical_Journal

def flush(which, progress_bar):
    if which == 0:
        flush_Annals_of_the_Association_of_American_Geographers.flush(progress_bar)
    elif which == 1:
        flush_The_Professional_Geographer.flush(progress_bar)
    elif which == 2:
        flush_Geoforum.flush(progress_bar)
    elif which == 3:
        flush_Transaction_of_the_Institute_of_British_Geographers.flush(progress_bar)
    elif which == 4:
        flush_The_Geographical_Journal.flush(progress_bar)
    else:
        pass

if __name__ == "__main__":
    for i in range(5):
        flush(i)