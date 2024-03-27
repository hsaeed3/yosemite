import concurrent.futures
from functools import wraps

class Lightspeed:
    """
    A class that provides a method for executing callables in parallel.

    Methods:
        __init__(max_workers): Initializes the Lightspeed object with the maximum number of worker threads.
        run(callable, *args, **kwargs): Executes the given callable in parallel.
    """

    def __init__(self, max_workers=None):
        """
        Initializes the Lightspeed object.

        Parameters:
            max_workers: The maximum number of worker threads to be used (default: None).
        """
        self.max_workers = max_workers

    def run(self, callable, *args, **kwargs):
        """
        Executes the given callable in parallel.

        Parameters:
            callable: The callable object to be executed.
            *args: Variable-length arguments to be passed to the callable.
            **kwargs: Keyword arguments to be passed to the callable.

        Returns:
            The result of the parallel execution.
        """
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future = executor.submit(callable, *args, **kwargs)
            result = future.result()
        return result
    
    def multiplier(self, callable, count, *args, **kwargs):
        """
        Executes the given callable multiple times in parallel.

        Parameters:
            callable: The callable object to be executed.
            count: The number of times to execute the callable.
            *args: Variable-length arguments to be passed to the callable.
            **kwargs: Keyword arguments to be passed to the callable.

        Returns:
            A list of results from the parallel executions.
        """
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = [executor.submit(callable, *args, **kwargs) for _ in range(count)]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
        return results
    
def main():
    accelerator = Lightspeed(max_workers=5)

    # Run a simple print statement in parallel
    accelerator.run(print, "Hello, World!")
    accelerator.multiplier(print, 5, "Hello, World!")

    # Run a lambda function in parallel
    result = accelerator.run(lambda x, y: x + y, 10, 20)
    print("Result:", result)

if __name__ == "__main__":
    main()