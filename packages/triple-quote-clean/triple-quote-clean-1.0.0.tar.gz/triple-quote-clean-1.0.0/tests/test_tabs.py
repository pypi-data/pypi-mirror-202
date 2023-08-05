
from triple_quote_clean import TripleQuoteCleaner


def test_tabs():

    input_string = """hello world"""
    tqc = TripleQuoteCleaner()
    output_1 = '\n' + input_string >> tqc.tab
    output_2 = '\n' + input_string >> tqc.tab.tab

    print("Input")
    print(input_string)

    print("Output Single Tab")
    print(output_1)

    print("Output Double Tab")
    print(output_2)

    assert output_1 == "    "+input_string, f"{output_1} != '    hello world'"


if __name__ == "__main__":
    test_tabs()
