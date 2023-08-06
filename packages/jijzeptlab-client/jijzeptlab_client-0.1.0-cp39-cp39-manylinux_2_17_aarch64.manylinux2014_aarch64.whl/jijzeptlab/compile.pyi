from typing import Optional

import jijmodeling as jm

from jijzeptlab.jijzeptlab import (
    FixedVariables as FixedVariables,
    InstanceData as InstanceData
)
from jijzeptlab.utils.baseclass import Option as Option

class CompileOption(Option):
    needs_normalize: bool

class CompiledInstance:
    compile_option: CompileOption
    problem: jm.Problem
    instance_data: InstanceData
    fixed_variables: FixedVariables
    def append_constraint(
        self, constraint: jm.Constraint, instance_data: InstanceData
    ): ...
    def __init__(
        self, engine_instance, compile_option, problem, instance_data, fixed_variables
    ) -> None: ...

def compile_model(
    problem: jm.Problem,
    instance_data: InstanceData,
    fixed_variables: Optional[FixedVariables] = ...,
    option: Optional[CompileOption] = ...,
) -> CompiledInstance: ...
