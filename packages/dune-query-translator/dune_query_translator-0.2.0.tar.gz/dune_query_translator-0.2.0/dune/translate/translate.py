import re

from sqlglot import ParseError

from dune.translate.errors import TranslationError
from dune.translate.helpers import (
    prep_query,
    quoted_param_left_placeholder,
    quoted_param_right_placeholder,
    add_warnings_and_banner,
    transforms,
    fix_bytearray_param,
    fix_bytearray_lower,
)


def translate(query, dialect, dataset):
    """Translate a query into DuneSQL"""
    if dialect not in ("spark", "postgres"):
        raise ValueError(f"Unknown dialect: {dialect}")
    return _translate_query_sqlglot(query, dialect, dataset.lower())


def _translate_query_sqlglot(query, sqlglot_dialect, dataset=None):
    """Translate a query using SQLGLot plus custom rules"""
    try:
        # note that you can't use lower() in any returns, because that affects table name and parameters

        # Insert placeholders for the parameters we use in Dune (`{{ param }}`), SQLGlot doesn't handle those
        query = query.replace("{{", quoted_param_left_placeholder).replace("}}", quoted_param_right_placeholder)
        query_tree = prep_query(query, sqlglot_dialect)
        query_tree = transforms(query_tree, sqlglot_dialect, dataset)
        query = query_tree.sql(dialect="trino", pretty=True)

        # Replace placeholders with Dune params again
        query = query.replace(quoted_param_left_placeholder, "{{").replace(quoted_param_right_placeholder, "}}")
        query = fix_bytearray_param(query)
        query = fix_bytearray_lower(query)

        return add_warnings_and_banner(query)
    except ParseError as e:
        # SQLGlot inserts terminal style colors to emphasize error location.
        # We remove these, as they mess up the formatting.
        # Also, don't leak intermediate param syntax in error message
        error_message = (
            str(e)
            .replace("\x1b[4m", "")
            .replace("\x1b[0m", "")
            .replace(quoted_param_left_placeholder, "{{")
            .replace(quoted_param_right_placeholder, "}}")
        )
        # Remove Line and Column information, since it's outdated due to previous transforms.
        error_message = re.sub(
            ". Line [0-9]+, Col: [0-9]+.",
            ".",
            error_message,
        )
        raise TranslationError(error_message)
