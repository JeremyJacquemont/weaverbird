from typing import Dict

from ..types import SQLStepTranslator
from .aggregate import translate_aggregate
from .filter import translate_filter
from .ifthenelse import translate_ifthenelse
from .select import translate_select
from .table import translate_table

sql_steps_translators: Dict[str, SQLStepTranslator] = {
    'domain': translate_table,  # type ignore # TODO to update
    'filter': translate_filter,
    'aggregate': translate_aggregate,
    'select': translate_select,
    'ifthenelse': translate_ifthenelse,
}