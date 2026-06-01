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


def split_items(text):
    result = []
    for part in text.split(","):
        part = part.strip()
        if part:
            result.append(part)
    return result


def normalize_symbol(symbol):
    if symbol in ("eps", "epsilon", "Îµ", "ε"):
        return ""
    return symbol


def parse_dpda_from_file(filename):
    dpda = DPDA()

    with open(filename, "r", encoding="utf-8") as file:
        lines = [line.strip() for line in file if line.strip()]

    reading_transitions = False

    for line in lines:
        if line == "Transitions:":
            reading_transitions = True
            continue

        if not reading_transitions:
            if line.startswith("States:"):
                dpda.states = split_items(line[len("States:"):])
            elif line.startswith("Input symbols:"):
                dpda.input_symbols = split_items(line[len("Input symbols:"):])
            elif line.startswith("Stack symbols:"):
                dpda.stack_symbols = split_items(line[len("Stack symbols:"):])
            elif line.startswith("Accepting states:"):
                dpda.accepting_states = set(split_items(line[len("Accepting states:"):]))
            elif line.startswith("Initial state:"):
                dpda.initial_state = line[len("Initial state:"):].strip()
            elif line.startswith("Initial stack symbol:"):
                dpda.initial_stack_symbol = line[len("Initial stack symbol:"):].strip()
            elif line.startswith("Input string:"):
                text = line[len("Input string:"):].strip()
                if text == "":
                    dpda.input_string = []
                elif "," in text:
                    dpda.input_string = split_items(text)
                else:
                    dpda.input_string = list(text)
            continue

        left, right = line.split("->")
        left_parts = [part.strip() for part in left.split(",")]
        right_parts = [part.strip() for part in right.split(",")]

        state = left_parts[0]
        input_symbol = normalize_symbol(left_parts[1])
        stack_top = left_parts[2]
        next_state = right_parts[0]
        push_value = normalize_symbol(right_parts[1])

        dpda.transitions[(state, input_symbol, stack_top)] = (next_state, push_value)

    return dpda


def apply_transition(stack, push_value):
    if push_value == "":
        return

    for symbol in reversed(push_value):
        stack.append(symbol)


def run_epsilon_transitions(dpda, state, stack):
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


def simulate_dpda(dpda):
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
    return visited_states, state in dpda.accepting_states


def print_simulation(dpda, visited_states, accepted):
    if dpda.input_string:
        printable_input = "".join(dpda.input_string)
    else:
        printable_input = "eps"

    print("Input string: " + printable_input)

    if dpda.input_string:
        for symbol, state in zip(dpda.input_string, visited_states):
            print(f"{symbol} -> {state}")
    else:
        print("No input symbols were consumed.")

    if accepted:
        print("Accepted: yes")
    else:
        print("Accepted: no")


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
