import time
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

def process_message(value):
    """Execute function on data."""
    result = value ** 2
    print(f"Consumed {value} -> Processed: {result}")
    return result

if __name__ == "__main__":
    print("Consumer starting...")
    while True:
        try:
            if os.path.exists(db_file):
                with open(db_file, 'r+') as f:  # Open for read and write
                    fcntl.flock(f, fcntl.LOCK_EX)  # Exclusive lock
                    lines = f.readlines()
                    if lines:
                        value = int(lines[0].strip())
                        process_message(value)
                        # Rewrite the remaining lines
                        f.seek(0)
                        f.write(''.join(lines[1:]))
                        f.truncate()
                    fcntl.flock(f, fcntl.LOCK_UN)  # Unlock
        except Exception as e:
            print(f"Error consuming: {e}")
        time.sleep(1)  # Poll every second to avoid busy loop

        