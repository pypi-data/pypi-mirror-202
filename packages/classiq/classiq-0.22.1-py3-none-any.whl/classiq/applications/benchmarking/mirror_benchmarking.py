from copy import deepcopy

from classiq.interface.generator.model.preferences.preferences import (
    Preferences,
    QuantumFormat,
    TranspilationOption,
)
from classiq.interface.generator.result import GeneratedCircuit

from classiq._internals.async_utils import Asyncify
from classiq.model.model import Model
from classiq.quantum_functions.decorators import quantum_function as qfunc
from classiq.quantum_functions.function_library import QASM_INTRO, FunctionLibrary
from classiq.quantum_register import QReg, ZeroQReg

_MB_NAME: str = "mirror_benchmarking"
_MB_FUNCTION_LIBRARY_NAME: str = f"{_MB_NAME}_function_library"


class MirrorBenchmarking(metaclass=Asyncify):
    def __init__(self, model: Model):
        self.functional_model: Model = model
        self.functional_model._model.preferences = self.get_functional_preferences(
            model.preferences
        )

    async def synthesize_async(self) -> GeneratedCircuit:
        mb_model = await self._mirror_benchmarking_model_async()
        return await mb_model.synthesize_async()

    async def _mirror_benchmarking_model_async(self) -> Model:
        functional_circuit: GeneratedCircuit = (
            await self.functional_model.synthesize_async()
        )

        num_qubits: int = functional_circuit.data.width
        circuit_qasm_list = functional_circuit.qasm.split(QASM_INTRO)  # type: ignore[union-attr]
        if not circuit_qasm_list:
            raise AssertionError(
                "Functional model synthesis did not result in a legal QASM"
            )
        circuit_qasm: str = circuit_qasm_list[-1]

        @qfunc
        def functional_model_function(reg: ZeroQReg[num_qubits]) -> QReg[num_qubits]:  # type: ignore[type-arg, valid-type]
            return QASM_INTRO + circuit_qasm  # type: ignore[return-value]

        model_function_library = FunctionLibrary(
            functional_model_function,
            name=_MB_FUNCTION_LIBRARY_NAME,
        )

        mb_model = Model(
            preferences=self.get_mirror_benchmarking_preferences(
                self.functional_model.preferences
            )
        )
        mb_model.include_library(model_function_library)
        inner_wires = mb_model.functional_model_function()
        mb_model.functional_model_function(in_wires=inner_wires, is_inverse=True)
        return mb_model

    @staticmethod
    def get_functional_preferences(preferences: Preferences) -> Preferences:
        functional_preferences = deepcopy(preferences)
        functional_preferences.output_format = [QuantumFormat.QASM]
        return functional_preferences

    @staticmethod
    def get_mirror_benchmarking_preferences(preferences: Preferences) -> Preferences:
        mb_preferences = deepcopy(preferences)
        mb_preferences.transpilation_option = TranspilationOption.DECOMPOSE
        return mb_preferences
