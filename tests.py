from storage import test as storage_test
from audio import test as audio_test

def run_all_tests():
    print("Running all unit tests...")
    storage_test()
    audio_test()
    print("All tests completed successfully!")