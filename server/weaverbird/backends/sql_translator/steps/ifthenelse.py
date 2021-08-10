from weaverbird.backends.sql_translator.steps.utils.query_transformation import (
    build_selection_query,
)
from weaverbird.backends.sql_translator.types import (
    SQLPipelineTranslator,
    SQLQuery,
    SQLQueryDescriber,
    SQLQueryRetriever,
)
from weaverbird.pipeline.steps import IfthenelseStep


def recurse_format_else(step: IfthenelseStep) -> str:
    """
    In a case of a nested if then else, we're going to loop until the type of else_value's step
    is different from IfthenelseStep type

    params:
    step: IfthenelseStep
    """
    composed_query: str = "/-*-/"
    while type(step.else_value) == IfthenelseStep:
        composed_query = composed_query.replace(
            "/-*-/",
            f"""(SELECT IF({step.condition}, {step.then}, /-*-/) AS {step.new_column}""",
        )
        step = step.else_value

    return composed_query.replace(
        "/-*-/",
        f"""(SELECT IF({step.condition}, {step.then}, {str(step.else_value)}) AS {step.new_column}""",
    )


def translate_ifthenelse(
    step: IfthenelseStep,
    query: SQLQuery,
    index: int,
    sql_query_retriever: SQLQueryRetriever = None,
    sql_query_describer: SQLQueryDescriber = None,
    sql_translate_pipeline: SQLPipelineTranslator = None,
) -> SQLQuery:
    query_name = f'IFTHENELSE_STEP_{index}'

    new_query = SQLQuery(
        query_name=query_name,
        transformed_query=f"""{query.transformed_query}, {query_name} AS"""
        f""" {recurse_format_else(step)}"""
        f""" FROM {query.query_name})""",
        selection_query=build_selection_query(query.metadata_manager.tables_metadata, query_name),
        metadata_manager=query.metadata_manager,
    )
    return new_query