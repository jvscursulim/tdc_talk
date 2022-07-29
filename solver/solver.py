import numpy as np
from typing import List
from lights_out import LightsOut
from qiskit.circuit import ClassicalRegister, QuantumCircuit, QuantumRegister


class LightsOutSolver:
    """Lights out solver class."""
    
    def __init__(self, games: List[LightsOut]) -> None:
        """
        Args:
            games (List[LightsOut]): A list with games layout.

        Raises:
            TypeError: If the input is not a List.
        """
        if isinstance(games, List):
            
            self.games = games
        else:
            
            raise TypeError("The input is not a List!")
        
    def create_solver_qc(self) -> QuantumCircuit:
        """Creates the quantum circuit that will be used
        to solve the game.

        Raises:
            ValueError: If games is empty!

        Returns:
            QuantumCircuit: A quantum circuit that solves
            the game.
        """
        if len(self.games) == 0:
            
            raise ValueError("The list of games is empty!")
        else:
            
            num_qubits = self.games[0].layout_length()
            qubits = QuantumRegister(size = num_qubits, name = "sol_vector")
            ancilla = QuantumRegister(size = num_qubits, name = "ancilla")
            bits = ClassicalRegister(size = num_qubits, name = "bits")
            
            if len(self.games) == 1:
                
                qc = QuantumCircuit(qubits, ancilla, bits)
                qc.h(qubit = qubits)
                qc.barrier()
                
                for index, item in enumerate(self.games[0].layout):
                    
                    if item == 0:
                        
                        qc.x(qubit = ancilla[index])
                
                qc.barrier()
            else:
                
                qram = QuantumRegister(size = len(self.games)/2, name = "qram_address")
                qram_address_bit = ClassicalRegister(size = len(self.games)/2, name = "qram_address_bits")
                qc = QuantumCircuit(qubits, ancilla, qram, bits, qram_address_bit)
                
                qc.h(qubit = qubits)
                qc.h(qubit = qram)
                qc.barrier()
                
                binary_index_list = [bin(i)[bin(i).index('b')+1:] for i in range(len(self.games))]
                length_list = [len(binary) for binary in binary_index_list]
                new_binary_list = []

                for item in binary_index_list:
    
                    if len(item) < max(length_list):
        
                        new_item = '0'*(max(length_list)-len(item))+item
                        new_binary_list.append(new_item)
                    elif len(item) == max(length_list):
        
                        new_binary_list.append(item)
                
                for i in range(len(self.games)):
                    
                    for idx, char in enumerate(new_binary_list[i]):
                                
                        if char == '0':
                                    
                            qc.x(qubit = qram[idx])
                    
                    for index, item in enumerate(self.games[i].layout):
                        
                        if item == 0:
                            
                            qc.mct(control_qubits = qram, target_qubit = ancilla[index])

                    for idx, char in enumerate(new_binary_list[i]):
                                
                                if char == '0':
                                    
                                    qc.x(qubit = qram[idx])
                    qc.barrier()
                
            N = 2**self.games[0].layout_length()
                
            for _ in range(int(np.sqrt(N))-1):
                
                for index_row, row in enumerate(self.game_possibles_movements()):
                        
                    for index_item, item in enumerate(row):
                            
                        if item == 1:
                                
                            qc.cx(control_qubit = qubits[index_item], target_qubit = ancilla[index_row])
                    qc.barrier()
                    
                qc.h(qubit = ancilla[-1])    
                qc.mct(control_qubits = ancilla[:-1], target_qubit = ancilla[-1])
                qc.h(qubit = ancilla[-1])
                qc.barrier()
                    
                for index_row, row in enumerate(self.game_possibles_movements()):
                        
                    for index_item, item in enumerate(row):
                            
                        if item == 1:
                                
                            qc.cx(control_qubit = qubits[index_item], target_qubit = ancilla[index_row])
                    qc.barrier()
                        
                qc.h(qubit = qubits)
                qc.x(qubit = qubits)
                qc.h(qubit = qubits[-1])
                qc.mct(control_qubits = qubits[:-1], target_qubit = qubits[-1])
                qc.h(qubit = qubits[-1])
                qc.x(qubit = qubits)
                qc.h(qubit = qubits)
                qc.barrier()
                
            qc.measure(qubit = qubits, cbit = bits)
            if len(self.games) > 1:
                
                qc.measure(qubit = qram, cbit = qram_address_bit)
                
            return qc
            
    def game_possibles_movements(self) -> list:
        
        layout_length = self.games[0].layout_length()
        n_rows = int(np.sqrt(layout_length))
        matrix_entries_positions = [[(i,j) for j in range(n_rows)] for i in range(n_rows)]
        tuples_list = []
        
        for tp_position in matrix_entries_positions:
            
            for tp in tp_position:
                
                tuples_list.append(tp)
        
        possibles_movements_matrix = []
            
        if n_rows == 2:
    
            for index, tp in enumerate(tuples_list):
    
                aux = [0 for _ in range(layout_length)]
                aux[index] = 1
        
                if tp[0] == 0 and tp[1] == 0:
        
                    aux[tuples_list.index((tp[0]+1,tp[1]))] = 1
                    aux[tuples_list.index((tp[0], tp[1]+1))] = 1
                elif tp[0] == 0 and tp[1] == 1:
            
                    aux[tuples_list.index((tp[0], tp[1]-1))] = 1
                    aux[tuples_list.index((tp[0]+1, tp[1]))] = 1
                elif tp[0] == 1 and tp[1] == 1:
        
                    aux[tuples_list.index((tp[0]-1,tp[1]))] = 1
                    aux[tuples_list.index((tp[0], tp[1]-1))] = 1
                elif tp[0] == 1 and tp[1] == 0:
            
                    aux[tuples_list.index((tp[0], tp[1]+1))] = 1
                    aux[tuples_list.index((tp[0]-1, tp[1]))] = 1
        
                possibles_movements_matrix.append(aux)
            
            return possibles_movements_matrix
        else:
    
            for index, tp in enumerate(tuples_list):
    
                aux = [0 for _ in range(layout_length)]
                aux[index] = 1
        
                if tp[0] == 0 and tp[1] == 0:
        
                    aux[tuples_list.index((tp[0]+1,tp[1]))] = 1
                    aux[tuples_list.index((tp[0], tp[1]+1))] = 1
                elif tp[0] == 0 and (tp[1] > 0 and tp[1] < n_rows-1):
            
                    aux[tuples_list.index((tp[0]+1,tp[1]))] = 1
                    aux[tuples_list.index((tp[0], tp[1]+1))] = 1
                    aux[tuples_list.index((tp[0], tp[1]-1))] = 1
                elif tp[0] == 0 and tp[1] == n_rows-1:
            
                    aux[tuples_list.index((tp[0], tp[1]-1))] = 1
                    aux[tuples_list.index((tp[0]+1, tp[1]))] = 1
                elif (tp[0] > 0 and tp[0] < n_rows-1) and tp[1] == 0:
            
                    aux[tuples_list.index((tp[0]-1, tp[1]))] = 1
                    aux[tuples_list.index((tp[0], tp[1]+1))] = 1
                    aux[tuples_list.index((tp[0]+1, tp[1]))] = 1
                elif tp[0] == n_rows-1 and tp[1] == 0:
            
                    aux[tuples_list.index((tp[0], tp[1]+1))] = 1
                    aux[tuples_list.index((tp[0]-1, tp[1]))] = 1
                elif tp[0] == n_rows-1 and (tp[1] > 0 and tp[1] < n_rows-1):
            
                    aux[tuples_list.index((tp[0]-1,tp[1]))] = 1
                    aux[tuples_list.index((tp[0], tp[1]+1))] = 1
                    aux[tuples_list.index((tp[0], tp[1]-1))] = 1    
                elif tp[0] == n_rows-1 and tp[1] == n_rows-1:
        
                    aux[tuples_list.index((tp[0]-1,tp[1]))] = 1
                    aux[tuples_list.index((tp[0], tp[1]-1))] = 1
                elif (tp[0] > 0 and tp[0] < n_rows-1) and tp[1] == n_rows-1:
            
                    aux[tuples_list.index((tp[0]-1, tp[1]))] = 1
                    aux[tuples_list.index((tp[0], tp[1]-1))] = 1
                    aux[tuples_list.index((tp[0]+1, tp[1]))] = 1
                else:
            
                    aux[tuples_list.index((tp[0]-1, tp[1]))] = 1
                    aux[tuples_list.index((tp[0], tp[1]-1))] = 1
                    aux[tuples_list.index((tp[0]+1, tp[1]))] = 1
                    aux[tuples_list.index((tp[0], tp[1]+1))] = 1
        
                possibles_movements_matrix.append(aux)
                
            return possibles_movements_matrix