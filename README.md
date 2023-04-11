# Quality Tool

## Setup

Make sure you have [Poetry >= 1.2.0](https://python-poetry.org/docs/) installed.
You can then get started by running:

```sh
poetry install
```

### Code duplication - cpd

As of this moment, we are using copy paste detector to find duplicate code.
This requires you to download cpd and place the `bin/` and `lib/` folder (and their files) in a cpd subfolder in metrics (`metrics/cpd/<cpd folders goes here>`).

You can download cpd from the following link (check if there is a newer release): https://github.com/pmd/pmd/releases/tag/pmd_releases/6.54.0

## Running, Testing, and Formatting

This is all done using poetry. To run:

```sh
poetry run main <path/to/source/code> <Quality_model> <language>
```

To see supported languages please refer to: `byoqm/source_coordinator/languages.py`

Optional values can be gotten by running:

```sh
poetry run main --help
```

To test:

```sh
poetry run test
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
cd grammars && git clone --depth 1 https://github.com/tree-sitter/tree-sitter-python && git clone --depth 1 https://github.com/tree-sitter/tree-sitter-c-sharp && git clone --depth 1 https://github.com/tree-sitter/tree-sitter-java && cd -
```

Build the grammar file:

```sh
poetry run python byoqm/build_treesitter.py
```
