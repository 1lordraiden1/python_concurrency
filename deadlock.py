import threading
import time

# Shared resources
lock1 = threading.Lock()
lock2 = threading.Lock()

def thread1():
    print("Thread 1: Acquiring Lock 1")
    lock1.acquire()
    time.sleep(1)  # Simulate some work
    print("Thread 1: Acquiring Lock 2")
    lock2.acquire()
    
    print("Thread 1: Working with Lock 1 and Lock 2")
    lock2.release()
    lock1.release()

def thread2():
    print("Thread 2: Acquiring Lock 2")
    lock2.acquire()
    time.sleep(1)  # Simulate some work
    print("Thread 2: Acquiring Lock 1")
    lock1.acquire()
    
    print("Thread 2: Working with Lock 2 and Lock 1")
    lock1.release()
    lock2.release()

# Create threads
t1 = threading.Thread(target=thread1)
t2 = threading.Thread(target=thread2)

# Start threads
t1.start()
t2.start()

# Wait for threads to finish
t1.join()
t2.join()
