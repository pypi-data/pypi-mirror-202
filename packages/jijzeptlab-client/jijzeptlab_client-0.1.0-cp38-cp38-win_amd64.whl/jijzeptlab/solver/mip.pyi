from enum import Enum
from typing import Dict, List, Optional

import jijmodeling as jm
import mip

from jijzeptlab.compile import CompiledInstance as CompiledInstance
from jijzeptlab.exception import JijZeptLabSolverError as JijZeptLabSolverError
from jijzeptlab.utils.baseclass import (
    Option as Option,
    ResultWithDualVariables as ResultWithDualVariables
)
from pydantic import BaseModel as BaseModel

class MipModelOption(Option):
    ignore_constraint_names: List[str] = ...
    relaxed_variable_names: List[str] = ...
    relax_all_variables: bool = ...
    ignore_constraint_indices: Dict[str, List[List[int]]] = ...

class MipModelStatus(Enum):
    SUCCESS: str
    TRIVIALLY_INFEASIBLE: str

class MipModel:
    mip_model: mip.Model | None
    model_status: MipModelStatus
    def __init__(self, mip_model, mip_decoder, model_status) -> None: ...

class MipResultStatus(Enum):
    SUCCESS: str
    TRIVIALLY_INFEASIBLE: str

class MipResult(ResultWithDualVariables):
    mip_model: mip.Model | None
    status: MipResultStatus
    def to_sample_set(self) -> jm.SampleSet | None: ...
    def __init__(self, mip_model, mip_decoder, status) -> None: ...

def create_model(
    compiled_instance: CompiledInstance, option: Optional[MipModelOption] = ...
) -> MipModel: ...
def solve(mip_model: MipModel) -> MipResult: ...
