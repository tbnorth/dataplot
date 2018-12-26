# DataPlot

A simple Python class wrapping separate data preparation and
plot building steps in a [matplotlib](https://matplotlib.org/)
pipeline.

Separating the data preparation and plot building:

 - makes it easy to provide the exact data in a plot.
 - makes the data in a plot available for tests etc., useful
   when extracting the data requires non-trivial processing and
   other questions about the data arise.

The basic idea is a that a JSON encodable `dict` of data is generated
by the data preparation function, and this `dict` is used by the plot
building function to make the plot.  The DataPlot class is just a thin
wrapper around this idea which handles saving the plots in different
formats and sets up a suggested skeleton for the `dict`:

```python
    {
        # author info. etc.
        '_metadata': {
            'generated': time.asctime(),
            # a pointer to this class, to explain JSON format
            'relation': "https://github.com/tbnorth/dataplot",
        },
        # general plot data, title, x label, etc.
        'ax': {'x': {}, 'y': {}},
        'ds': {},  # x, y, etc., lists of the same length
        'kv': {},  # arbitrary key / value info.
    }
```
