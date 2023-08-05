from triple_quote_clean import TripleQuoteCleaner


def test_query():

    query = """--sql
        select *
        from some_database
    """

    target = """select *\nfrom some_database"""

    tqc = TripleQuoteCleaner()
    tqc.skip_top_lines = 1
    output = query >> tqc

    assert output == target, f"{output} != {target}"


if __name__ == "__main__":
    test_query()
