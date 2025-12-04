from typing import Callable, List, Optional
from dataclasses import dataclass

@dataclass
class State:
    """
    Represents one FSM state.

    Attributes:
        conditional: Returns True when this state should activate.
        runner: Executed when active in normal mode.
        test_runner: Executed when active in test mode.
        _id: Unique state identifier.
        name: Human-readable state name.
    """
    conditional: Callable[[], bool]
    runner: Callable[[], None]
    test_runner: Callable[[], None]
    _id: int
    name: str

class FiniteStateMachine:
    """
    FSM that activates the first state whose conditional returns True.
    Uses `runner` in normal mode and `test_runner` in test mode.
    """

    states: List[State]
    current_state: Optional[State]
    isInTest: bool
    _counter: int
    _state_creation_lock: bool

    def __init__(self, isInTest: bool) -> None:
        """
        Initialize the FSM.

        :param isInTest: If True, executes test_runner instead of runner.
        """
        self.isInTest = isInTest
        self.states = []
        self.current_state = None
        self._counter = 0
        self._state_creation_lock = False

    def construct_state(
            self,
            name: str,
            conditional: Callable[[], bool],
            runner: Callable[[], None],
            test_runner: Callable[[], None]
        ) -> None:
        """
        Add a state to the FSM. Must be done before the first execute() call.

        :param name: State name.
        :param conditional: Determines if the state should activate.
        :param runner: Executes when active (normal mode).
        :param test_runner: Executes when active (test mode), good for debugging.
        """
        if not self._state_creation_lock:
            state = State(conditional, runner, test_runner, self._counter, name)
            self._counter += 1
            self.states.append(state)
        else:
            raise Exception("[ERROR] Cannot add states after execution begins.")

    
    def execute(self) -> None:
        """
        Evaluate all states and run every state whose condition is True.
        Updates current_state to the last one executed.
        """
        self._state_creation_lock = True
        any_active = False

        for state in self.states:
            if state.conditional():
                self.current_state = state
                any_active = True
                (state.test_runner if self.isInTest else state.runner)()

        if not any_active:
            raise Exception("[ERROR] No state was activated")
