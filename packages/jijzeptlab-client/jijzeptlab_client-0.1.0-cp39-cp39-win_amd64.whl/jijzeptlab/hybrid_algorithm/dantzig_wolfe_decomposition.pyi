from dataclasses import dataclass as dataclass
from typing import Any, Callable, Dict, List, Optional, Tuple

import jijmodeling as jm
import jijzeptlab as jzl

from _typeshed import Incomplete
from jijmodeling.type_annotations import SparseSolution as SparseSolution
from jijzeptlab.hybrid_algorithm.exception import (
    CannotDecomposeError as CannotDecomposeError
)
from jijzeptlab.hybrid_algorithm.util import (
    convert_dual_variables_to_dense as convert_dual_variables_to_dense,
    merge_all_samplesets as merge_all_samplesets,
    merge_sampleset as merge_sampleset
)

logger: Incomplete

class DantzigWolfeDecomposition:
    LARGE_CONSTANT: int
    BASIS_PREFIX: str
    U_PREFIX: str
    SIGMA_PREFIX: str
    LAMBDA_PREFIX: str
    DualVariableType = Dict[str, Dict[Tuple[int, ...], float]]
    problem: Incomplete
    masterproblem_callback: Incomplete
    subproblem_callback: Incomplete
    separated_constraints: Incomplete
    overlapped_constraints: Incomplete
    num_feas: Incomplete
    deci_vars: Incomplete
    basis_placeholder: Incomplete
    u: Incomplete
    lambd: Incomplete
    slack_v: Incomplete
    slack_w: Incomplete
    slack_M: Incomplete
    separated_constraint_decivars: Incomplete
    instance_data_masterproblem: Incomplete
    instance_data_subproblem: Incomplete
    def __init__(
        self,
        compiled_instance: jzl.CompiledInstance,
        separated_constraints_label: List[List[str]],
        overlapped_constraints_label: List[str],
        masterproblem_callback: Callable[
            [jm.Problem, dict, Tuple[Any, ...], Any],
            Optional[Tuple[jm.SampleSet, DualVariableType]],
        ],
        subproblem_callback: Callable[
            [jm.Problem, dict, Tuple[Any, ...], Any],
            Optional[Tuple[jm.SampleSet, DualVariableType]],
        ],
        separated_objectives: Optional[List[jm.Expression]] = ...,
        overlapped_constraint_elements: Optional[Dict[str, List[jm.Expression]]] = ...,
        slack_M_value: float = ...,
    ) -> None: ...
    def initialize(self, slack_M_value: float = ...): ...
    @property
    def separated_subproblems(self) -> List[jm.Problem]: ...
    @property
    def shifted_separated_subproblems(self) -> List[jm.Problem]: ...
    @property
    def masterproblem(self) -> jm.Problem: ...
    @property
    def always_feasible_masterproblem(self) -> jm.Problem: ...
    @property
    def convergence_parameter(self) -> float: ...
    @property
    def current_solution(self) -> jm.SampleSet: ...
    @property
    def current_dual_variables(self) -> DualVariableType: ...
    def is_feasible(self) -> bool: ...
    def is_converge(self, tol: float = ...) -> bool: ...
    def update(
        self, *args: Tuple[Any, ...], **kwargs: Any
    ) -> Tuple[Optional[jm.SampleSet], Optional[List[jm.SampleSet]]]: ...
