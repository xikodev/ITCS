import sys


class DPDA:
    def __init__(self):
        self.states = []
        self.input_symbols = []
        self.stack_symbols = []
        self.accepting_states = set()
        self.initial_state = None
        self.initial_stack_symbol = None
        self.input_string = []
        self.transitions = {}


def parse_csv(text: str):
    items = []

    for part in text.split(","):
        cleaned = part.strip()
        if cleaned:
            items.append(cleaned)

    return items


def parse_input_string(text: str):
    cleaned = text.strip()

    if not cleaned:
        return []

    if "," in cleaned:
        return parse_csv(cleaned)

    return list(cleaned)


def parse_transition(line: str):
    left, right = line.split("->")
    source_parts = [part.strip() for part in left.split(",")]
    target_parts = [part.strip() for part in right.split(",")]

    if len(source_parts) != 3:
        raise ValueError(f"Invalid transition source: {line}")
    if len(target_parts) != 2:
        raise ValueError(f"Invalid transition target: {line}")

    state, input_symbol, stack_top = source_parts
    next_state, push_value = target_parts
    return state, input_symbol, stack_top, next_state, push_value


def normalize_symbol(symbol: str):
    if symbol in {"eps", "epsilon", "ε"}:
        return ""
    return symbol


def validate_dpda(dpda: DPDA):
    if not dpda.states:
        raise ValueError("Missing states.")
    if not dpda.stack_symbols:
        raise ValueError("Missing stack symbols.")
    if dpda.initial_state is None:
        raise ValueError("Missing initial state.")
    if dpda.initial_stack_symbol is None:
        raise ValueError("Missing initial stack symbol.")

    state_set = set(dpda.states)
    input_symbol_set = set(dpda.input_symbols)
    stack_symbol_set = set(dpda.stack_symbols)

    if dpda.initial_state not in state_set:
        raise ValueError("Initial state is not listed in states.")
    if dpda.initial_stack_symbol not in stack_symbol_set:
        raise ValueError("Initial stack symbol is not listed in stack symbols.")
    if not dpda.accepting_states.issubset(state_set):
        raise ValueError("Accepting states must be listed in states.")

    for symbol in dpda.input_string:
        if symbol not in input_symbol_set:
            raise ValueError(f"Input symbol '{symbol}' is not listed in input symbols.")

    for (state, input_symbol, stack_top), (next_state, push_value) in dpda.transitions.items():
        if state not in state_set:
            raise ValueError(f"Unknown source state '{state}'.")
        if next_state not in state_set:
            raise ValueError(f"Unknown target state '{next_state}'.")
        if input_symbol and input_symbol not in input_symbol_set:
            raise ValueError(f"Unknown input symbol '{input_symbol}' in transitions.")
        if stack_top not in stack_symbol_set:
            raise ValueError(f"Unknown stack symbol '{stack_top}' in transitions.")

        for symbol in push_value:
            if symbol not in stack_symbol_set:
                raise ValueError(f"Unknown stack symbol '{symbol}' in push value.")


def parse_dpda_from_file(filename: str):
    dpda = DPDA()

    with open(filename, "r", encoding="utf-8") as file:
        lines = []

        for line in file:
            cleaned = line.strip()
            if cleaned:
                lines.append(cleaned)

    reading_transitions = False

    for line in lines:
        if reading_transitions:
            state, input_symbol, stack_top, next_state, push_value = parse_transition(line)
            key = (state, normalize_symbol(input_symbol), stack_top)

            if key in dpda.transitions:
                raise ValueError(f"Non-deterministic transition duplicated for {key}.")

            dpda.transitions[key] = (next_state, normalize_symbol(push_value))
            continue

        if line.startswith("States:"):
            dpda.states = parse_csv(line[len("States:"):])
        elif line.startswith("Input symbols:"):
            dpda.input_symbols = parse_csv(line[len("Input symbols:"):])
        elif line.startswith("Stack symbols:"):
            dpda.stack_symbols = parse_csv(line[len("Stack symbols:"):])
        elif line.startswith("Accepting states:"):
            dpda.accepting_states = set(parse_csv(line[len("Accepting states:"):]))
        elif line.startswith("Initial state:"):
            dpda.initial_state = line[len("Initial state:"):].strip()
        elif line.startswith("Initial stack symbol:"):
            dpda.initial_stack_symbol = line[len("Initial stack symbol:"):].strip()
        elif line.startswith("Input string:"):
            dpda.input_string = parse_input_string(line[len("Input string:"):])
        elif line == "Transitions:":
            reading_transitions = True

    validate_dpda(dpda)
    return dpda


def apply_transition(stack, push_value: str):
    if push_value == "":
        return

    for symbol in reversed(push_value):
        stack.append(symbol)


def run_epsilon_transitions(dpda: DPDA, state: str, stack):
    visited = set()

    while True:
        stack_top = stack[-1] if stack else ""
        key = (state, "", stack_top)

        if key in visited:
            raise ValueError("Detected an epsilon-transition loop.")

        transition = dpda.transitions.get(key)
        if transition is None:
            return state

        visited.add(key)
        next_state, push_value = transition
        stack.pop()
        apply_transition(stack, push_value)
        state = next_state


def simulate_dpda(dpda: DPDA):
    stack = [dpda.initial_stack_symbol]
    state = dpda.initial_state
    visited_states = []

    state = run_epsilon_transitions(dpda, state, stack)

    for symbol in dpda.input_string:
        if not stack:
            raise ValueError("The stack became empty before processing finished.")

        stack_top = stack[-1]
        transition = dpda.transitions.get((state, symbol, stack_top))

        if transition is None:
            visited_states.append("REJECT")
            return visited_states, False

        next_state, push_value = transition
        stack.pop()
        apply_transition(stack, push_value)
        state = next_state
        state = run_epsilon_transitions(dpda, state, stack)
        visited_states.append(state)

    state = run_epsilon_transitions(dpda, state, stack)
    accepted = state in dpda.accepting_states
    return visited_states, accepted


def print_simulation(dpda: DPDA, visited_states, accepted: bool):
    printable_input = "".join(dpda.input_string) if dpda.input_string else "eps"

    print("Input string: " + printable_input)

    if dpda.input_string:
        for symbol, state in zip(dpda.input_string, visited_states):
            print(f"{symbol} -> {state}")
    else:
        print("No input symbols were consumed.")

    print("Accepted: " + ("yes" if accepted else "no"))


def main():
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = input("Enter DPDA input file name: ")

    filename = filename.replace("\ufeff", "").strip()
    dpda = parse_dpda_from_file(filename)
    visited_states, accepted = simulate_dpda(dpda)
    print_simulation(dpda, visited_states, accepted)


if __name__ == "__main__":
    main()


# Expected input format:
# States: q0,q1,q2
# Input symbols: a,b
# Stack symbols: Z,A
# Accepting states: q2
# Initial state: q0
# Initial stack symbol: Z
# Input string: aabb
# Transitions:
# q0,a,Z->q0,AZ
# q0,a,A->q0,AA
# q0,b,A->q1,eps
# q1,b,A->q1,eps
# q1,eps,Z->q2,Z
