# Aplicando o algoritmo de Grover e QRAM para resolver o puzzle game lights out

![logo](figures/tdc-logo-post.png)

Repositório para armazenar o conteúdo da palestra: Aplicando o algoritmo de Grover e QRAM para resolver o puzzle game lights out, apresentada na The Developer's Conference - [TDC_2022](https://thedevconf.com/tdc/2022/business/trilha-quantum-computing) na trilha de quantum computing. 

## Descrição:

O algoritmo de Grover é um algoritmo quântico que nos permite executar buscas não estruturadas de forma mais rápida que as propostas clássicas (complexidade do algoritmo de Grover O(sqrt(N)) e complexidade dos algoritmos clássicos O(N)). Além de buscas, esse algoritmo pode ser adaptado para resolver sistemas de equações em modulo 2 e portanto poderia ser usado para resolver o puzzle game lights out. Gostaria também de apresentar a QRAM, definida por Seth Lloyd, e mostrar como combinar ela com o algoritmo de Grover para resolver várias configurações do puzzle game lights out em paralelo.

## Exemplo:

```python
from lights_out import LightsOut
from solver import LightsOutSolver
from qiskit import Aer, execute
from qiskit.visualization import plot_histogram

backend = Aer.get_backend("qasm_simulator")

game_layout = [0,1,1,0]

game1 = LightsOut(layout = game_layout)
games_list = [game1]
game_solver = LightsOutSolver(games = games_list)

qc = game_solver.create_solver_qc()
qc = qc.reverse_bits()

counts = execute(experiments = qc, backend = backend, shots = 8192).result().get_counts()
plot_histogram(counts)

results = [(key, value) for key, value in counts.items() if value > 100]
```

![circuito](/figures/circuito_exemplo.png)
### Figura 1: Circuito gerado pelo trecho de código acima.

## Referências:

[[1](https://arxiv.org/abs/quant-ph/9605043)] Lov K. Grover. A fast quantum mechanical algorithm for database search

[[2](https://www.youtube.com/watch?v=ePr2MgQkqL0&list=PLOFEBzvs-VvrhKYASly1BXo1AdPyoCsor&index=6)] Dinner Party using Grover's Algorithm — Programming on Quantum Computers — Coding with Qiskit S2E5

[[3](https://github.com/qiskit-community/IBMQuantumChallenge2020/blob/main/exercises/week-2/ex_2a_en.ipynb)] IBM Quantum Challenge 2020 - Exercício 2-A

[[4](https://github.com/qiskit-community/IBMQuantumChallenge2020/blob/main/exercises/week-2/ex_2b_en.ipynb)] IBM Quantum Challenge 2020 - Exercício 2-B

[[5](https://qiskit.org/textbook/ch-algorithms/grover.html)] Qiskit Textbook - Capítulo 3.8 - Grover's Algorithm

[[6](https://youtu.be/iJX794qJIpY?t=1394)] Qiskit Global Summer School 2020 - Writing and Running Quantum Programs - Part 2

[[7](https://www.youtube.com/watch?v=0RPFWZj7Jm0&list=PLOFEBzvs-VvrhKYASly1BXo1AdPyoCsor&index=3)] Grovers Algorithm — Programming on Quantum Computers — Coding with Qiskit S2E3

[[8](https://arxiv.org/abs/0708.1879)] Artigo do Seth Lloyd (e colaboradores) sobre QRAM

[[9](https://en.wikipedia.org/wiki/Lights_Out_(game))] Artigo da Wikipedia Lights Out (game)

[[10](https://mathworld.wolfram.com/LightsOutPuzzle.html)] Wolfram MathWorld - Lights Out Puzzle

[[11](https://qiskit.org/textbook/ch-states/atoms-computation.html)] Qiskit Textbook - Capítulo 1.2 - The Atoms of Computation