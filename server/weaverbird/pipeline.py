from typing import List, Union

from pydantic import BaseModel

from weaverbird.steps import (
    AppendStep,
    ArgmaxStep,
    ConcatenateStep,
    ConvertStep,
    CumSumStep,
    DateExtractStep,
    DomainStep,
    FilterStep,
    FormulaStep,
    JoinStep,
    RenameStep,
)

PipelineStep = Union[
    AppendStep,
    ArgmaxStep,
    ConcatenateStep,
    ConvertStep,
    CumSumStep,
    DateExtractStep,
    DomainStep,
    FilterStep,
    FormulaStep,
    JoinStep,
    RenameStep,
]


class Pipeline(BaseModel):
    steps: List[PipelineStep]
