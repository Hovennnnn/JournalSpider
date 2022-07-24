from flush import flush_Annals_of_the_Association_of_American_Geographers
from flush import flush_Geoforum
from flush import flush_The_Professional_Geographer
from flush import flush_Transaction_of_the_Institute_of_British_Geographers
from flush import flush_The_Geographical_Journal

def Flushing(which, progress_bar):
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
        raise

if __name__ == "__main__":
    for i in range(5):
        Flushing(i, lambda num, text: print(f'{num}%', text))