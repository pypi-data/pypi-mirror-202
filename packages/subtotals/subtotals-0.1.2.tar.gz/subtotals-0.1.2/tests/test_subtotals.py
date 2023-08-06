import os
import pandas as pd
from subtotals import groupby
from pandas.testing import assert_frame_equal as afe

folder = os.path.dirname(os.path.abspath(__file__))
sales_file = os.path.join(folder, 'sales.csv')
sales_data: pd.DataFrame = pd.read_csv(sales_file)


def test_subtotal():
    agg = {'sales': 'sum', 'growth': 'min'}
    cols = ['country', 'city', 'product', 'sales', 'growth']
    actual = groupby(sales_data, ['country', 'city', 'product'], agg, margins_name='All')

    l0 = sales_data.groupby([0] * len(sales_data), sort=False).agg(agg)
    l0['country'] = l0['city'] = l0['product'] = 'All'
    afe(actual[actual['level'] == 0][cols].reset_index(drop=True), l0[cols])

    l1 = sales_data.groupby('country', sort=False).agg(agg).reset_index()
    l1['city'] = l1['product'] = 'All'
    afe(actual[actual['level'] == 1][cols].reset_index(drop=True), l1[cols])

    l2 = sales_data.groupby(['country', 'city'], sort=False).agg(agg).reset_index()
    l2['product'] = 'All'
    afe(actual[actual['level'] == 2][cols].reset_index(drop=True), l2[cols])

    l3 = sales_data.groupby(['country', 'city', 'product'], sort=False).agg(agg).reset_index()
    afe(actual[actual['level'] == 3][cols].reset_index(drop=True), l3[cols])
