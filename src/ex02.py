import matplotlib
from matplotlib import pyplot as plt
from qiskit import QuantumCircuit, transpile
from qiskit.visualization import plot_histogram
from qiskit_aer import AerSimulator

SHOTS = 500
matplotlib.use("qtagg")


def main():
    qc = QuantumCircuit(1, 1)
    qc.h(0)
    qc.measure(0, 0)

    simulator = AerSimulator()
    qc = transpile(qc, simulator)

    result = simulator.run(qc, shots=SHOTS).result()
    counts = result.get_counts(qc)
    normalized_counts = {state: count / SHOTS for state, count in counts.items()}

    plot_histogram(normalized_counts)
    plt.ylabel("Probabilities")
    plt.show()


if __name__ == "__main__":
    main()
