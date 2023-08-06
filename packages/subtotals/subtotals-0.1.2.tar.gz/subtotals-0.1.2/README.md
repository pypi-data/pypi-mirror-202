<!-- markdownlint-disable first-line-h1 -->

**subtotals** groups Pandas DataFrames and creates subtotals at each level.

## Install

```shell
python3 -m pip install subtotals
```

subtotals requires Python 3 or above.

## Usage

If you have a [sales.csv](https://github.com/gramener/subtotals/blob/master/tests/sales.csv) like this:

```text
country    city              product   sales   growth
India      Hyderabad         Biscuit   866.1   -0.270
India      Hyderabad         Cake       26.4   -0.242
India      Hyderabad         Cream      38.3   -0.291
India      Hyderabad         Eggs      513.7   -0.113
India      Bangalore         Biscuit    41.9   -0.402
India      Bangalore         Cake       52.2    0.064
India      Bangalore         Cream      17.8   -0.052
India      Bangalore         Eggs      178.9   -0.261
India      Coimbatore        Biscuit   217.4    0.114
India      Coimbatore        Cake
India      Coimbatore        Cream      94.4   -0.288
India      Coimbatore        Eggs       72.8   -0.066
Singapore  Singapore         Biscuit   671.0   -0.014
Singapore  Singapore         Cake      560.2   -0.197
Singapore  Singapore         Cream     237.9    0.194
Singapore  Singapore         Eggs      719.0    0.118
USA        South Plainfield  Biscuit    18.3   -0.154
USA        South Plainfield  Cake       41.6    0.043
USA        South Plainfield  Cream      32.4    0.068
USA        South Plainfield  Eggs       12.5    0.084
USA        Newport Beach     Biscuit  1352.4    0.384
USA        Newport Beach     Cake      190.2    0.119
USA        Newport Beach     Cream     148.2    0.053
USA        Newport Beach     Eggs
```

... then:

```python
subtotals.groupby(
  data=pd.read_csv('tests/sales.csv'),
  by=['country', 'city'],
  agg={'sales': 'sum', 'growth': 'max'}
)
```

... looks like this:

```text
level    country              city   sales  growth
    0      Total             Total  6103.6   0.384    <- grand total
    1      India             Total  2119.9   0.114    <- sub total by country
    1  Singapore             Total  2188.1   0.194
    1        USA             Total  1795.6   0.384
    2      India         Hyderabad  1444.5  -0.113    <- sub sub total by city
    2      India         Bangalore   290.8   0.064
    2      India        Coimbatore   384.6   0.114
    2  Singapore         Singapore  2188.1   0.194
    2        USA  South Plainfield   104.8   0.084
    2        USA     Newport Beach  1690.8   0.384
```

1. The first row has the grand total of all metrics.
2. The next set of rows have the sub total by the first group (country)
3. The next set of rows have the sub sub total by the second
`groupby` elements, and so on.

Total rows are labels by `margins_name` which defaults to `Total`.


## API

`subtotals.groupby` returns a subtotal-ed DataFrame and accepts:

- `data` (pd.DataFrame): The data to group and subtotal
- `groups` (list of column names): Levels by which the data must be grouped
- `agg`: How to aggregated columns. Same as Pandas
  [GroupBy.agg](https://pandas.pydata.org/docs/reference/api/pandas.core.groupby.DataFrameGroupBy.agg.html)
- `margins_name` (str): Name of the row that contains the subtotals
