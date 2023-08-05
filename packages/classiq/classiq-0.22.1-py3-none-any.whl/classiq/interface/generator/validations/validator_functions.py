from typing import Iterable, List, Sized, Tuple, TypeVar, Union

import numpy as np

from classiq.interface.helpers.custom_pydantic_types import PydanticProbabilityFloat

from classiq import RegisterUserInput

SUM_TO_ONE_SENSITIVITY = 8

Amplitude = TypeVar("Amplitude", Tuple[float, ...], List[complex])
Numeric = (float, int)
RegisterOrConst = Union[RegisterUserInput, float]
RegisterOrConstOrDict = Union[RegisterUserInput, float, dict]


def _is_power_of_two(vector: Sized) -> bool:
    n = len(vector)
    return (n != 0) and (n & (n - 1) == 0)


def is_amplitudes_sum_to_one(amp: Iterable[complex]) -> bool:
    return round(sum(abs(np.array(amp)) ** 2), SUM_TO_ONE_SENSITIVITY) == 1


def is_probabilities_sum_to_one(pro: Iterable[PydanticProbabilityFloat]) -> bool:
    return round(sum(pro), SUM_TO_ONE_SENSITIVITY) == 1


def validate_amplitudes(amp: Amplitude) -> Amplitude:
    if not is_amplitudes_sum_to_one(amp):
        raise ValueError("Amplitudes do not sum to 1")
    if not _is_power_of_two(amp):
        raise ValueError("Amplitudes length must be power of 2")
    return amp


def validate_probabilities(cls, pmf):
    if not is_probabilities_sum_to_one(pmf):
        raise ValueError("Probabilities do not sum to 1")
    if not _is_power_of_two(pmf):
        raise ValueError("Probabilities length must be power of 2")
    return pmf


def validate_reg(value: RegisterOrConstOrDict, name: str) -> RegisterOrConst:
    if isinstance(value, Numeric):
        return value
    elif isinstance(value, RegisterUserInput):
        return value.revalued(name=name)
    elif isinstance(value, dict):
        return RegisterUserInput(**value).revalued(name=name)
    raise ValueError("Unrecognized value type")
