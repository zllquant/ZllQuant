from strategy.stockpool.low_pe_stock_pool import LowPeStockPool


class StockPoolFactory:
    @staticmethod
    def get_stock_pool(pool_name, begin_date, end_date, interval):
        if pool_name == 'low_pe_stock_pool':
            return LowPeStockPool(begin_date, end_date, interval)
