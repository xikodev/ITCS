# Introduction to Theoretical Computer Science

Faculty of Electrical Engineering and Computing

---

## Lab 1

### Problem

In a programming language of your choice, implement a DFA minimization algorithm
(described in e.g. Sect. 4.4.3 in [1]).
The input to your program should be a textual definition of a deterministic finite automaton
(DFA), given in a format of your choice. The output should be the minimized DFA in the
same format.

### Example Input

```
input.txt
```

The file input.txt contains textual DFA definition.
Example of a textual DFA definition (the format can be different in your solution):

```
States: p1,p2,p3,p4,p5,p6,p7
Symbols: c,d
Accepting states: p5,p6,p7
Initial state: p1
Transitions:
p1,c->p6
p1,d->p3
p2,c->p7
p2,d->p3
p3,c->p1
p3,d->p5
p4,c->p4
p4,d->p6
p5,c->p7
p5,d->p3
p6,c->p4
p6,d->p1
p7,c->p4
p7,d->p2
```

### Example Output

The executable program should print the required result. An example of program output for the above input:

```
States: {p1,p2},{p3},{p4},{p5},{p6,p7}
Symbols: c,d
Accepting states: {p5},{p6,p7}
Initial state: {p1,p2}
Transitions:
{p1,p2},c->{p6,p7}
{p1,p2},d->{p3}
{p3},c->{p1,p2}
{p3},d->{p5}
{p4},c->{p4}
{p4},d->{p6,p7}
{p5},c->{p6,p7}
{p5},d->{p3}
{p6,p7},c->{p4}
{p6,p7},d->{p1,p2}
```

Problem solution: [lab01.py](lab01.py)
