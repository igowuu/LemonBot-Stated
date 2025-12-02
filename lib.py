from typing import Callable, List, Optional
class State:
  #will be called to determine if the state should be executed, any number of arguments can be passed in
  conditional: Callable[..., bool]
  #lambda function that will be called when the state is executed, any number of arguments can be passed in
  runner: Callable[..., None]
  #should have identical functionality as above, just in simulation/testing
  test_runner: Callable[..., None]
  #should be generated behind the scenes when constructed in state machine, should not be altered
  _id: int 
  #human readable name for debugging purposes, FSM does not care what this is
  name: str

class FinieStateMachine:
  #list of all states the machine can be in, may not be altered once execute is called
  states: List[State]
  #current state of the machine, robot will crash if it is None
  current_state: Optional[State]
  #duh
  isInTest: bool
  #private variable used to count id's for state generation
  _counter: int
  #used to prevent states from being added after the machine has been executed
  _state_creation_lock: bool
  #inilizes the machine, states are created with construct_state after
  def __init__(self, isInTest: bool):
   self.isInTest = isInTest
   self.states = []
   self.current_state = None
   self._counter = 0
   self._state_creation_lock = False
  #creates a new state and adds it to the FSM's options, cannot be called after execute is called
  def construct_state(self, name: str, conditional: Callable[..., bool], runner: Callable[..., None], test_runner: Callable[..., None]):
    if not self._state_creation_lock:
      state = State()
      state.runner = runner
      state.test_runner = test_runner
      state.name = name
      state.conditional = conditional
      state._id = self._counter
      self._counter += 1
      self.states.append(state)
    else:
      raise Exception("[ERROR] Cannot add states after the FSM has been executed")
  #executes the FSM, will run one execution loop, substates can be execcuted by the lambda functions
  def execute(self):
    for state in self.states:
      if state.conditional():
        self.current_state = state
        if self.isInTest:
          state.test_runner()
        else:
          state.runner()
