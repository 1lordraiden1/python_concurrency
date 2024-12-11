import json
import concurrent.futures
import queue
import threading

# JSON file name
JSON_FILE = 'users.json'

# Lock for thread-safe access to the JSON file
lock = threading.Lock()

# Load data from the JSON file
def load_data():
    with open(JSON_FILE, 'r') as file:
        return json.load(file)

# Save data to the JSON file
def save_data(data):
    with open(JSON_FILE, 'w') as file:
        json.dump(data, file, indent=4)

# Create operation
def create_user(user_data):
    with lock:
        data = load_data()
        user_data['id'] = len(data['users']) + 1
        data['users'].append(user_data)
        save_data(data)

# Read operation
def get_users():
    with lock:
        data = load_data()
        return data['users']

# Update operation
def update_user(user_id, updated_data):
    with lock:
        data = load_data()
        for user in data['users']:
            if user['id'] == user_id:
                user['name'] = updated_data['name']
                user['email'] = updated_data['email']
                break
        save_data(data)

# Delete operation
def delete_user(user_id):
    with lock:
        data = load_data()
        data['users'] = [user for user in data['users'] if user['id'] != user_id]
        save_data(data)

# Multi-threading implementation
def execute_crud_operation(operation, *args):
    if operation == 'create':
        create_user(*args)
    elif operation == 'read':
        return get_users()
    elif operation == 'update':
        update_user(*args)
    elif operation == 'delete':
        delete_user(*args)

def main():
    # Create some sample data
    user_data_list = [
        {'name': 'John Doe', 'email': 'john@example.com'},
        {'name': 'Jane Doe', 'email': 'jane@example.com'},
        {'name': 'Bob Smith', 'email': 'bob@example.com'}
    ]

    # Create users concurrently

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = []
        for user_data in user_data_list:
            futures.append(executor.submit(execute_crud_operation, 'create', user_data))

        # Get the executor's threads
        executor_threads = executor._threads
        print(f"Executor threads: {len(executor_threads)}")

        # Print the thread names
        for thread in executor_threads:
            print(f"Thread: {thread.name}")

    # Read users concurrently
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = []
        for _ in range(5):
            futures.append(executor.submit(execute_crud_operation, 'read'))
        for future in futures:
            users = future.result()
            print(users)

    # Update users concurrently
    user_id = 1
    updated_data = {'name': 'John Doe Updated', 'email': 'john.updated@example.com'}
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = []
        for _ in range(5):
            futures.append(executor.submit(execute_crud_operation, 'update', user_id, updated_data))
        for future in futures:
            future.result()

    # Delete users concurrently
    user_id = 1
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = []
        for _ in range(5):
            futures.append(executor.submit(execute_crud_operation, 'delete', user_id))
        for future in futures:
            future.result()

if __name__ == '__main__':
    main()