Turing Machine Simulator
========================

What and why?
-------------

A small program for simulating a turing machine, mostly because I've been
wanting to write one for a while now.

Usage
-----

### Input

The turing machine instructions should be in a newline-delimited text file with
the following format:

    {state} {tape-sym} {write-sym} {direction} {next-state}

Direction is either 'l' for left or 'r' for right. 

Blank symbol is '\_'. 

Other elements can be any arbitrary string.

The default start state is state 1.

### Test cases

Put your test cases in another text file, newline delimited.

### Sample Run

    python tm_simulator.py {instructions} {test-cases}

See the tests/ folder for sample inputs

For more options, run

    python tm_simulator.py -h

### Output

Final output TBD

Todo
----

1. Make TMSimulator.run return a sane output rather than just printing
2. Separate classes into separate files for organization
3. Let user set max step # to avoid infinite loop
4. Gui for visualizing states and transitions
5. Commenting for input files
6. Reachable exception
7. Visualize where the tape pointer is

