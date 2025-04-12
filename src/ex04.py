import signal

import matplotlib
from dotenv import load_dotenv
from matplotlib import pyplot as plt
from qiskit import QuantumCircuit, transpile
from qiskit.visualization import plot_histogram
from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit_ibm_runtime import SamplerV2 as Sampler

from ex01 import load_key

signal.signal(
    signal.SIGINT,
    lambda *_: (print("\033[2Dftl_quantum: CTRL+C sent by user."), exit(1)),
)

SHOTS = 500
matplotlib.use("qtagg")


def choose_backend():
    load_dotenv()
    QISKIT_API_KEY = load_key("QISKIT_API_KEY")
    service = QiskitRuntimeService(
        channel="ibm_quantum",
        token=QISKIT_API_KEY,
    )

    backend = service.least_busy(operational=True, simulator=False)
    if not backend:
        raise RuntimeError("No backends available.")
    return backend


def main():
    qc = QuantumCircuit(2)

    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()

    qc.draw("mpl")
    plt.show()
    plt.close()

    backend = choose_backend()
    qc = transpile(qc, backend)

    plot_histogram(
        {
            state: count / SHOTS
            for state, count in Sampler(mode=backend)
            .run([qc])
            .result()[0]
            .data.res.get_counts()
            .items()
        }
    )
    plt.ylabel("Probabilities")
    plt.show()


if __name__ == "__main__":
    main()
