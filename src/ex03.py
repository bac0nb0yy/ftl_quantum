import signal

import matplotlib
from matplotlib import pyplot as plt
from qiskit import QuantumCircuit, transpile
from qiskit.visualization import plot_histogram
from qiskit_aer import AerSimulator

signal.signal(
    signal.SIGINT,
    lambda *_: (print("\033[2Dftl_quantum: CTRL+C sent by user."), exit(1)),
)


SHOTS = 500

matplotlib.use("qtagg")


def main():
    qc = QuantumCircuit(2)

    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()

    qc.draw("mpl")
    plt.show()
    plt.close()

    simulator = AerSimulator()
    qc = transpile(qc, simulator)

    plot_histogram(
        {
            state: count / SHOTS
            for state, count in simulator.run(qc, shots=SHOTS).result().get_counts(qc).items()
        }
    )
    plt.ylabel("Probabilities")
    plt.show()


if __name__ == "__main__":
    main()
