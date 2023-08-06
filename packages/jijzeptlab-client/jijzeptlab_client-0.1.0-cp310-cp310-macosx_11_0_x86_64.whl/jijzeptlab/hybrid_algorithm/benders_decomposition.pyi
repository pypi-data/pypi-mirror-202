from enum import Enum
from typing import Any, Callable, List, Tuple

import jijmodeling as jm
import jijzeptlab as jzl

from _typeshed import Incomplete
from jijzeptlab.hybrid_algorithm.util import (
    convert_dual_variables_to_dense as convert_dual_variables_to_dense,
    merge_sampleset as merge_sampleset
)
from jijzeptlab.utils.baseclass import (
    Option as Option,
    Result as Result,
    ResultWithDualVariables as ResultWithDualVariables,
    StateModel as StateModel
)

logger: Incomplete

class InitializeOption(Option):
    slack_M_value: float

class UpdateCallback(Option):
    masterproblem_callback: Callable[[jzl.CompiledInstance], Result]
    subproblem_callback: Callable[[jzl.CompiledInstance], ResultWithDualVariables]

class BendersDecompositionResultStatus(Enum):
    SUCCESS: str
    MASTERPROBLEM_INFEASIBLE: str
    SUBPROBLEM_INFEASIBLE: str

class BendersDecompositionResult(Result):
    masterproblem_sampleset: jm.SampleSet | None
    subproblem_sampleset: jm.SampleSet | None
    original_compiled_model: jzl.CompiledInstance
    lower_bound: float
    upper_bound: float
    status: BendersDecompositionResultStatus
    def is_feasible(self) -> bool: ...
    def is_converge(self, tol: float = ...) -> bool: ...
    def to_sample_set(self) -> jm.SampleSet | None: ...
    def __init__(
        self,
        masterproblem_sampleset,
        subproblem_sampleset,
        original_compiled_model,
        lower_bound,
        upper_bound,
        _is_feasible,
        status,
    ) -> None: ...

class BendersDecompositionModel(StateModel):
    compiled_model: jzl.CompiledInstance
    master_decision_variables: List[jm.DecisionVariable]
    LARGE_CONSTANT: int
    LOGENC_RANGE: int
    FIXED_PREFIX: str
    RANDOMIZER_PREFIX: str
    BENDERS_COST_PLACEHOLDER: str
    DUAL_PREFIX: str
    FIXED_MASTER_PREFIX: str
    alpha_variable: jm.DecisionVariable
    option: InitializeOption | None
    original_problem: Incomplete
    original_instance_data: Incomplete
    original_fixed_variables: Incomplete
    fixed_placeholder: Incomplete
    masterproblem_randomizer: Incomplete
    subproblem_constraints_masterterm: Incomplete
    slack_M: Incomplete
    dummy_zero: Incomplete
    def __post_init__(self) -> None: ...
    compiled_masterproblem: Incomplete
    def reset(self, option: InitializeOption | None = ...): ...
    compiled_subproblem: Incomplete
    def update(
        self, callback: UpdateCallback, *args: Tuple[Any, ...], **kwargs: Any
    ) -> BendersDecompositionResult: ...
    def __init__(
        self,
        compiled_model,
        master_decision_variables,
        LARGE_CONSTANT,
        LOGENC_RANGE,
        FIXED_PREFIX,
        RANDOMIZER_PREFIX,
        BENDERS_COST_PLACEHOLDER,
        DUAL_PREFIX,
        FIXED_MASTER_PREFIX,
        alpha_variable,
        option,
    ) -> None: ...

def create_model(
    compiled_model: jzl.CompiledInstance,
    master_decision_variables: List[jm.DecisionVariable],
    alpha_variable: jm.DecisionVariable | None = ...,
    LARGE_CONSTANT: int | None = ...,
) -> BendersDecompositionModel: ...
