
import timeit

# time calculation timer
def time_taken(outer_function):
    def inner():
        start = timeit.default_timer()
        outer_function()
        end = timeit.default_timer()
        print("Execution Time: ", (end-start))
    return inner    