import time

from pocketpose.utils.misc import all_exec_times, timed_exec


# Sample functions and class for testing
@timed_exec
def sample_function(duration):
    """Function that sleeps for 'duration' seconds."""
    time.sleep(duration)


class SampleClass:
    @timed_exec
    def sample_method(self, duration):
        """Method that sleeps for 'duration' seconds."""
        time.sleep(duration)


def test_timed_execution_function():
    sample_function(0.1)
    assert 0.09 < all_exec_times[f"{__name__}.sample_function"].last < 0.11
    assert len(all_exec_times[f"{__name__}.sample_function"].all) == 1


def test_timed_execution_method():
    sample_class = SampleClass()
    sample_class.sample_method(0.2)
    assert 0.19 < all_exec_times[f"{__name__}.sample_method"].last < 0.21
    assert len(all_exec_times[f"{__name__}.sample_method"].all) == 1


def test_execution_time_stats():
    # Call the function 4 more times to check average calculation
    for _ in range(4):
        sample_function(0.2)

    assert 0.19 < all_exec_times[f"{__name__}.sample_function"].last < 0.21
    assert len(all_exec_times[f"{__name__}.sample_function"].all) == 5  # 1 + 4

    actual_avg = (0.1 + 0.2 * 4) / 5  # 0.1 is the first call above
    avg = all_exec_times[f"{__name__}.sample_function"].avg
    assert actual_avg - 0.01 < avg < actual_avg + 0.01


def test_key_generation():
    assert f"{__name__}.sample_function" in all_exec_times
    assert f"{__name__}.sample_method" in all_exec_times, all_exec_times.keys()
