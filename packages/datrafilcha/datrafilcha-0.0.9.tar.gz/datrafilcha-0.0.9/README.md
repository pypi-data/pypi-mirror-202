# datrafilcha


Data transformed/filtred charted.


Give CSV, choose column, choose function, get plot.

### Data filters/transformers
  - Uniq values: count most repeated lines
  - Frequency of occurrences: Suppose you want to know how often you will meet the value when reading list of values line by line expressed as histogram.
    For example in the following set:
        a,b,a,b,a,b,a,b
    We have 8 items and we want to know the frequency of occurrences of letter b.
    X axe value = number of items - sequence
    Y axe value = for each x - y is either 0 b is not present or 1 b is present

    Outputs x,y coordinates 0:0,1:1,2:0,3:1,4:0:5:1... each 1 is bar on plot, 0 is empty space


### Sample code

```
from datrafilcha import facade


configuration = {
    'id': 'UniqValues',
    'column_name': <COLUMN NAME>,
    'desc': True,
    'limit': 5,
}

data_filters_facade = facade.DataFiltersFacade()
html_plot = data_filters_facade.csv_column(configuration,
                                            data_source_file)

with open('new_plot.html', 'w') as f:
    f.write(new_chart.html)
```
