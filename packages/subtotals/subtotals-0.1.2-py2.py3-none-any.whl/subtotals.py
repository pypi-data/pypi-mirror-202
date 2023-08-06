'''Generate groupby subtotals for Pandas DataFrames.'''

import pandas as pd
from typing import Union, List, Dict, Callable

__version__ = '0.1.2'


def groupby(
    data: pd.DataFrame,
    by: List[str],
    agg: Union[Callable, str, List[Union[str, Callable]], Dict[str, Union[str, Callable]]],
    margins_name: str = 'Total',
) -> pd.DataFrame:
    '''Group a Pandas DataFrame with subtotals.

    Parameters:

        data: The data to subtotal
        by: Levels by which the data must be grouped
        agg: How to aggregated columns. See Pandas
            [GroupBy.agg](https://pandas.pydata.org/docs/reference/api/pandas.core.groupby.DataFrameGroupBy.agg.html)
        margins_name: Name of the row that contains the subtotals

    Returns:
        Subtotaled DataFrame
    '''
    grand_total = data.groupby(pd.Series(0, data.index), sort=False).agg(agg)
    grand_total['level'] = 0
    frames = [grand_total]
    for level in range(1, 1 + len(by)):
        frame = data.groupby(by[:level], sort=False, as_index=False).agg(agg)
        frame['level'] = level
        frames.append(frame)
    result = pd.concat(frames, ignore_index=True)
    if margins_name is not None:
        result[by] = result[by].astype(object).fillna(margins_name)
    return result
