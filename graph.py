import json
from graphviz import Digraph

def graph_turing_machine(description):
    states = description["states"]
    input_alphabet = description["inputAlphabet"]
    tape_alphabet = description["tapeAlphabet"]
    initial_state = description["initialState"]
    acceptance = description["acceptance"]
    blank = description["blank"]
    transitions = description["transitions"]
    
    dot = Digraph(comment='Turing Machine')
    dot.attr(rankdir='LR')
    
    for state in states:
        if state in acceptance:
            dot.node(state, shape='doublecircle', color="#4FAA69")
        else:
            dot.node(state, color="#BF6969")
    
    grouped_transitions = {}
    for transition in transitions:
        from_state = transition["currentState"]
        to_state = transition["nextState"]
        tape_input = transition["tapeInput"]
        write_tape = transition["writeTape"]
        direction = transition["direction"]
        
        label = f"{tape_input}→{write_tape},{direction}"
        
        if (from_state, to_state) not in grouped_transitions:
            grouped_transitions[(from_state, to_state)] = [label]
        else:
            grouped_transitions[(from_state, to_state)].append(label)
    
    for (from_state, to_state), labels in grouped_transitions.items():
        label = "\n".join(labels)
        dot.edge(from_state, to_state, label=label, color="#BF6969")
    
    return dot

if __name__ == "__main__":
    with open('fibonacci.json') as json_file:
        data = json.load(json_file)

    dot = graph_turing_machine(data)
    dot.render('turing_machine', format='pdf', cleanup=True, view=True)
