# storage.py
# Stores up to 20 most recent sensor readings

buffer_size = 20
storage_buffer = []

def save(sensor_value):
    """
    Save the most recent sensor value into a rolling buffer.
    """
    global storage_buffer
    storage_buffer.append(sensor_value)
    if len(storage_buffer) > buffer_size:
        storage_buffer.pop(0)  # drop oldest
    return storage_buffer

def get_latest():
    """Return the most recent sensor value (or None if not set)."""
    if not storage_buffer:
        return None
    return storage_buffer[-1]

def get_all():
    """Return all stored values (latest to oldest)."""
    return storage_buffer[::-1]

def clear():
    """Clear the storage buffer."""
    global storage_buffer
    storage_buffer = []
