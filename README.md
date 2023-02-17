# Quality Tool

## Setup

Make sure you have [Poetry](https://python-poetry.org/docs/) installed.
You can then get started by running:

```sh
poetry install
```

## Running, Testing, and Formatting

This is all done using poetry. To run:

```sh
poetry run python byoqm/main.py <path/to/source/code>
```

To test:

```sh
poetry run python -m unittest
```

To format:

```
poetry run black .
```


## Building Tree Sitter Grammars

Make sure you have a `build/` and `grammars/` folders in the root of the project:

```sh
mkdir build grammars
```

Clone the python grammar into `grammars/`:


```sh
cd grammars && git clone https://github.com/tree-sitter/tree-sitter-python && cd -
```

Build the grammar file:

```sh
poetry run python byoqm/build_treesitter.py
```
