from dune.translate.translate import _translate_query, _clean_dataset


def migrate_spark(query):
    """Migrate a Dune query from Spark SQL to DuneSQL"""
    return _translate_query(query, sqlglot_dialect="spark")


def migrate_postgres(query, dataset):
    """Migrate a Dune query from PostgreSQL to DuneSQL"""
    dataset = _clean_dataset(dataset)
    return _translate_query(query, sqlglot_dialect="postgres", dataset=dataset)
