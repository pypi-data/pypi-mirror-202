from triple_quote_clean import TripleQuoteCleaner


def test_guide_character():

    query = """--sql
    $$
        select *
        from some_database
    """

    target = """    select *\n    from some_database"""

    tqc = TripleQuoteCleaner()
    tqc.skip_top_lines = 1
    output = query >> tqc

    print("Input")
    print(query)

    print("Output")
    print(output)

    assert output == target, f"{output} != {target}"


if __name__ == "__main__":
    test_guide_character()
