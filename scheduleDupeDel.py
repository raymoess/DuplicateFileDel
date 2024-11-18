import schedule
import time
from dupedelete import find_dupes, delete_dupes  # Import functions from duplicate_cleaner.py

#function that combines finding and deleting duplicates
def cleanup_dupes():
    directory = ""  #choose path to scan for dupe files
    log_file = "deletion_log.txt"  #log file where moved files will be written
    print(f"Starting duplicate file scan in: {directory}...")
    dupes = find_dupes(directory)
    delete_dupes(dupes, log_file)  #pass the log file to delete_duplicates

#change between the below lines of code to choose when you want the program to be scheduled to run
schedule.every(10).seconds.do(cleanup_dupes)
#schedule.every().sunday.at("07:00").do(cleanup_dupes)

while True:
    #run pending scheduled tasks
    schedule.run_pending()
    time.sleep(1)
