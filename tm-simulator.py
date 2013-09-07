#!/usr/bin/env python

import sys
import argparse

from collections import namedtuple


class State(object):
    """
    A representation of a TM state
    """

    def __init__(self, state_id):
        self.state_id = state_id 
        self.reachable = False
        self.next_states = {}
        self.instructions = {}

    def __repr__(self):
        """Temp repr for debugging purposes"""
        # TODO: Clean up
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
        """Returns the tape's current symbol"""
        return self.tape[self.pointer]

    def replace(self, x):
        """Replaces the current tape symbol with x"""
        self.tape[self.pointer] = x

    def move(self, direction):
        """Moves along the tape left or right. 
        
        Grows a buffer on the left to reduce the number of list copies required

        Args:
            direction: direction of tape movement. 1 for right, -1 for left.
        """
        if self.pointer == self.left and direction == -1:
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
        """Grows the buffer on the left
        
        Buffer size increases by 2x

        Args:
            li: list that will be grown left

        Returns:
            List that has a grown left
        """
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
        """Loads a tape into the TM config

        Args:
            tape_str: string of a tape

        Raises:
            TMHalt: Current state does not have any transitions
        """
        self.tape = Tape(tape_str)
        self.cur_state = self.start_state

    def step(self):
        """Takes one step into the TM sim"""
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

    def run(self, verbose=False):
        """Runs until the TM halts

        Args:
            verbose: flag that indicates whether verbose print is turned on or off
        """
        # prints verbosely if flag is enabled
        if verbose:
            def verboseprint(*args):
                for arg in args:
                    print arg,
                print
        else:
            # Empty function
            verboseprint = lambda *a: None

        s = "{:10}: {}"
        step = 1
        print s.format("START", self.tape)
        try:
            while 1:
                self.step()
                verboseprint(s.format("STEP" + str(step), self.tape))
                step += 1
        except TMHalt:
            print s.format("STEP" + str(step), self.tape)


class AmbiguousStateError(Exception):
    pass


class InputError(Exception):
    pass


class TMHalt(Exception):
    pass


def parse_instructions(raw_instructions):
    """Parses a string of TM instructions and constructs the TM states

    Args:
        raw_instructions: string of TM instructions

    Returns:
        The starting state of the TM

    Raises:
        AmbiguousStateError: A state has two or more of the same tape symbol
            input
    """
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

    # first pass for constructing states
    state_table = {}
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
    # TODO: start state depends on user-input
    return state_table['1']


def get_tapes(raw_tapes):
    """Converts a string of many tapes into an array of tapes

    Args:
        raw_tapes: string of many tapes

    Returns:
        An array of tapes
    """
    return [x.strip() for x in raw_tapes.strip().split('\n')]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TM simulator")
    parser.add_argument("instructions", help="text file of TM instructions")
    parser.add_argument("test_cases", help="text file of test cases")
    parser.add_argument("-v", "--verbosity", action="store_true",
                        help="increase step verbosity")
    args = parser.parse_args()

    try:
        with open(args.instructions) as f:
            start_state = parse_instructions(f.read())
            tm = TMSimulator(start_state)

        with open(args.test_cases) as f:
            tapes = get_tapes(f.read())

        for t in tapes:
            tm.load_tape(t)
            tm.run(verbose=args.verbosity)
            print
    except (AmbiguousStateError, InputError) as e:
        print repr(e)
