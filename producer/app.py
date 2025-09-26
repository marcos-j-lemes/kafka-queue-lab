import time
import random
import os
import fcntl

# Config
db_dir = '/app/data'
db_file = os.path.join(db_dir, 'queue.txt')

# Ensure directory exists
os.makedirs(db_dir, exist_ok=True)

# Touch file if not exists
if not os.path.exists(db_file):
    open(db_file, 'w').close()

def send_message(value):
    """Append message to the file with locking."""
    try:
        with open(db_file, 'a') as f:
            fcntl.flock(f, fcntl.LOCK_EX)  # Exclusive lock
            f.write(f"{value}\n")
            fcntl.flock(f, fcntl.LOCK_UN)  # Unlock
        print(f"Produced message: {value}")
    except Exception as e:
        print(f"Error producing: {e}")

if __name__ == "__main__":
    print("Producer starting...")
    while True:  # Infinite loop for demo
        for _ in range(10):  # Send 10 messages
            value = random.randint(1, 100)
            send_message(value)
            time.sleep(0.5)  # Throttle
        print("Batch sent, waiting 5s...")
        time.sleep(5)