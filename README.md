Turing Machine Simulator
========================

What and why?
-------------

A small program for simulating a turing machine. 

I've always wanted to develop this when I was a TA for intro to CS given how
annoying it was to grade the turing machine problems. So what better time to
automate the process than when I'm no longer a intro to CS TA?

Usage
-----

### Input

The turing machine instructions should be in a newline-delimited text file with
the following format:

    {state} {tape-sym} {write-sym} {direction} {next-state}

Direction is either 'l' for left or 'r' for right. Blank symbol is '\_'. Other
elements can be any arbitrary string.

### Test cases

Put your test cases in another text file, newline delimited.

### Sample Run

    python tm-simulator.py {instructions} {test-cases}

See test\_instructions.txt and test\_tapes.txt for sample input.

For more options, run

    python tm-simulator.py -h

### Output

Final output TBD

Todo
----

1. Make TMSimulator.run return a sane output rather than just printing
2. Separate classes into separate files for organization
3. Let user set max step # to avoid infinite loop
4. Gui for visualizing states and transitions
5. Commenting for input files

