from typing import List, Literal, Optional

from pandas import DataFrame
from pydantic import Field
from pydantic.main import BaseModel

from weaverbird.steps.base import BaseStep
from weaverbird.types import ColumnName, PopulatedWithFieldnames

AggregateFn = Literal['avg', 'sum', 'min', 'max', 'count', 'first', 'last']

functions_aliases = {'avg': 'mean'}


class Aggregation(BaseModel):
    class Config(PopulatedWithFieldnames):
        ...

    new_columns: List[ColumnName] = Field(alias='newcolumns')
    agg_function: AggregateFn = Field(alias='aggfunction')
    columns: List[ColumnName]


def get_aggregate_fn(agg_function: str) -> str:
    if agg_function in functions_aliases:
        return functions_aliases[agg_function]
    return agg_function


def make_aggregation(aggregation: Aggregation) -> dict:
    return {
        column_name: get_aggregate_fn(aggregation.agg_function)
        for column_name in aggregation.columns
    }


class AggregateStep(BaseStep):
    name = Field('aggregate', const=True)
    on: List[ColumnName] = []
    aggregations: List[Aggregation]
    keep_original_granularity: Optional[bool] = Field(
        default=False, alias='keepOriginalGranularity'
    )

    class Config(PopulatedWithFieldnames):
        ...

    def execute(self, df: DataFrame, domain_retriever=None, execute_pipeline=None):
        group_by_columns = self.on

        # if no group is specified, we create a pseudo column with a single value
        if len(group_by_columns) == 0:
            group_by_columns = ['__VQB__GROUP_BY__']
            df = df.assign(**{group_by_columns[0]: True})

        grouped_by_df = df.groupby(group_by_columns)
        aggregated_cols = []
        for aggregation in self.aggregations:
            for col, new_col in zip(aggregation.columns, aggregation.new_columns):
                agg_serie = (
                    grouped_by_df[col]
                    .agg(get_aggregate_fn(aggregation.agg_function))
                    .rename(new_col)
                )
                aggregated_cols.append(agg_serie)

        df_result = DataFrame(aggregated_cols).transpose().reset_index()

        # it is faster this way, than to transform the original df
        if self.keep_original_granularity:
            df_result = df.merge(df_result, on=group_by_columns, how='left')

        # we do not want the pseudo column to ever leave this function
        if len(self.on) == 0:
            del df_result[group_by_columns[0]]
        return df_result
