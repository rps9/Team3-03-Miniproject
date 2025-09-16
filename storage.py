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

# ------------------ Unit Tests ------------------
if __name__ == "__main__":
    print("Running storage.py unit tests...")

    clear()
    assert get_latest() is None, "Buffer should be empty at start"

    # Save a few values
    save(10)
    save(20)
    save(30)

    assert get_latest() == 30, "Latest should be most recent value"
    assert get_all() == [30, 20, 10], "get_all should return reversed order"

    # Test buffer overflow
    clear()
    for i in range(25):  # exceed buffer size
        save(i)
    all_vals = get_all()
    assert len(all_vals) == buffer_size, "Buffer should not exceed buffer_size"
    assert all_vals[0] == 24 and all_vals[-1] == 5, "Oldest values should drop"

    print("All storage.py tests passed ✅")
    print("Final buffer contents:", get_all())
