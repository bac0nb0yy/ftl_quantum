import matplotlib
from matplotlib import pyplot as plt
from qiskit import QuantumCircuit

matplotlib.use("qtagg")


def main():
    qc = QuantumCircuit(1)
    qc.h(0)
    qc.draw("mpl")
    plt.show()


if __name__ == "__main__":
    main()
