import sys

from collections import namedtuple


class State(object):
    """
    A representation of a TM instruction
    """

    def __init__(self, state_id):
        """
        """
        self.state_id = state_id 
        self.reachable = False
        self.next_states = {}
        self.instructions = {}

    def __repr__(self):
        s = "State: " + self.state_id + "\n"
        s += "Instructions:\n"
        for i in self.instructions.items():
            s += "\t" + str(i) + "\n"
        return s


class Tape(object):
    """
    The TM tape
    """

    # TODO: interchangeable blanks from input
    _blanks = ['_', 'b']
    _blank = _blanks[0]

    def __init__(self, s):
        self.left_buf_size = 10
        self.tape = [None] * self.left_buf_size +  list(s)
        self.left = self.left_buf_size
        self.pointer = self.left

    def get_cur_symbol(self):
        return self.tape[self.pointer]

    def replace(self, x):
        self.tape[self.pointer] = x

    def move(self, direction):
        if self.pointer == self.left and direction == -1:
            print self.tape
            if self.pointer == 0:
                self.tape = self.__grow_left(self.tape)
                self.pointer = self.left
            self.pointer -= 1
            self.tape[self.pointer] = self._blank
            self.left -= 1
        elif self.pointer == len(self.tape) - 1 and direction == 1:
            self.pointer += 1
            self.tape.append(self._blank)
        else:
            self.pointer += direction

    def __grow_left(self, li):
        li = [None] * self.left_buf_size + li
        self.left_buf_size *= 2
        self.left = self.left_buf_size
        return li

    def __str__(self):
        # splice is so inefficient D:
        return ''.join(self.tape[self.left:])


class TMSimulator(object):
    """
    Simulates a TM
    """
    _left = 'l'
    _right = 'r'

    def __init__(self, start_state):
        self.start_state = start_state

    def load_tape(self, tape_str):
        self.tape = Tape(tape_str)
        self.cur_state = self.start_state

    def step(self):
        """
        Takes one step into the TM sim
        """
        tape_sym = self.tape.get_cur_symbol()
        instr = self.cur_state.instructions.get(tape_sym)
        if instr is not None:
            self.tape.replace(instr.write)

            if instr.direction.lower() == self._left:
                self.tape.move(-1)
            elif instr.direction.lower() == self._right:
                self.tape.move(1)
            else:
                raise InputError(instr.direction + " is not a valid direction")

            self.cur_state = self.cur_state.next_states[instr.next]
        else:
            raise TMHalt()

    def run(self):
        """
        Runs until the TM halts
        """
        try:
            while 1:
                self.step()
                print self.tape
        except TMHalt:
            print "TM halted"


class AmbiguousStateError(Exception):
    pass

class InputError(Exception):
    pass

class TMHalt(Exception):
    pass


def parse_instructions(raw_instructions):
    Instruction = namedtuple('Instruction', ['state', 
                                             'tape', 
                                             'write',
                                             'direction',
                                             'next'])
    # list of Instruction tuples
    instructions = []
    for x in raw_instructions.strip().split('\n'):
        i = x.strip().split(' ')
        instructions.append(Instruction(state = i[0],
                                        tape = i[1],
                                        write = i[2],
                                        direction = i[3],
                                        next = i[4]))
    state_table = {}

    # first pass for constructing states
    for i in instructions:
        if i.state not in state_table:
            state_table[i.state] = State(i.state)
        if i.next not in state_table:
            state_table[i.next] = State(i.next)

    # second pass for writing rules and linking states
    for i in instructions:
        state = state_table[i.state]
        if i.tape in state.instructions:
            raise AmbiguousStateError(
                "{} tape input already exists in {}".format(i.tape,
                                                            i.state))
        state.instructions[i.tape] = i
        next_state = state_table[i.next]
        next_state.reachable = True
        state.next_states[i.next] = next_state

    # default start state is 1
    return state_table['1']


def get_tapes(raw_tapes):
    return [x.strip() for x in raw_tapes.strip().split('\n')]


if __name__ == "__main__":
    # if len(sys.argv) != 3:
    #     sys.exit(2)

    try:
        with open(sys.argv[1]) as f:
            start_state = parse_instructions(f.read())
            tm = TMSimulator(start_state)

        with open(sys.argv[2]) as f:
            tapes = get_tapes(f.read())

        tm.load_tape(tapes[0])
        tm.run()
    except AmbiguousStateError as detail:
        print detail
    except InputError as detail:
        print detail
