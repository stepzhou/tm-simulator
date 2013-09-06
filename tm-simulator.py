import sys

from collections import namedtuple

class Instruction(object):
    """
    A representation of a TM instruction
    """

    def __init__(self, state):
        self.state = state 
        self.reachable = False
        self.next_states = {}
        self.rules = {}


class TMSimulator(object):
    """
    Simulates a TM
    """

    _blank = '_'
    
    def __init__(self, start_state):
        self.start_state = start_state
        self.index = 0

    def run(self, tape):
        raise NotImplementedError


class AmbiguousInstructionError(Exception):
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
    itable = {}

    # first pass for constructing instructions
    for i in instructions:
        if i.state not in itable:
            itable[i.state] = Instruction(i.state)

    # second pass for writing rules and connecting instructions
    for i in instructions:
        instr = itable[i.state]
        if i.tape in instr.rules:
            raise AmbiguousInstructionError(
                "{} tape input already exists in {}".format(i.tape,
                                                            i.state)
        # TODO: consider making a namedtuple. or is that overkill?
        instr.rules[i.tape] = (i.write, i.direction, i.next)
        instr.next_states[i.next] = itable[i.next]


def get_tapes(raw_tapes):
    raise NotImplementedError


if __name__ == "__main__":
    # if len(sys.argv) != 3:
    #     sys.exit(2)

    with open(sys.argv[1]) as f:
        start_state = parse_instructions(f.read())

    # with open(sys.argv[2]) as f:
    #     tapes = get_tapes(f.read())
