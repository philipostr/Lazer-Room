from lazer_sim import *

'''To run the line_profiler
Prerequisite: install it using "pip install line_profiler"
1. kernprof -l profile_lazer_sim.py
2. python3 -m line_profiler profile_lazer_sim.py.lprof
'''

'''To run the memory_profiler
Prerequisite: install it using "python setup.py install
1. python3 -m memory_profiler profile_lazer_sim.py
'''

def profile_run():
    for x in range(100):
        simulate(5, 5, (2,2), (1,1), 5, True)
        # simulate(5, 5, (2,2), (1,1), 5, False)


if __name__ == '__main__':
    profile_run()
