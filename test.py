import threading
import time
import random
import matplotlib.pyplot as plt

# Shared data structure to log thread activity
log = []

# Function executed by threads
def worker(thread_id):
    start_time = time.time()
    duration = random.uniform(1, 3)  # Random duration for each thread
    log.append((thread_id, 'start', start_time))
    time.sleep(duration)  # Simulate work
    end_time = time.time()
    log.append((thread_id, 'end', end_time))

# Create and start threads
threads = []
for i in range(5):  # 5 threads
    t = threading.Thread(target=worker, args=(i,))
    threads.append(t)
    t.start()

# Wait for all threads to complete
for t in threads:
    t.join()

# Prepare data for plotting
thread_ids = []
start_times = []
end_times = []

for thread_id, event, timestamp in log:
    if event == 'start':
        thread_ids.append(thread_id)
        start_times.append(timestamp)
    elif event == 'end':
        end_times.append(timestamp)

# Plot the threading timeline
plt.figure(figsize=(10, 6))
for i, thread_id in enumerate(thread_ids):
    plt.plot([start_times[i], end_times[i]], [thread_id, thread_id], marker='o', label=f"Thread {thread_id}")

plt.xlabel("Time (s)")
plt.ylabel("Thread ID")
plt.title("Thread Execution Timeline")
plt.legend()
plt.grid()
plt.show()
