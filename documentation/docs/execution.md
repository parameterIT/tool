# How to run?

Run and output results of the configured quality model on the targeted source code.

```sh
poetry run core [OPTIONS] SRC_ROOT QUALITY_MODEL
```
E.g.
```sh
poetry run core --show-graphs false . code_climate
```

## Additional arguments

| Options | Default  | Description  |
|---|---|---|
| -o, --output TEXT  |   | The path to the output directory  |
| --save-file BOOLEAN  | TRUE  | Boolean determining whether or not a file should be saved in the output directory  |
| --show-graphs BOOLEAN  | TRUE  | Boolean determining whether or not the dashboard should be saved  |
| --start-data [%Y-%m-%d]   |   | The point in time that the graphs should display from  |
| --end-data [%Y-%m-%d] | | The point in time that the graphs should display from |
| --help | | Show this message and exit
| --verbose | -v | Shows more detailed log statements (for developing)

## Developer specific information
### Running tests 
Running the current tests can be done be using the following command: 
```sh
poetry run test
```
### Black formatter
We have made use of _black_ to format our files, and any changes made to the program will require _black_ to be run before being able to merge into the main branch. 

_Black_ is used by running the following command: 
```sh
poetry run black .
```