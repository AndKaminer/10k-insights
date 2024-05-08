# Main Documentation [(Back to README)](/README.md)

See also: [Flask docs](/docs/flask.md), [Nonflask docs](/docs/nonflask.md)

## Installation/Setup
Look at the README

## Adding New Tickers
Simply add the (valid) ticker to the TICKERS list in the main __init__.py file.

## Adding New Sections of the 10K to Evaluate
Be my guest.
1. Parse it in the parser function in the FilingRetriever class in retrieval.py
2. Add it to the section_to_name dictionary in the main __init__.py
3. Unfortunately, you have to add it manually to the selections on the stock page, but
a fork could improve that pretty easily.
