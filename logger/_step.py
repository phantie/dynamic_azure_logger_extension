from typing import Self


class Step:
    def __init__(self):
        self.step_counter = 0

    def inc(self):
        self.step_counter += 1
    
    def peek(self) -> int:
        return self.step_counter

    def copy(self) -> Self:
        step = Step()
        step.step_counter = self.step_counter
        return step


