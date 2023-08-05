import qiskit
from qiskit.providers import  BackendV1
from qiskit.providers.provider import ProviderV1
from qiskit.providers.models import BackendConfiguration
from qiskit_aer import AerSimulator
from qiskit.providers.options import Options

class QuantierBackend(BackendV1):
    def __init__(self):
        configuration = BackendConfiguration(
            backend_name='simple_backend',
            backend_version='1.0.0',
            n_qubits=32,
            basis_gates=['u1', 'u2', 'u3', 'cx', 'id'],
            simulator=True,
            local=True,
            conditional=False,
            open_pulse=False,
            memory=True,
            max_shots=1000000,
            max_experiments=1,
            gates=[],
            coupling_map=None
        )
        self._aer_simulator = AerSimulator()
        super().__init__(configuration=configuration)

    def run(self, qobj, **kwargs):
        return self._aer_simulator.run(qobj, **kwargs)

    @classmethod
    def _default_options(cls):
        return Options()
    
class QuantierProvider(ProviderV1):
    def __init__(self):
        super().__init__()
        self._backend = QuantierBackend()
        self._simulator = AerSimulator()

    def get_backend(self, name=None, **kwargs):
        if name is None or name.lower() == 'quantier_simulator':
            return self._simulator
        elif name.lower() == 'quantier':
            return self._backend
        else:
            raise qiskit.providers.exceptions.QiskitBackendNotFoundError('Backend not found')

    def backends(self, name=None, **kwargs):
        if name is None:
            return [self._simulator, self._backend]
        if name.lower() == 'quantier':
            return [self._backend]
        if name.lower() == 'quantier_simulator':
            return [self._simulator]
        else:
            return []

provider = QuantierProvider()
