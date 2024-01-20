from typing import TypeAlias, Optional, Callable
from enum import Enum

Denominator: TypeAlias = int
Numerator: TypeAlias = int
Fraction: TypeAlias = tuple[Numerator, Denominator]
Index: TypeAlias = int
Value: TypeAlias = int


class Timing(Enum):
    BEFORE = 1
    AFTER = 2


class Cursor:
    index: Index
    timing: Timing

    def __init__(self, _index: Index, _timing: Timing) -> None:
        self.index = _index
        self.timing = _timing

    def __repr__(self):
        return f'Cursor({self.index}, {self.timing})'

    def __eq__(self, other):
        if isinstance(other, Cursor):
            return self.index == other.index and self.timing == other.timing
        return False


BreakPoint: TypeAlias = Callable[[Value], bool] | Optional[Cursor]


class ProgramState:
    program: list[Fraction]
    input: Value
    current: Value
    cursor: Optional[Cursor] = None
    is_terminated: bool = False
    break_points: list[BreakPoint]

    def __init__(self, _program: list[Fraction], _input: Value, _break_points: list[BreakPoint] = []) -> None:
        self.program = _program
        self.input = _input
        self.current = _input
        self.break_points = _break_points

    def step_forward(self) -> None:
        if self.is_terminated:
            return
        if len(self.program) == 0:
            self.is_terminated = True
            return
        if self.cursor is None:
            result = self.__find_next_fraction()
            if result is None:
                self.is_terminated = True
                return
            self.cursor = Cursor(result[0], Timing.BEFORE)
            return
        if self.cursor.timing == Timing.BEFORE:
            fraction = self.program[self.cursor.index]
            self.current = fraction[0] * self.current // fraction[1]
            self.cursor.timing = Timing.AFTER
            return
        if self.cursor.timing == Timing.AFTER:
            self.cursor = None
            return

    def go_to_next_break_point(self) -> None:
        if self.is_terminated:
            return

        self.step_forward()

        while (not self.is_terminated) and (not self.__is_break_point()):
            self.step_forward()
        return

    def __is_break_point(self) -> bool:
        for break_point in self.break_points:
            if callable(break_point):
                if self.cursor is None:
                    return False
                if self.cursor.timing == Timing.BEFORE:
                    return False
                if break_point(self.current):
                    return True
            else:
                if break_point == self.cursor:
                    return True

    def __find_next_fraction(self) -> Optional[tuple[Index, Fraction]]:
        for index, f in enumerate(self.program):
            if self.current % f[1] == 0:
                return index, f
        return None

    def __repr__(self):
        return f'ProgramState({self.program}, {self.input}, {self.current}, {self.cursor}, {self.is_terminated})'


if __name__ == '__main__':
    PRIMEGAME: list[Fraction] = [(17, 91), (78, 85), (19, 51), (23, 38), (29, 33), (77, 29), (95, 23), (77, 19),
                                 (1, 17), (11, 13), (13, 11), (15, 2), (1, 7), (55, 1)]
    is_power_of_2: BreakPoint = lambda x: x > 0 and x & (x - 1) == 0
    log_two: Callable[[int], int] = lambda x: x.bit_length() - 1
    state: ProgramState = ProgramState(PRIMEGAME, 2, [is_power_of_2])
    while not state.is_terminated:
        state.go_to_next_break_point()
        print(log_two(state.current))  # n th prime

