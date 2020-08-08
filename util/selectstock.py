import rqdatac as rqd
import pandas as pd

rqd.init()


def get_universe(date):
    return (
        rqd.all_instruments(type='CS', date=date)
            .loc[lambda df: ~df['status'].isin(['Delisted', 'Unknown'])]
            .loc[:, 'order_book_id']
            .tolist()
    )


def drop_st(universe, date):
    is_st = rqd.is_st_stock(universe, date, date).squeeze()
    assert isinstance(is_st, pd.Series), 'is_st is not series'
    return is_st.index[~is_st]


def drop_suspended(universe, date):
    # squeeze(axis=0):DataFrames with a single column or a single row are squeezed to a Series
    is_suspended = rqd.is_suspended(universe, date, date).squeeze()
    assert isinstance(is_suspended, pd.Series), 'is_suspended is not series'
    return is_suspended.index[~is_suspended]


def drop_recently_listed(universe, date, min_days_listed=60):
    # 一个列表,里面元素是Instrument对象
    instruments = rqd.instruments(universe)
    return [inst.order_book_id
            for inst in instruments
            if inst.days_from_listed(date) > min_days_listed]


def get_industry(universe, date):
    return (
        rqd.shenwan_instrument_industry(universe, date).loc[:, 'index_name'].rename('industry')
    )
