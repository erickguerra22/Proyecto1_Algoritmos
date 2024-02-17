import json

class TuringMachine:
    def __init__(self, states, input_alphabet, tape_alphabet, initial_state, acceptance, transitions, tape):
        self.states = states
        self.input_alphabet = input_alphabet
        self.tape_alphabet = tape_alphabet
        self.state = initial_state
        self.acceptance = acceptance
        self.transitions = transitions
        self.position = 0
        self.tape = tape

    def run(self):
        print(self.state)
        print(self.tape[self.position])
        transition = [t for t in transitions if t['currentState'] == self.state and t['tapeInput'] == self.tape[self.position]]
        if len(transition)>0:
            transition = transition[0]
            self.tape[self.position] = transition['writeTape'][-1]
            if '_' not in self.tape[0]:
                self.tape.insert(0,'_')
            elif self.tape[len(self.tape)-2] != '_':
                self.tape.insert(len(self.tape)-2,'_')
            derivation = ''
            for index, element in enumerate(self.tape):
                if index == self.position:
                    derivation += '\033[94m' + element + '\033[0m'
                else:
                    derivation += element
            #derivation = derivation.replace('_','')
            print(derivation)
            self.state = transition['nextState']
            if transition['direction'] == 'R': self.position += 1
            else: self.position -= 1
            if self.run():
                return True
        if self.state in self.acceptance:
            return True
        return False

if __name__ == "__main__":
    
    # Obtener componentes para la máquina
    
    with open('fibonacci.json') as json_file:
        data = json.load(json_file)
        states = data["states"]
        input_alphabet = data["inputAlphabet"]
        tape_alphabet = data["tapeAlphabet"]
        initial_state = data["initialState"]
        acceptance = data["acceptance"]
        transitions = data["transitions"]

    # Obtener input
    
    w = data["init_tape"]
    turing_machine = TuringMachine(states, input_alphabet, tape_alphabet, initial_state, acceptance, transitions, [*w, 'B'])
    
    # Verificar cadena

    print('\nDerivación:\n')
    result = turing_machine.run()
    print(f'\nEstado final: {turing_machine.state}')
    print(f'Cadena en la cinta: {turing_machine.tape}')
    if result:
        print(f'\nÚltimo número de la serie Fibonacci calculado: {"".join("".join(turing_machine.tape).split("B")[1]).replace("_","")}\n')
