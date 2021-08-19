from weaverbird.backends.sql_translator.steps import translate_todate
from weaverbird.pipeline.steps import ToDateStep


def test_translate_simple_todate(query):
    step = ToDateStep(name='todate', column='raichu', format='%d/%m/%Y')

    query = translate_todate(
        step,
        query,
        index=1,
    )
    expected_transformed_query = (
        'WITH SELECT_STEP_0 AS (SELECT * FROM products), TODATE_STEP_1 AS (SELECT TOTO, FLORIZARRE, IFF(TRY_TO_DATE('
        'RAICHU) != NULL, TO_DATE(RAICHU, \'%d/%m/%Y\') , \'not-valid-date-format\') AS RAICHU ) FROM SELECT_STEP_0) '
    )
    assert query.transformed_query == expected_transformed_query
    assert query.selection_query == 'SELECT TOTO, RAICHU, FLORIZARRE FROM TODATE_STEP_1'
    assert query.query_name == 'TODATE_STEP_1'


def test_translate_automatic_guess_todate(query):
    step = ToDateStep(name='todate', column='raichu')

    query = translate_todate(
        step,
        query,
        index=1,
    )
    expected_transformed_query = (
        'WITH SELECT_STEP_0 AS (SELECT * FROM products), TODATE_STEP_1 AS (SELECT TOTO, FLORIZARRE, IFF(TRY_TO_DATE('
        'RAICHU) != NULL, TO_DATE(RAICHU) , \'not-valid-date-format\') AS RAICHU ) FROM SELECT_STEP_0) '
    )
    assert query.transformed_query == expected_transformed_query
    assert query.selection_query == 'SELECT TOTO, RAICHU, FLORIZARRE FROM TODATE_STEP_1'
    assert query.query_name == 'TODATE_STEP_1'
