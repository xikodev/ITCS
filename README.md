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

The file [input.txt](lab01/input.txt) contains textual DFA definition.
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

Problem solution: [lab01.py](lab01/lab01.py)

---

## Lab 2

### Problem

In a programming language of your choice, implement a simulator of a Deterministic
Pushdown Automaton (DPDA).
The input to your program should be a textual definition of a DPDA, given in a format of your
choice (it could be similar to the DFA definition format above), along with an input string
which should be processed by the DPDA.
The simulator should output, for each input symbol, the correponding active state of the
DPDA. At the end, it should output whether the input string is accepted.

### Example Input

```
input.txt
```

The file [input.txt](lab02/input.txt) contains textual DPDA definition.
Example of a textual DPDA definition (the format can be different in your solution):

```
States: q0,q1,q2
Input symbols: a,b
Stack symbols: Z,A
Accepting states: q2
Initial state: q0
Initial stack symbol: Z
Input string: aabb
Transitions:
q0,a,Z->q0,AZ
q0,a,A->q0,AA
q0,b,A->q1,eps
q1,b,A->q1,eps
q1,eps,Z->q2,Z
```

### Example Output

The executable program should print the required result. An example of program output for the above input:

```
Input string: aabb
a -> q0
a -> q0
b -> q1
b -> q2
Accepted: yes
```

Problem solution: [lab02.py](lab02/lab02.py)
