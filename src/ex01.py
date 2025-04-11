import os
import signal
import sys
from dataclasses import dataclass

from dotenv import load_dotenv
from qiskit_ibm_runtime import QiskitRuntimeService

signal.signal(
    signal.SIGINT,
    lambda *_: (print("\033[2Dftl_quantum: CTRL+C sent by user."), exit(1)),
)


NEWLINES = 3


@dataclass
class Backend:
    name: str
    pending_jobs: int
    n_qubits: int
    simulator: bool


def load_key(key):
    value = os.getenv(key)
    if not value:
        print(f"Missing key: {key}")
        sys.exit(1)
    return value


def n_digits(n):
    digits = 1
    while n >= 10:
        digits += 1
        n //= 10
    return digits


def format_int(n, padding, s):
    return f"{n:>{padding}} {s}{'s' if n > 1 else ' '}"


def list_quantum_computers(service):
    backends = [
        Backend(
            backend.name,
            backend.status().pending_jobs,
            backend.configuration().n_qubits,
            backend.configuration().simulator,
        )
        for backend in service.backends()
    ]

    mx_name = max(len(backend.name) for backend in backends)
    mx_pending_jobs = max(n_digits(backend.pending_jobs) for backend in backends)
    mx_n_qubits = max(n_digits(backend.n_qubits) for backend in backends)

    for i, (simulator, s) in enumerate([(True, "Simulated"), (False, "Real")]):
        if i > 0:
            print(end="\n" * NEWLINES)
        print(f"{s} quantum computers:")
        for backend in backends:
            if simulator == backend.simulator:
                print(
                    f"\t{backend.name:<{mx_name}}",
                    f"has {format_int(backend.pending_jobs, mx_pending_jobs, 'queue')}",
                    f"with {format_int(backend.n_qubits, mx_n_qubits, 'qubit')}",
                )


def main():
    load_dotenv()
    QISKIT_API_KEY = load_key("QISKIT_API_KEY")
    service = QiskitRuntimeService(
        channel="ibm_quantum",
        token=QISKIT_API_KEY,
    )

    list_quantum_computers(service)


if __name__ == "__main__":
    main()
