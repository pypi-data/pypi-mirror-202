from typing import Any, Dict, List, Optional

import pydantic

from classiq.interface.executor.execution_preferences import ExecutionPreferences
from classiq.interface.generator.expressions import Expression
from classiq.interface.generator.function_call import (
    SUFFIX_RANDOMIZER,
    FunctionCall,
    WireDict,
)
from classiq.interface.generator.functions import (
    FunctionLibraryData,
    NativeFunctionDefinition,
    PortDeclaration,
)
from classiq.interface.generator.functions.port_declaration import (
    PortDeclarationDirection,
)
from classiq.interface.generator.model.constraints import Constraints
from classiq.interface.generator.model.preferences.preferences import Preferences
from classiq.interface.helpers.versioned_model import VersionedModel

MAIN_FUNCTION_NAME = "main"
DEFAULT_PORT_SIZE = 1


def _create_default_library() -> FunctionLibraryData:
    return FunctionLibraryData(
        functions=[NativeFunctionDefinition(name=MAIN_FUNCTION_NAME)]
    )


class Model(VersionedModel):
    """
    All the relevant data for generating quantum circuit in one place.
    """

    # Must be validated before logic_flow
    function_library: FunctionLibraryData = pydantic.Field(
        default_factory=_create_default_library,
        description="The user-defined custom function library.",
    )

    constraints: Constraints = pydantic.Field(default_factory=Constraints)

    def __init__(
        self,
        *,
        logic_flow: Optional[List[FunctionCall]] = None,
        inputs: Optional[WireDict] = None,
        outputs: Optional[WireDict] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if logic_flow:
            self._main_func.logic_flow.extend(logic_flow)
        if inputs:
            self.set_inputs(inputs)
        if outputs:
            self.set_outputs(outputs)

    @property
    def _main_func(self) -> NativeFunctionDefinition:
        return self.function_library.function_dict[
            MAIN_FUNCTION_NAME
        ]  # type:ignore[return-value]

    @property
    def logic_flow(self) -> List[FunctionCall]:
        return self._main_func.logic_flow

    @property
    def inputs(self) -> WireDict:
        return self._main_func.input_ports_wiring

    def set_inputs(self, value) -> None:
        self._update_main_declarations(value, PortDeclarationDirection.Input)
        self._main_func.input_ports_wiring.update(value)

    @property
    def outputs(self) -> WireDict:
        return self._main_func.output_ports_wiring

    def set_outputs(self, value) -> None:
        self._update_main_declarations(value, PortDeclarationDirection.Output)
        self._main_func.output_ports_wiring.update(value)

    execution_preferences: Optional[ExecutionPreferences] = pydantic.Field(default=None)
    preferences: Preferences = pydantic.Field(default_factory=Preferences)

    @pydantic.validator("preferences", always=True)
    def _seed_suffix_randomizer(cls, preferences: Preferences) -> Preferences:
        SUFFIX_RANDOMIZER.seed(preferences.random_seed)
        return preferences

    @pydantic.validator("preferences", always=True)
    def _align_backend_preferences(
        cls, preferences: Preferences, values: Dict[str, Any]
    ) -> Preferences:
        exec_pref: Optional[ExecutionPreferences] = values.get("execution_preferences")
        if exec_pref is not None and (
            preferences.backend_name is None
            or preferences.backend_service_provider is None
        ):
            preferences.backend_name = exec_pref.backend_preferences.backend_name
            preferences.backend_service_provider = (
                exec_pref.backend_preferences.backend_service_provider
            )
        return preferences

    def _update_main_declarations(
        self, value, direction: PortDeclarationDirection
    ) -> None:
        for port_name in value.keys():
            if port_name in self._main_func.port_declarations:
                direction = PortDeclarationDirection.Inout
            self._main_func.port_declarations[port_name] = PortDeclaration(
                name=port_name,
                size=Expression(expr=f"{DEFAULT_PORT_SIZE}"),
                direction=direction,
            )
