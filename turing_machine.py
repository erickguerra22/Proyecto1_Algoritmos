import json
import sys


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
        transition = [t for t in transitions if t['currentState'] == self.state and t['tapeInput'] == self.tape[self.position]]
        if len(transition)>0:
            transition = transition[0]
            self.tape[self.position] = transition['writeTape'][-1]
            derivation = ''
            for index, element in enumerate(self.tape):
                if index == self.position:
                    derivation += '\033[94m' + element + '\033[0m'
                else:
                    derivation += element
            print(derivation)
            print(self.state)
            self.state = transition['nextState']
            if transition['direction'] == 'R': self.position += 1
            elif transition['direction'] == 'L': self.position -= 1
            if self.run():
                return True
        if self.state in self.acceptance:
            return True
        return False

if __name__ == "__main__":
    
    # Definir límite de recursión
    sys.setrecursionlimit(1000000000)
    
    # Obtener componentes para la máquina
    with open('fibonacci.json') as json_file:
        data = json.load(json_file)
        states = data["states"]
        input_alphabet = data["inputAlphabet"]
        tape_alphabet = data["tapeAlphabet"]
        initial_state = data["initialState"]
        acceptance = data["acceptance"]
        transitions = data["transitions"]
        blank = data["blank"]

    # Obtener input
    
    w = input('Ingrese la cadena inicial: ')
    if blank:
        w = blank * len(w)*10 + w + blank * len(w)*10
    turing_machine = TuringMachine(states, input_alphabet, tape_alphabet, initial_state, acceptance, transitions, [*w, 'B'])
    
    # Verificar cadena

    print('\nDerivación:\n')
    result = turing_machine.run()
    print(f'\nEstado final: {turing_machine.state}')
    print(f'Cadena en la cinta: {turing_machine.tape}')
    #print(f'Cadena en la cinta: {turing_machine.tape}')
    if result:
        unaryNum = "".join(turing_machine.tape).replace("_","").replace("B","")
        print('\nCadena aceptada')
        print(f'Número resultante:\nUnario:{unaryNum}\nDecimal:{len(unaryNum)}')
    else:
        print('\nCadena no aceptada')
