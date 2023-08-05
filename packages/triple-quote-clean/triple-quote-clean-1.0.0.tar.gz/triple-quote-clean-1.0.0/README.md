# triple-quote-clean

TripleQuoteCleaner is a Python class that can be used to clean triple-quoted
strings in a variety of ways. It's designed to be used in cases where you want
to remove extraneous whitespace and/or add indentation to a triple-quoted
string. This is useful when dealing with extensions/code that require some
extraneous metadata in the string.

To use TripleQuoteCleaner, simply import it into your Python script:

```python
from triple_quote_clean import TripleQuoteCleaner
```

## Usage

### Basic Usage

TripleQuoteCleaner is designed to be used with the `>>`, `<<`, `<` `>`, `**`
operators in Python. All the different operators were selected to allow for
flexibility when considering the operator order, i.e. `**` takes the highest
priority and should be used when adding strings

Here's an example:

```python
query = """--sql
    select *
    from some_database
"""

tqc                = TripleQuoteCleaner()
tqc.skip_top_lines = 1
output             = query >> tqc
```

In this example, the >> operator is used to "pipe" the query string into tqc.
skip_top_lines is set to 1 so that the first line of the query (the "--sql"
line) is skipped. The output of this code will be:

```sql
select *
from some_database
```

### Indentation

TripleQuoteCleaner can also be used to add indentation to a triple-quoted
string. Here's an example:

```python
input_string = """hello world"""
tqc          = TripleQuoteCleaner()
output       = '\n' + input_string >> tqc.tab
```

In this example, tqc.tab is used to add one level of indentation to the output
string. The output of this code will be:

```markdown
    hello world
```

### Guide Characters

Indentation can also be specified using a "guide character". This is useful if
you want to maintain a certain level of tabs in all your paragraphs in your
triple-quoted string. Here's an example:

```python
query = """--sql
$$
    select *
    from some_database
"""

tqc                = TripleQuoteCleaner()
tqc.skip_top_lines = 1
output             = query >> tqc
```

In this example, tqc.guide_character is set to "$$" so that the 4 beginning
spaces will be maintained . The output of this code will be:

```sql
    select *
    from some_database
```
