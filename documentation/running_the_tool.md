# How to run?

Run and output results of the configured quality model on the targeted source code.

```
poetry run main [OPTIONS] SRC_ROOT QUALITY_MODEL
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