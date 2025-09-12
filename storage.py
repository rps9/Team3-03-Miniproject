# storage.py
# Stores the most recent sensor reading (only one sensor now)

latest_value = None

def save(sensor_value):
    """
    Save the most recent sensor value.
    """
    global latest_value
    latest_value = sensor_value
    return latest_value

def get_latest():
    """Return the most recent sensor value (or None if not set)."""
    return latest_value

def clear():
    """Clear stored value."""
    global latest_value
    latest_value = None
