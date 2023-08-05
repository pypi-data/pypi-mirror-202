from triple_quote_clean import TripleQuoteCleaner


def test_rshift():

    input_string = """hello world"""
    tqc = TripleQuoteCleaner()
    output = '\n' + input_string >> tqc

    print(output)

    assert output == input_string, f"{output} != {input_string}"


if __name__ == "__main__":
    test_rshift()
