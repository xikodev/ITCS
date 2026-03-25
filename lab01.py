from collections import deque


class DFA:
    def __init__(self):
        self.states = []
        self.symbols = []
        self.accepting = set()
        self.initial_state = None
        self.transitions = {}


def parse_csv(text: str):
    items = []

    for part in text.split(","):
        cleaned = part.strip()
        if cleaned:
            items.append(cleaned)

    return items


def parse_transition(line: str):
    left, target = line.split("->")
    parts = left.split(",")
    state = parts[0].strip()
    symbol = parts[1].strip()
    return state, symbol, target.strip()


def validate_dfa(dfa: DFA):
    if not dfa.states:
        raise ValueError("Missing  states.")
    if not dfa.symbols:
        raise ValueError("Missing symbols.")
    if dfa.initial_state is None:
        raise ValueError("Mising initial state.")
    if dfa.initial_state not in dfa.states:
        raise ValueError("Initial state is not listed in states.")

    unknown_accepting = dfa.accepting - set(dfa.states)
    if unknown_accepting:
        raise ValueError("Accepting states must  be listed in states.")

    for state in dfa.states:
        for symbol in dfa.symbols:
            if (state, symbol) not in dfa.transitions:
                raise ValueError(f"Missing transition for ({state}, {symbol}).")


def parse_dfa_from_file(filename: str):
    dfa = DFA()

    with open(filename, "r") as file:
        lines = []

        for line in file:
            cleaned = line.strip()
            if cleaned:
                lines.append(cleaned)

    reading_transitions = False

    for line in lines:
        if reading_transitions:
            state, symbol, target = parse_transition(line)
            dfa.transitions[(state, symbol)] = target
            continue

        if line.startswith("States:"):
            dfa.states = parse_csv(line[len("States:"):])
        elif line.startswith("Symbols:"):
            dfa.symbols = parse_csv(line[len("Symbols:"):])
        elif line.startswith("Accepting states:"):
            dfa.accepting = set(parse_csv(line[len("Accepting states:"):]))
        elif line.startswith("Initial state:"):
            dfa.initial_state = line[len("Initial state:"):].strip()
        elif line == "Transitions:":
            reading_transitions = True

    validate_dfa(dfa)
    return dfa


def reachable_states(dfa: DFA):
    visited = {dfa.initial_state}
    queue = deque([dfa.initial_state])

    while queue:
        state = queue.popleft()
        for symbol in dfa.symbols:
            next_state = dfa.transitions[(state, symbol)]
            if next_state not in visited:
                visited.add(next_state)
                queue.append(next_state)

    return visited


def minimize_dfa(dfa: DFA):
    reachable = reachable_states(dfa)
    states = []
    for state in dfa.states:
        if state in reachable:
            states.append(state)

    state_count = len(states)

    state_index = {}
    for index, state in enumerate(states):
        state_index[state] = index

    distinguishable = []
    for _ in range(state_count):
        row = []
        for _ in range(state_count):
            row.append(False)
        distinguishable.append(row)

    for i in range(state_count):
        for j in range(i):
            if (states[i] in dfa.accepting) != (states[j] in dfa.accepting):
                distinguishable[i][j] = True

    changed = True
    while changed:
        changed = False

        for i in range(state_count):
            for j in range(i):
                if distinguishable[i][j]:
                    continue

                for symbol in dfa.symbols:
                    target_a = dfa.transitions[(states[i], symbol)]
                    target_b = dfa.transitions[(states[j], symbol)]

                    if target_a == target_b:
                        continue

                    first = state_index[target_a]
                    second = state_index[target_b]
                    row = max(first, second)
                    column = min(first, second)

                    if distinguishable[row][column]:
                        distinguishable[i][j] = True
                        changed = True
                        break

    parent = list(range(state_count))

    def find(node: int):
        if parent[node] != node:
            parent[node] = find(parent[node])
        return parent[node]

    def union(left: int, right: int):
        parent[find(right)] = find(left)

    for i in range(state_count):
        for j in range(i):
            if not distinguishable[i][j]:
                union(i, j)

    groups = {}
    for index, state in enumerate(states):
        root = find(index)
        groups.setdefault(root, []).append(state)

    equivalence_classes = list(groups.values())
    state_to_class = {}
    class_names = []

    for group in equivalence_classes:
        class_name = "{" + ",".join(group) + "}"
        class_names.append(class_name)
        for state in group:
            state_to_class[state] = class_name

    minimized = DFA()
    minimized.states = class_names
    minimized.symbols = dfa.symbols[:]
    minimized.initial_state = state_to_class[dfa.initial_state]
    minimized.accepting = {
        state_to_class[state] for state in states if state in dfa.accepting
    }

    for group in equivalence_classes:
        representative = group[0]
        source_name = state_to_class[representative]
        for symbol in dfa.symbols:
            target = dfa.transitions[(representative, symbol)]
            minimized.transitions[(source_name, symbol)] = state_to_class[target]

    return minimized


def print_dfa(dfa: DFA):
    accepting_states = []
    for state in dfa.states:
        if state in dfa.accepting:
            accepting_states.append(state)

    print("States: " + ",".join(dfa.states))
    print("Symbols : " + ",".join(dfa.symbols))
    print("Accepting states:" + ", ".join(accepting_states))
    print("Initial state: " + dfa.initial_state)
    print("Transitions:  ")

    for state in dfa.states:
        for symbol in dfa.symbols:
            print(f"{state},{symbol}->{dfa.transitions[(state, symbol)]}")


def main():
    filename = input("Enter DFA  input file nane:").strip()
    dfa = parse_dfa_from_file(filename)
    print_dfa(minimize_dfa(dfa))


if __name__ == "__main__":
    main()


# Borna Krpan
# JMBAG: 0036569999
