# Architectural Overview
An overview of the architecture of the tool is key to understanding its usefulness.

## Plugin style system
The essence of this tool is to explore the possibility of having a fully parameterized Software Quality Assessment Tool _(SWQAT)_. Therefore, we have opted to choose a modular plug-in architecture for both the actual quality model as well as the visualization. 

The tool will make use of a quality model that contains an arbitrary amount of aggregations, which are made up of underlying aggregations or metrics. Metrics are the bottom-most level of the quality models, and are repsonsible for keeping track of violations. 

To ensure transparency, the tool can make use of any implemented quality model.
Configuring these models with transparent measured metrics and user-defined aggregation formulas allows developers and businesses to create a better approximation of actual software quality.