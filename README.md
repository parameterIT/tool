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

### Programming Language Detection - GitHub Linguist

To detect the programming languages of source code files we use GitHub linguist by running it in a docker container. 
Make sure you have [Docker >= 23.0.4](https://docs.docker.com/) installed.
You will also need to pull the docker image for GitHub Linguist:

```shell
docker pull toffernator/linguist
```

## Running, Testing, and Formatting

This is all done using poetry. To run:

```sh
poetry run core <path/to/source/code> <Quality_model>
```
e.g.
```sh
poetry run core . code_climate
```

To see supported languages please refer to: `byoqm/source_coordinator/languages.py`

Optional values can be gotten by running: 

```sh
poetry run core --help
```

To test:

```sh
poetry run test
```

To format:

```
poetry run black .
```


## Building Tree-Sitter Grammars

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
poetry run python core/build_treesitter.py
```
