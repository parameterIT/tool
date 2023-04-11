

  * All authors should be listed in pyproject.toml
  * Likely `main` is not a good name for the program
  * I could not quickly figure out what name for the QUALITY_MODEL parameter is appropriate/needed
  * Why do I have to specifiy a LANGUAGE parameter?
    - It seems counter-intuitive to me that I have to specify a language when running with a multi-language quality model like the one from Code Climate. (`poetry run main . code_climate python`)
  * How would it work to build a release of byoqm that would include tree-sitter sources?
