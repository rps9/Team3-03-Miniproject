# storage.py
# Stores sensor activation history

# Simple in-memory storage (circular buffer style)
buffer_size = 20   # keep last 20 activation events
storage_buffer = []

def save(activated_sensors):
    """
    Save a new sensor activation event.
    activated_sensors: list of indices (e.g., [0, 2])
    """
    global storage_buffer
    if activated_sensors:   # only store if something was activated
        storage_buffer.append(activated_sensors)
        if len(storage_buffer) > buffer_size:
            storage_buffer.pop(0)  # drop oldest
    return storage_buffer

def get_all():
    """Return all stored activation events."""
    return storage_buffer

def clear():
    """Clear the storage buffer."""
    global storage_buffer
    storage_buffer = []
