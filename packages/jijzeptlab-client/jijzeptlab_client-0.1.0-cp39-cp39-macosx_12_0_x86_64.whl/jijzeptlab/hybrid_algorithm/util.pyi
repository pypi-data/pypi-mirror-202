import typing as tp

import jijmodeling as jm
import numpy as np

from jijmodeling.sampleset.record import SparseSolution as SparseSolution

def show_decivar_dependency(
    problem: jm.Problem,
) -> tp.Dict[tp.Tuple[str, ...], tp.List[str]]: ...
def convert_dual_variables_to_dense(
    input_dual_variables: tp.Dict[tp.Tuple[int, ...], float]
) -> np.ndarray: ...
def merge_sampleset(
    sampleset1: jm.SampleSet, sampleset2: jm.SampleSet
) -> jm.SampleSet: ...
def merge_all_samplesets(samplesets: tp.List[jm.SampleSet]) -> jm.SampleSet: ...
