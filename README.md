A python code to debug [FRACTRAN](https://en.wikipedia.org/wiki/FRACTRAN) programs. Requires python 3.10 or higher.

usage:
```python
from fractran_debugger import *

multiplication_program = [(455, 33), (11, 13), (1, 11),
                          (3, 7), (11, 2), (1, 3)]
input = (2 ** 9) * (3 ** 11)
break_points = [lambda x: x % 5 == 0, Cursor(3, Timing.BEFORE)]

state = ProgramState(multiplication_program, input, break_points)
while not state.is_terminated:
    state.go_to_next_break_point()
    print(state)

print(state.current == 5 ** (9 * 11))
```