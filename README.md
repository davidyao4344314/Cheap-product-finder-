# Cheap Product Finder

Stage 1 begins with a small Python backend package and seller-independent domain
models. The models define the data that later provider, validation, ranking, and
service layers will exchange.

## Structure

```text
src/cheap_product_finder/
    __init__.py
    models/
        __init__.py
        domain.py
tests/
    test_models.py
```

## Domain models

- `SearchRequest` keeps the user's original product query and requested location.
- `Location` supports a city alone or more detailed geographic information.
- `ProductRequirement` holds structured product details for future matching.
- `Seller` identifies a product source and its basic coverage.
- `ProductListing` is a common offer format across sellers. Monetary fields use
  `Decimal` so later cost calculations can avoid binary floating-point rounding.
- `SearchResult` holds the request, normalized location, listing groups, and
  diagnostics that a future search service will populate.

This commit contains data models only. It does not parse product queries, retrieve
listings, validate products, calculate totals, rank prices, or provide a CLI.

## Run tests

From the project root, using Python 3.10 or later:

```sh
PYTHONPATH=src python3 -m unittest discover -s tests -v
```
