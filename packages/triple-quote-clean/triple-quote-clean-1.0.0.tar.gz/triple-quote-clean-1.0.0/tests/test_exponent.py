from triple_quote_clean import TripleQuoteCleaner


def test_exponent():

    query = """--sql
        select *
        from some_database
    """

    target = """select *\nfrom some_database\nwhere  some_value = 3"""

    tqc = TripleQuoteCleaner()
    tqc.skip_top_lines = 1
    output = tqc ** query + "\nwhere  some_value = 3"

    assert output == target, f"{output} != {target}"


if __name__ == "__main__":
    test_exponent()
