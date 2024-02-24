import time
from threading import Thread
import sys
from predict_new_doc import cluster_new_doc
from scrape_reddit import main

# Define the function to be periodically called
def periodic_function(interval, num_scrape):
    while True:
        # Perform periodic tasks here
        print(f"Will scrape {num_scrape} posts.")
        main(num_scrape)
        time.sleep(interval * 60)  # Wait for the specified interval

if len(sys.argv) != 2:
    raise Exception('Usage: python3 test_automation.py <interval>')
# Start the periodic function in a separate thread
interval = sys.argv[1]  # Set the interval (in seconds)
try:
    num_scrape = int(input('How many posts?'))
except:
    print('please enter an integer')
thread = Thread(target=periodic_function, args=(int(interval), int(num_scrape),))
thread.daemon = True  # Daemonize the thread to allow main program to exit
thread.start()

# Interact with the user in the main thread
while True:
    user_input = input("Enter 'quit' to exit, or enter a message to be clustered: ")
    if user_input.strip().lower() == 'quit':
        break
    elif not user_input:
        continue
    else:
        cluster_new_doc(user_input)

print("Exiting program.")

